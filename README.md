# CAMEDUSTATS — Cambodia Public Education Statistics Portal

**CAMEDUSTATS** is an interactive, bilingual (**English / ភាសាខ្មែរ**) web analytics platform built with **Python, Streamlit, Pandas, and Plotly** to explore multi-year public education statistics across all 25 provinces of Cambodia (2015–2016 through 2020–2021).

Instead of displaying static raw counts, the platform automatically harmonizes multiple yearly datasets into normalized educational risk, equity, and resource-strain indicators—complete with a responsive Dark/Light theme and interactive visualizations.

---

## Project Structure

```text
CAMEDUSTATS/
├── app.py                                                # Main application, ETL pipeline, bilingual dictionary & views
├── style.css                                             # Custom layout, theme variables, fixed sidebar & typography
├── requirements.txt                                      # Python dependencies
├── .gitignore                                            # Excludes cache & virtual environment files
├── README.md                                             # Documentation & architecture guide
├── CambodiaEducationStatisticsandIndicators2015-2016.csv # 2015–2016 provincial dataset
├── CambodiaPublicEducationStatistics2016-2017.csv        # 2016–2017 provincial dataset
├── CambodiaPublicEducationStatistics2017-2018.csv        # 2017–2018 provincial dataset
├── CambodiaPublicEducationStatistics2018-2019.csv        # 2018–2019 provincial dataset
└── CambodiaPublicEducationStatistics2020-2021.csv        # 2020–2021 provincial dataset
```

> **Note:** Placing any additional yearly MoEYS CSV file inside the project folder (or a `data/` subfolder) is automatically discovered and integrated on startup.

---

## Core System Architecture (How It Works)

Use these four pillars when explaining the engineering behind **CAMEDUSTATS** to your mentor:

1. **Automated Multi-Year ETL & Schema Harmonization (`pathlib`, `re`, `pandas`)**
   - Uses `pathlib.Path.glob("*.csv")` and regex (`re.search`) to automatically detect every academic year file and extract its reporting period.
   - Resolves real-world inconsistencies across historical MoEYS files without modifying the original CSVs:
     - Renames the column typo `t_e1264nrol` $\rightarrow$ `t_enrol` in the `2017–2018` file.
     - Standardizes province spelling drift (`Tbaung Khmum` $\rightarrow$ `Tboung Khmum`) in `2020–2021` so longitudinal trend lines and map coordinates stay continuous.
     - Coerces numeric columns and safely fills blank cells in `2018–2019` to prevent calculation errors.
   - Cached with `@st.cache_data` so CSV parsing and indicator calculations run once rather than on every UI click.

2. **State Management & Multi-Year Aggregation (`st.session_state`, `pandas.groupby`)**
   - Tracks the active page, selected year filter, language (`en` / `km`), and color theme (`dark` / `light`) in `st.session_state`.
   - Defaults to **All Years (2015–2021)** by computing each province's **annual average** (`groupby(["prov_en", "prov_kh"]).mean()`). This prevents double-counting the same students across consecutive school years.

3. **Bilingual Localization Engine (i18n)**
   - Uses a centralized `TEXT` dictionary containing paired English and Khmer strings for every heading, chart title, axis label, hover tooltip, and table column.
   - Dynamically maps province labels between `prov_en` and `prov_kh` and loads unified **Manrope** + **Noto Sans Khmer** Google Fonts across HTML and Plotly canvas elements.

4. **Dynamic Theme & Custom UI Layer (`CSS Variables`, `html.escape`)**
   - A Python token generator (`getThemeTokens`) injects CSS custom properties (`--bg`, `--surface`, `--border`, `--text`, `--risk-high`, etc.) and synchronizes those exact hex values with Plotly charts and map backgrounds.
   - Custom HTML components pass through a helper that strips leading indentation and escapes strings via `html.escape` for safe, predictable rendering, while preserving Streamlit's native `Material Symbols Rounded` icon font.

---

## Page-by-Page Technology Breakdown

