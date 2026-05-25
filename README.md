<div align="center">
  <h1>✨ Cleany</h1>
  <p><b>An elegant, highly automated Data Cleaning & Reporting platform built with Flask and Pandas.</b></p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![Pandas](https://img.shields.io/badge/Pandas-1.3%2B-150458.svg)](https://pandas.pydata.org/)
</div>

---

CleanFlow AI is designed to take raw, messy datasets and automatically apply missing value imputation, duplicate removal, formatting standardization, and outlier clipping. It generates a polished Excel dataset and a comprehensive Data Quality PDF report with just a few clicks.

## 🚀 Key Features

- **No Login Required**: Instant access to data processing.
- **Automated Cleaning Pipeline**: Automatically detects and handles missing values, duplicates, and outliers (IQR).
- **Premium Analytics**: Generates summary statistics and correlation heatmaps.
- **AI Insights**: Natural language summaries of your dataset's condition.
- **Export Engine**: Download cleaned datasets in CSV/Excel and quality reports in PDF.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite (SQLAlchemy)
- **Reporting**: ReportLab (PDF), OpenPyXL (Excel)
- **Frontend**: Jinja2 Templates, HTML5/CSS3 (Custom Editorial UI)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rajmund09/Cleany.git
   cd Cleany
   ```

2. **Set up a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and configure your `SECRET_KEY`.
   ```bash
   cp .env.example .env
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   *The app will be available at `http://127.0.0.1:5000`.*

## 📂 Project Structure

```text
├── ai_engine/          # Logic for natural language insights
├── analytics/          # Statistics and correlation algorithms
├── api/                # RESTful routes handling uploads/processing
├── data_cleaning/      # Pandas-based data anomaly handling
├── database/           # SQLite setup and models
├── exports/            # PDF/Excel report generation modules
├── static/             # Custom high-end CSS and JS assets
├── templates/          # Jinja2 HTML templates
├── app.py              # Main application entry point
└── config.py           # Application configuration
```

## 🔒 Security & Data Privacy

This application is designed to process data locally. Uploaded datasets, generated reports, and local SQLite databases are automatically excluded from version control via `.gitignore` to prevent any accidental data leaks to GitHub.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
