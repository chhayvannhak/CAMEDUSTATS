# EduInsight Cambodia

An interactive Streamlit dashboard for exploring Cambodia Education Statistics and Indicators 2015–2016.

## Project Structure

```text
EduInsight-Cambodia/
│
├── app.py
├── style.css
├── requirements.txt
├── README.md
└── CambodiaEducationStatisticsandIndicators2015-2016.csv
```

## Features

1. Home — Education statistics overview
2. National Dashboard — National education indicators and visualizations
3. Provincial Analysis — Compare education indicators by province
4. Student & Gender — Explore student enrollment and gender participation
5. Education Workforce — Analyze teachers and education personnel
6. Data Explorer — Search, filter, inspect, and download CSV data
7. About Project — Project objectives, methodology, and limitations

## Technologies

- Python
- Streamlit
- Pandas
- Plotly
- Custom CSS

## Installation on Windows

Open the project folder in VS Code.

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the application:

```powershell
streamlit run app.py
```

Open your browser:

```text
http://localhost:8501
```

## Dataset

Cambodia Education Statistics and Indicators 2015–2016.

The dashboard uses historical data from the supplied CSV file.

## Methodology Notes

- Male enrollment is derived by subtracting female enrollment from total enrollment.
- Male repeat students are derived from total repeat students minus female repeat students.
- Male teachers are derived from total teachers minus female teachers.
- Female participation percentages are calculated from the corresponding totals.
- Student-to-teacher values are aggregate proxies, not classroom-level ratios.
- The dataset represents one historical reporting period and does not establish multi-year trends.

## Important

Keep the CSV file in the same folder as app.py.

Keep the filename unchanged:

CambodiaEducationStatisticsandIndicators2015-2016.csv