| Page / Module | Purpose | Technologies & Techniques Used |
| :--- | :--- | :--- |
| **Global Shell (Sidebar & Top Bar)** | Navigation, year filtering, language switching, and Dark/Light mode | **Streamlit** (`st.sidebar`, `st.button`, `st.selectbox`, `st.columns`, `st.session_state`), **Custom CSS** (flexbox fixed sidebar pinning the Loaded Data summary to the bottom; CSS variables for instant theme switching). |
| **1. Overview** | National executive summary, spatial map, top priority provinces, and national multi-year trends | **Pandas** (aggregations & min-max scaling), **Plotly Express** (`px.scatter_geo` bubble map using mapped provincial lat/lon coordinates; `px.area` enrollment trajectory), **Plotly Graph Objects** (`go.Figure` dual-axis line chart combining repeater rate and teacher load), **HTML/CSS** (severity color-coded Priority Watchlist cards). |
| **2. Provincial Insights** | Risk-vs-strain quadrant benchmarking, full 25-province rankings, and multi-province trend comparison | **Plotly Express** (`px.scatter` quadrant matrix with `add_vline`/`add_hline` national average benchmarks and selective outlier `add_annotation` callouts; horizontal `px.bar` rankings; `px.line` multi-year comparator), **Streamlit** (`st.multiselect` capped at 6 provinces for readability). |
| **3. Equity & Workforce** | Gender parity in enrollment and repetition, female teacher representation, and school infrastructure | **Pandas** (derived male counts and gender-specific repetition rates), **Plotly Graph Objects** (`go.Bar` grouped horizontal chart comparing male vs. female repeater rates), **Plotly Express** (horizontal `px.bar` for female teacher share with a 50% parity line, plus Top 12 rankings for disadvantaged schools and pagoda classes). |
| **4. Data Table** | Interactive exploration and clean data export | **Pandas** (case-insensitive bilingual filtering across `prov_en` and `prov_kh`, rounding & column pruning to keep only essential indicators), **Streamlit** (`st.text_input`, `st.dataframe`, `st.download_button` exporting UTF-8 with BOM `utf-8-sig` so Khmer script opens cleanly in Excel). |
| **5. About** | Transparent documentation of goals, data coverage, formulas, and limitations | **Custom HTML/CSS** (structured two-column documentation cards) driven by the same bilingual `TEXT` dictionary so documentation translates seamlessly into Khmer. |

---

## Methodology & Indicator Formulas

All derived metrics are calculated dynamically from the original MoEYS source columns:

| Indicator | Formula | Source Columns |
| :--- | :--- | :--- |
| **Repeater Rate (%)** | $\frac{\text{Repeat Students}}{\text{Total Enrollment}} \times 100$ | `t_repeat`, `t_enrol` |
| **Students per Teacher** *(Aggregate Proxy)* | $\frac{\text{Total Enrollment}}{\text{Total Teachers}}$ | `t_enrol`, `t_teacher` |
| **Average Class Size** | $\frac{\text{Total Enrollment}}{\text{Total Classes}}$ | `t_enrol`, `no_class` |
| **Disadvantaged School Share (%)** | $\frac{\text{Disadvantaged Schools}}{\text{Total Schools}} \times 100$ | `dis_school`, `no_school` |
| **Female Enrollment / Teacher Share (%)** | $\frac{\text{Female Count}}{\text{Total Count}} \times 100$ | `enrol_girl` / `t_enrol`, `teacher_f` / `t_teacher` |

**Composite Priority Score (0–100)**

Each component is min-max normalized across the 25 provinces to $[0, 1]$ and combined using weighted scoring:

```math
\text{Priority Score} = \left(0.40 \cdot \text{Norm}(\text{Repeater Rate}) + 0.40 \cdot \text{Norm}(\text{Students per Teacher}) + 0.20 \cdot \text{Norm}(\text{Disadvantaged Share})\right) \times 100
```

- **Priority Tiers:** High Priority ($\ge 55$), Moderate ($35$–$54.9$), Lower Strain ($< 35$).
- **Derived Male Counts:** Calculated as total minus female counts (`t_enrol - enrol_girl` and `t_repeat - repeat_gir`).
- **All-Years View:** Aggregates each province by its multi-year annual average to avoid double-counting students across consecutive academic years.

---

## Installation & Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/chhayvannhak/CAMEDUSTATS.git
cd CAMEDUSTATS
```

### 2. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies & Launch

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Limitations & Responsible Use

- **Provincial Aggregation:** Indicators are macro provincial proxies and may mask urban-rural disparities within individual districts or schools.
- **Historical Coverage:** Represents reported MoEYS public education statistics from `2015–2016` through `2020–2021` (interim missing years such as `2019–2020` are omitted rather than interpolated).
- **Descriptive Scope:** Visualizations highlight relative disparities to support exploration and discussion; they do not establish causality.