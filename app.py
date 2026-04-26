from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Storage Tiers per Provider ────────────────────────────────────────────────
STORAGE_TIERS = {
    "aws": [
        {"id": "standard",          "label": "Standard",          "rate": 0.023},
        {"id": "infrequent_access", "label": "Infrequent Access", "rate": 0.0125},
        {"id": "glacier",           "label": "Glacier",           "rate": 0.004},
    ],
    "azure": [
        {"id": "hot",     "label": "Hot",     "rate": 0.0184},
        {"id": "cool",    "label": "Cool",    "rate": 0.010},
        {"id": "archive", "label": "Archive", "rate": 0.002},
    ],
    "gcp": [
        {"id": "standard", "label": "Standard", "rate": 0.020},
        {"id": "nearline", "label": "Nearline", "rate": 0.010},
        {"id": "coldline", "label": "Coldline", "rate": 0.007},
        {"id": "archive",  "label": "Archive",  "rate": 0.004},
    ],
}

# ── Compute & Transfer rates (unchanged) ─────────────────────────────────────
PRICING = {
    "aws":   {"name": "AWS",   "compute": 0.0416, "transfer": 0.09},
    "azure": {"name": "Azure", "compute": 0.0380, "transfer": 0.087},
    "gcp":   {"name": "GCP",   "compute": 0.0350, "transfer": 0.12},
}


def get_storage_rate(provider: str, tier_id: str | None) -> tuple[float, str]:
    """Return (rate, label) for the given provider + tier. Falls back to first tier."""
    tiers = STORAGE_TIERS.get(provider, STORAGE_TIERS["aws"])
    if tier_id:
        for t in tiers:
            if t["id"] == tier_id:
                return t["rate"], t["label"]
    return tiers[0]["rate"], tiers[0]["label"]


def next_cheaper_tier(provider: str, current_tier_id: str):
    """Return the next cheaper tier dict, or None if already cheapest."""
    tiers = STORAGE_TIERS.get(provider, [])
    for i, t in enumerate(tiers):
        if t["id"] == current_tier_id and i + 1 < len(tiers):
            return tiers[i + 1]
    return None


def calc_provider(provider: str, storage_gb: float, compute_hours: float,
                  transfer_gb: float, tier_id: str | None = None):
    """Calculate costs for one provider."""
    p = PRICING[provider]
    rate, label = get_storage_rate(provider, tier_id)
    storage_cost  = round(storage_gb * rate, 2)
    compute_cost  = round(compute_hours * p["compute"], 2)
    transfer_cost = round(transfer_gb * p["transfer"], 2)
    total         = round(storage_cost + compute_cost + transfer_cost, 2)
    return {
        "storage": storage_cost,
        "compute": compute_cost,
        "transfer": transfer_cost,
        "total": total,
        "tier_label": label,
        "tier_id": tier_id or STORAGE_TIERS[provider][0]["id"],
        "storage_rate": rate,
    }


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(force=True)

    provider      = data.get("provider", "aws").lower()
    storage_gb    = float(data.get("storage_gb", 0))
    compute_hours = float(data.get("compute_hours", 0))
    transfer_gb   = float(data.get("transfer_gb", 0))
    tier_id       = data.get("storage_tier")       # e.g. "glacier"
    priority      = data.get("priority", "balanced")  # balanced | storage | compute

    # Selected provider uses chosen tier; others use their default (first) tier
    selected = calc_provider(provider, storage_gb, compute_hours, transfer_gb, tier_id)

    all_providers = {}
    for key in PRICING:
        if key == provider:
            all_providers[PRICING[key]["name"]] = selected
        else:
            all_providers[PRICING[key]["name"]] = calc_provider(
                key, storage_gb, compute_hours, transfer_gb, None
            )

    # ── Priority-based recommendations ────────────────────────────────
    recommendation = {}
    total = selected["total"]

    if priority == "storage" and total > 0:
        storage_pct = (selected["storage"] / total) * 100 if total else 0
        recommendation["highlight"] = "storage"
        recommendation["warning"] = storage_pct > 50
        recommendation["text"] = (
            "For storage-heavy workloads, consider moving infrequently accessed "
            "data to Cool/Nearline/Glacier tier to reduce costs."
        )
        nxt = next_cheaper_tier(provider, selected["tier_id"])
        if nxt and storage_gb > 0:
            cheaper_cost = round(storage_gb * nxt["rate"], 2)
            savings = round(selected["storage"] - cheaper_cost, 2)
            recommendation["savings"] = {
                "tier": nxt["label"],
                "amount": savings,
                "text": f"Switch to {nxt['label']} → save ${savings:.2f}/month",
            }

    elif priority == "compute" and total > 0:
        compute_pct = (selected["compute"] / total) * 100 if total else 0
        recommendation["highlight"] = "compute"
        recommendation["warning"] = compute_pct > 50
        recommendation["text"] = (
            "For compute-heavy workloads, consider Reserved Instances or "
            "Committed Use Discounts for up to 60% savings on listed price."
        )
        discounted = round(selected["compute"] * 0.63, 2)  # 37% off
        recommendation["savings"] = {
            "tier": "1-year commitment",
            "amount": round(selected["compute"] - discounted, 2),
            "text": f"With 1-year commitment → ~${discounted:.2f}/month",
        }

    else:  # balanced
        recommendation["highlight"] = None
        recommendation["warning"] = False
        costs = {"storage": selected["storage"], "compute": selected["compute"],
                 "transfer": selected["transfer"]}
        highest = max(costs, key=costs.get)
        recommendation["text"] = (
            f"The highest cost category is {highest}. "
            f"Consider optimising {highest} usage to reduce overall spend."
        )

    return jsonify({
        "provider": PRICING[provider]["name"],
        "storage_cost": selected["storage"],
        "compute_cost": selected["compute"],
        "transfer_cost": selected["transfer"],
        "total_cost": selected["total"],
        "tier_label": selected["tier_label"],
        "priority": priority,
        "recommendation": recommendation,
        "all_providers": all_providers,
    })


@app.route("/tiers/<provider>")
def tiers(provider):
    """Return available storage tiers for a provider."""
    provider = provider.lower()
    return jsonify(STORAGE_TIERS.get(provider, STORAGE_TIERS["aws"]))


@app.route("/pricing")
def pricing():
    """Return full pricing table."""
    result = {}
    for k, v in PRICING.items():
        result[k] = {
            "name": v["name"],
            "compute": v["compute"],
            "transfer": v["transfer"],
            "storage_tiers": STORAGE_TIERS[k],
        }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
