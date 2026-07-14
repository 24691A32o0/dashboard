# 📊 Sales Analytics Dashboard

An interactive sales analytics web app built with **Streamlit** and **Plotly** —
a deployable, browser-based upgrade of a typical exploratory sales-analysis notebook.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 📁 Upload your own CSV, or explore the bundled synthetic sample dataset
- 🎛️ Sidebar filters: date range, region, category, product
- 📌 KPI cards: total sales, total profit, total orders, avg order value, profit margin
- 📈 Interactive Plotly charts: product-wise sales, region share, monthly trend, category profit
- 🏆 Top-performing products table with adjustable rank count
- ⬇️ Download the currently filtered dataset as CSV
- 🔍 Raw data explorer

## Project Structure

```
sales-dashboard/
├── app.py                     # Main Streamlit app
├── generate_sample_data.py    # Script to (re)generate the sample dataset
├── data/
│   └── sales_data.csv         # Bundled sample sales data
├── .streamlit/
│   └── config.toml            # Theme configuration
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone and set up a virtual environment

```bash
git clone https://github.com/<your-username>/sales-dashboard.git
cd sales-dashboard
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the app locally

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### 3. (Optional) Regenerate sample data

```bash
python generate_sample_data.py
```

## Using Your Own Data

Upload a CSV via the sidebar. Expected columns:

| Column      | Required | Description                    |
|-------------|----------|---------------------------------|
| Order_ID    | optional | Unique order identifier         |
| Date        | ✅        | Order date (YYYY-MM-DD)         |
| Product     | ✅        | Product name                    |
| Category    | ✅        | Product category                |
| Region      | ✅        | Sales region                    |
| Quantity    | optional | Units sold                      |
| Unit_Price  | optional | Price per unit                  |
| Sales       | ✅        | Total sale amount (or auto-computed from Quantity × Unit_Price) |
| Profit      | optional | Profit amount                   |

## Deployment

### Streamlit Community Cloud (free, easiest)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app**, select this repo/branch, and set the main file to `app.py`.
4. Deploy — you'll get a public shareable URL.

### Other options

- **Render / Railway**: use a `Procfile` or start command:
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- **Docker**: build an image with `requirements.txt` installed, expose port `8501`,
  and run the same command as above.
- **Hugging Face Spaces**: choose the "Streamlit" SDK when creating a new Space and push this repo.

## Tech Stack

- [Streamlit](https://streamlit.io) — web app framework
- [Pandas](https://pandas.pydata.org) — data manipulation
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts

## License

MIT — feel free to use and adapt this project.
