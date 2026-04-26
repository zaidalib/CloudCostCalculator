# ☁️ Cloud Cost Calculator
**Note**: This project was done as a part of submission for the subject 'Sustainable Energy'.

---

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0-0075AB?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6383?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

> Simulate and compare cloud infrastructure costs across AWS, Azure, and GCP with intelligent recommendations for cost optimization — where sustainability meets savings.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **Multi-Provider Comparison** | Estimate costs across AWS, Azure, and GCP in a single calculation |
| **Tier-Based Storage Pricing** | Select from multiple storage tiers (Standard, Infrequent Access, Glacier, etc.) |
| **Workload Priority Modes** | Balanced, Storage Heavy, or Compute Heavy recommendations |
| **Visual Analytics** | Interactive bar charts and doughnut charts using Chart.js |
| **Real-Time Updates** | Live formula calculations as you type |
| **Cost Optimization Tips** | Smart recommendations with exact savings potential |

---

## 💰 Pricing Structure

### Storage Tiers

| Provider | Tiers & Rates |
|----------|---------------|
| **AWS** | Standard ($0.023) \| Infrequent Access ($0.0125) \| Glacier ($0.004) |
| **Azure** | Hot ($0.0184) \| Cool ($0.010) \| Archive ($0.002) |
| **GCP** | Standard ($0.020) \| Nearline ($0.010) \| Coldline ($0.007) \| Archive ($0.004) |

### Compute & Transfer Rates

| Provider | Compute (per hour) | Transfer (per GB) |
|----------|-------------------|-------------------|
| **AWS** | $0.0416 | $0.0900 |
| **Azure** | $0.0380 | $0.0870 |
| **GCP** | $0.0350 | $0.1200 |

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.14 + Flask |
| **Frontend** | HTML5 + Vanilla JavaScript |
| **Styling** | Tailwind CSS (CDN) |
| **Charts** | Chart.js 4.4.7 (CDN) |
| **Fonts** | Google Fonts (Space Mono, IBM Plex Mono) |

---

## 🏃 Installation & Setup

```bash
# Clone or navigate to the project directory
cd "Sustainable Calculator"

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install Flask
pip install flask

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

---

## 📋 Usage Guide

1. **Select Provider**: Click on AWS, Azure, or GCP to choose your preferred cloud provider
2. **Enter Usage**:
   - **Storage**: GB per month
   - **Compute**: Hours of runtime
   - **Data Transfer**: GB outbound
3. **Choose Storage Tier**: Select from available tiers for cost optimization
4. **Set Priority**: Choose workload priority (Balanced/Storage Heavy/Compute Heavy)
5. **Calculate**: Click "Calculate Costs" to see detailed breakdowns

### Example Calculation

For 500 GB storage, 720 compute hours, 100 GB transfer:

| Provider | Total Cost |
|----------|------------|
| **Azure** | $45.26 ✓ |
| **GCP** | $47.20 |
| **AWS** | $50.45 |

---

## 📊 Charts & Comparison

After calculation, the results include:

- **Bar Chart**: Cost breakdown by category (Storage, Compute, Transfer) for all providers
- **Doughnut Chart**: Total cost comparison with cheapest provider highlighted
- **Detailed Table**: Complete comparison with savings percentages

---

## 🌱 Sustainability Connection

**Cost optimization and environmental sustainability go hand in hand.**

The global data center industry consumes approximately **1–1.5% of the world's electricity** (IEA, 2024). Every dollar saved on unnecessary cloud resources represents:
- Reduced energy consumption
- Lower carbon emissions
- Less water usage for cooling
- Minimized electronic waste

> **Smart tip**: Moving infrequently accessed data to Glacier/Archive tiers can reduce storage costs by up to 82% — same energy reduction for the environment.

---

## 📂 Project Structure

```
Sustainable Calculator/
├── app.py                      # Flask backend server
├── templates/
│   └── index.html             # Single-page frontend application
└── README.md         # This MD File
```

---

## 🤝 Author

*Project for Sustainable Energy course - Semester 4*

---

## 📄 License

This project is created for educational purposes as part of a university coursework.
