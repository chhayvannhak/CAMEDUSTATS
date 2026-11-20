from pathlib import Path
import html
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# CAMEDUSTATS — Cambodia Education Statistics Portal
# ============================================================

st.set_page_config(
    page_title="CAMEDUSTATS | Cambodia Education Statistics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
CSS_FILE = BASE_DIR / "style.css"

FONT_FAMILY = "Manrope, 'Noto Sans Khmer', 'Leelawadee UI', sans-serif"

ESSENTIAL_NUMERIC = [
    "no_school",
    "dis_school",
    "no_class",
    "clas_pagod",
    "t_enrol",
    "enrol_girl",
    "t_repeat",
    "repeat_gir",
    "t_teacher",
    "teacher_f",
    "t_nonteach",
]

COLUMN_ALIASES = {
    "t_e1264nrol": "t_enrol",
    "total_enrol": "t_enrol",
}

PROVINCE_ALIASES = {
    "Tbaung Khmum": "Tboung Khmum",
    "Siem Reap": "Siemreap",
    "Ratanakiri": "Ratanak Kiri",
    "Mondulkiri": "Mondul Kiri",
}

PROVINCE_COORDS = {
    "Banteay Meanchey": (13.7532, 102.9896),
    "Battambang": (13.0957, 103.2022),
    "Kampong Cham": (11.9934, 105.4635),
    "Kampong Chhnang": (12.2500, 104.6667),
    "Kampong Speu": (11.4533, 104.5209),
    "Kampong Thom": (12.7111, 104.8887),
    "Kampot": (10.6104, 104.1815),
    "Kandal": (11.2237, 105.1259),
    "Kep": (10.4829, 104.3167),
    "Koh Kong": (11.6153, 102.9838),
    "Kratie": (12.4881, 106.0188),
    "Mondul Kiri": (12.4558, 107.1881),
    "Oddar Meanchey": (14.1610, 103.8216),
    "Pailin": (12.8489, 102.6093),
    "Phnom Penh": (11.5564, 104.9282),
    "Preah Sihanouk": (10.6253, 103.5234),
    "Preah Vihear": (13.8073, 104.9805),
    "Prey Veng": (11.4868, 105.3253),
    "Pursat": (12.5388, 103.9192),
    "Ratanak Kiri": (13.7394, 106.9873),
    "Siemreap": (13.3633, 103.8564),
    "Stung Treng": (13.5259, 105.9683),
    "Svay Rieng": (11.0879, 105.7993),
    "Takeo": (10.9908, 104.7850),
    "Tboung Khmum": (11.8891, 105.8760),
}

# ============================================================
# TRANSLATIONS (ENGLISH & KHMER)
# ============================================================

TEXT = {
    "en": {
        "brand_sub": "Cambodia Education Statistics",
        "nav_overview": "Overview",
        "nav_provincial": "Provincial Insights",
        "nav_equity": "Equity & Workforce",
        "nav_data": "Data Table",
        "nav_about": "About",
        "coverage_label": "LOADED DATA",
        "coverage_cycle_one": "1 Academic Year",
        "coverage_cycle_many": "{n} Academic Years",
        "coverage_provs": "{n} provinces · MoEYS Data",
        "all_years_opt": "All Years ({span})",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "footer_left": "CAMEDUSTATS · Cambodia Public Education Statistics",
        "footer_right": "Coverage: {span}",
        "overview_title": "National Education Overview",
        "overview_sub_all": "Annual averages across all loaded academic years ({span}) covering 25 provinces",
        "overview_sub_one": "National public education indicators for academic year {year} across 25 provinces",
        "kpi_enrol": "Total Enrollment",
        "kpi_enrol_avg": "Avg Annual Enrollment",
        "kpi_enrol_note": "Across {schools} schools",
        "kpi_repeat": "Repeater Rate",
        "kpi_repeat_avg": "Avg Repeater Rate",
        "kpi_repeat_note": "{count} repeat students",
        "kpi_str": "Students / Teacher",
        "kpi_str_avg": "Avg Students / Teacher",
        "kpi_str_note": "{teachers} active teachers",
        "kpi_dis": "Disadvantaged Schools",
        "kpi_dis_avg": "Avg Disadvantaged Schools",
        "kpi_dis_note": "{pagoda} classes in pagodas",
        "map_sec": "Provincial Map",
        "map_desc": "Bubble size represents enrollment and hover over any province for details",
        "map_metric_label": "Map Indicator",
        "watchlist_sec": "Priority Watchlist",
        "watchlist_desc": "Top 5 provinces ranked by combined repetition rate and teacher workload",
        "watchlist_sub": "Composite score (0–100) from repeater rate, students per teacher, and disadvantaged schools",
        "trend_sec": "Multi-Year National Trend",
        "trend_desc": "National enrollment, repetition rate, and teacher workload across loaded academic years",
        "chart_enrol_trend": "Total Student Enrollment Over Time",
        "chart_dual_trend": "Repeater Rate & Students per Teacher Over Time",
        "prov_title": "Provincial Insights",
        "prov_sub": "Compare grade repetition, teacher workload, and longitudinal trends across all 25 provinces",
        "quad_sec": "Teacher Load vs. Repeater Rate",
        "quad_desc": "Each bubble is a province (size = enrollment) — hover to view details and dashed lines show national averages",
        "quad_title": "Teacher Workload vs. Grade Repetition ({period})",
        "nat_avg": "National Avg",
        "rank_rep_title": "Grade Repeater Rate by Province (%)",
        "rank_str_title": "Students per Teacher by Province",
        "prov_trend_sec": "Provincial Trend Comparison",
        "prov_trend_desc": "Trace up to 6 provinces across all loaded academic years",
        "select_indicator": "Indicator",
        "select_provs": "Provinces to Compare",
        "eq_title": "Equity & Workforce",
        "eq_sub": "Gender representation in enrollment and repetition alongside teacher distribution and school facilities",
        "kpi_girl_enrol": "Female Enrollment",
        "kpi_girl_enrol_note": "{count} female students",
        "kpi_boy_rep": "Male Repeater Rate",
        "kpi_boy_rep_note": "vs. {girl_rate} for female students",
        "kpi_fem_teach": "Female Teachers",
        "kpi_fem_teach_note": "{count} female teachers",
        "kpi_class_size": "Avg Class Size",
        "kpi_class_size_note": "{classes} total classes",
        "chart_gender_rep": "Male vs. Female Repeater Rate by Province (%)",
        "chart_fem_teach": "Female Teacher Share by Province (%)",
        "chart_dis_top": "Top 12 Provinces by Disadvantaged Schools",
        "chart_pagoda_top": "Top 12 Provinces by Pagoda Classes",
        "male_label": "Male",
        "female_label": "Female",
        "data_title": "Data Table",
        "data_sub": "Essential provincial education indicators ready for search, filtering, and CSV export",
        "search_prov": "Search Province",
        "search_placeholder": "Type English or Khmer province name...",
        "showing_rows": "Showing {shown} of {total} records",
        "btn_download": "Download Filtered CSV",
        "col_year": "Year",
        "col_prov": "Province",
        "col_schools": "Schools",
        "col_dis": "Disadvantaged",
        "col_classes": "Classes",
        "col_pagoda": "Pagoda Classes",
        "col_enrol": "Enrollment",
        "col_girl_pct": "Female (%)",
        "col_rep_rate": "Repeater Rate (%)",
        "col_teachers": "Teachers",
        "col_str": "Students / Teacher",
        "col_cls_size": "Students / Class",
        "ind_priority": "Priority Score (0–100)",
        "ind_rep": "Repeater Rate (%)",
        "ind_str": "Students per Teacher",
        "ind_dis_pct": "Disadvantaged Schools (%)",
        "ind_enrol": "Total Enrollment",
        "ind_fem_teach": "Female Teachers (%)",
        "tier_high": "High Priority",
        "tier_mod": "Moderate",
        "tier_low": "Lower Strain",
        "hover_enrol": "Enrollment",
        "hover_rep": "Repeater Rate",
        "hover_str": "Students / Teacher",
        "hover_dis": "Disadvantaged Schools",
        "hover_cls": "Students / Class",
        "about_title": "About CAMEDUSTATS",
        "about_sub": "Open public education analytics platform built for exploring provincial disparities across Cambodia",
        "about_goal_title": "Project Goal",
        "about_goal_body": "CAMEDUSTATS transforms multi-year public education statistics from Cambodia into normalized, easy-to-compare provincial indicators. Instead of reading raw tables across separate PDFs and CSV files, researchers, students, and education planners can immediately inspect grade repetition hotspots, teacher staffing pressure, gender gaps, and disadvantaged school clusters in one unified interface.",
        "about_data_title": "Data Sources & Coverage",
        "about_data_items": [
            "Primary source: Cambodia Public Education Statistics and Indicators published by the Ministry of Education, Youth and Sport (MoEYS)",
            "Geographic scope: All 25 provinces and the capital municipality of Phnom Penh",
            "Temporal coverage: Multi-year reporting cycles automatically harmonized from local CSV files (2015–2016 through 2020–2021)",
            "Automated harmonization: Resolves cross-year schema differences including column typos, province spelling variations, and blank fields",
        ],
        "about_method_title": "Key Indicators & Methodology",
        "about_method_items": [
            "Repeater Rate (%): Repeat students divided by total enrollment (t_repeat / t_enrol × 100)",
            "Students per Teacher: Aggregate provincial ratio of enrolled students to active teachers (t_enrol / t_teacher)",
            "Average Class Size: Total enrollment divided by total reported classes (t_enrol / no_class)",
            "Priority Score (0–100): Min-max normalized weighted index combining Repeater Rate (40%), Students per Teacher (40%), and Disadvantaged School Share (20%)",
            "All-Years View: Aggregates each province by its multi-year annual average to prevent double-counting students across consecutive academic years",
        ],
        "about_limits_title": "Limitations & Responsible Use",
        "about_limits_items": [
            "Provincial-level aggregates may mask rural-urban differences within individual districts or schools",
            "Missing interim academic cycles (such as 2019–2020 if absent from the folder) appear as gaps in longitudinal charts rather than interpolated estimates",
            "All figures represent historical public reporting cycles and are intended for descriptive analysis rather than causal claims",
        ],
        "about_stack_title": "Platform & Attribution",
        "about_stack_body": "Built with Python, Streamlit, Pandas, and Plotly. Designed with bilingual English and Khmer support, neutral dark and light themes, and direct CSV export for reproducible research.",
    },
    "km": {
        "brand_sub": "ប្រព័ន្ធស្ថិតិអប់រំកម្ពុជា",
        "nav_overview": "ទិដ្ឋភាពទូទៅ",
        "nav_provincial": "ការវិភាគតាមខេត្ត",
        "nav_equity": "សមធម៌ និងគ្រូបង្រៀន",
        "nav_data": "តារាងទិន្នន័យ",
        "nav_about": "អំពីប្រព័ន្ធ",
        "coverage_label": "ទិន្នន័យដែលមាន",
        "coverage_cycle_one": "១ ឆ្នាំសិក្សា",
        "coverage_cycle_many": "{n} ឆ្នាំសិក្សា",
        "coverage_provs": "{n} រាជធានី-ខេត្ត · ទិន្នន័យក្រសួងអប់រំ",
        "all_years_opt": "គ្រប់ឆ្នាំសិក្សា ({span})",
        "theme_dark": "ងងឹត",
        "theme_light": "ភ្លឺ",
        "footer_left": "CAMEDUSTATS · ស្ថិតិអប់រំសាធារណៈកម្ពុជា",
        "footer_right": "ទិន្នន័យឆ្នាំសិក្សា៖ {span}",
        "overview_title": "ទិដ្ឋភាពទូទៅវិស័យអប់រំជាតិ",
        "overview_sub_all": "មធ្យមភាគប្រចាំឆ្នាំសរុបសម្រាប់ឆ្នាំសិក្សាទាំងអស់ ({span}) នៅគ្រប់ ២៥ រាជធានី-ខេត្ត",
        "overview_sub_one": "សូចនាករអប់រំសាធារណៈជាតិសម្រាប់ឆ្នាំសិក្សា {year} នៅគ្រប់ ២៥ រាជធានី-ខេត្ត",
        "kpi_enrol": "សិស្សសរុប",
        "kpi_enrol_avg": "សិស្សសរុបមធ្យមប្រចាំឆ្នាំ",
        "kpi_enrol_note": "នៅតាមសាលាចំនួន {schools}",
        "kpi_repeat": "អត្រាសិស្សត្រួតថ្នាក់",
        "kpi_repeat_avg": "អត្រាត្រួតថ្នាក់មធ្យម",
        "kpi_repeat_note": "សិស្សត្រួតថ្នាក់ {count} នាក់",
        "kpi_str": "សិស្សក្នុងគ្រូម្នាក់",
        "kpi_str_avg": "សិស្សក្នុងគ្រូម្នាក់មធ្យម",
        "kpi_str_note": "គ្រូបង្រៀនសរុប {teachers} នាក់",
        "kpi_dis": "សាលាជួបការលំបាក",
        "kpi_dis_avg": "សាលាលំបាកមធ្យមប្រចាំឆ្នាំ",
        "kpi_dis_note": "ថ្នាក់រៀននៅវត្ត {pagoda} ថ្នាក់",
        "map_sec": "ផែនទីស្ថិតិតាមរាជធានី-ខេត្ត",
        "map_desc": "ទំហំរង្វង់តំណាងឱ្យចំនួនសិស្ស និងរំកិលកណ្ដុរលើខេត្តណាមួយដើម្បីមើលព័ត៌មានលម្អិត",
        "map_metric_label": "សូចនាករលើផែនទី",
        "watchlist_sec": "បញ្ជីខេត្តអាទិភាព",
        "watchlist_desc": "ខេត្តទាំង ៥ ដែលមានសម្ពាធខ្ពស់លើអត្រាត្រួតថ្នាក់ និងបន្ទុកគ្រូបង្រៀន",
        "watchlist_sub": "ពិន្ទុសរុប (០–១០០) គណនាពីអត្រាត្រួតថ្នាក់ សិស្សក្នុងគ្រូម្នាក់ និងសាលាជួបការលំបាក",
        "trend_sec": "និន្នាការជាតិតាមឆ្នាំសិក្សា",
        "trend_desc": "ការប្រែប្រួលចំនួនសិស្ស អត្រាត្រួតថ្នាក់ និងសមាមាត្រសិស្សក្នុងគ្រូម្នាក់ឆ្លងកាត់ឆ្នាំសិក្សា",
        "chart_enrol_trend": "និន្នាការចំនួនសិស្សសរុបតាមឆ្នាំសិក្សា",
        "chart_dual_trend": "អត្រាត្រួតថ្នាក់ និងសិស្សក្នុងគ្រូម្នាក់តាមឆ្នាំ",
        "prov_title": "ការវិភាគតាមរាជធានី-ខេត្ត",
        "prov_sub": "ប្រៀបធៀបអត្រាសិស្សត្រួតថ្នាក់ បន្ទុកការងារគ្រូ និងនិន្នាការនៅគ្រប់ ២៥ រាជធានី-ខេត្ត",
        "quad_sec": "បន្ទុកគ្រូបង្រៀន ធៀបនឹង អត្រាសិស្សត្រួតថ្នាក់",
        "quad_desc": "រង្វង់នីមួយៗតំណាងឱ្យខេត្តមួយ រំកិលកណ្ដុរលើដើម្បីមើលតួលេខលម្អិត និងបន្ទាត់ដាច់ៗជាមធ្យមភាគជាតិ",
        "quad_title": "សិស្សក្នុងគ្រូម្នាក់ ធៀបនឹង អត្រាត្រួតថ្នាក់ ({period})",
        "nat_avg": "មធ្យមភាគជាតិ",
        "rank_rep_title": "អត្រាសិស្សត្រួតថ្នាក់តាមខេត្ត (%)",
        "rank_str_title": "សមាមាត្រសិស្សក្នុងគ្រូម្នាក់តាមខេត្ត",
        "prov_trend_sec": "ការប្រៀបធៀបនិន្នាការខេត្តតាមឆ្នាំ",
        "prov_trend_desc": "ជ្រើសរើសខេត្តរហូតដល់ ៦ ដើម្បីតាមដានការប្រែប្រួលឆ្លងកាត់ឆ្នាំសិក្សា",
        "select_indicator": "សូចនាករ",
        "select_provs": "ជ្រើសរើសខេត្តប្រៀបធៀប",
        "eq_title": "សមធម៌យេនឌ័រ និងបុគ្គលិកអប់រំ",
        "eq_sub": "សមាមាត្រសិស្សស្រី-ប្រុស អត្រាត្រួតថ្នាក់តាមភេទ គ្រូបង្រៀនស្រី និងស្ថានភាពសាលារៀន",
        "kpi_girl_enrol": "សិស្សស្រី",
        "kpi_girl_enrol_note": "សិស្សស្រីសរុប {count} នាក់",
        "kpi_boy_rep": "អត្រាសិស្សប្រុសត្រួតថ្នាក់",
        "kpi_boy_rep_note": "ធៀបនឹងសិស្សស្រី {girl_rate}",
        "kpi_fem_teach": "គ្រូបង្រៀនស្រី",
        "kpi_fem_teach_note": "គ្រូស្រីសរុប {count} នាក់",
        "kpi_class_size": "សិស្សមធ្យមក្នុងមួយថ្នាក់",
        "kpi_class_size_note": "ថ្នាក់រៀនសរុប {classes} ថ្នាក់",
        "chart_gender_rep": "អត្រាត្រួតថ្នាក់សិស្សប្រុស ធៀបនឹង សិស្សស្រី (%)",
        "chart_fem_teach": "ភាគរយគ្រូបង្រៀនស្រីតាមខេត្ត (%)",
        "chart_dis_top": "ខេត្តទាំង ១២ ដែលមានសាលាជួបការលំបាកច្រើនជាងគេ",
        "chart_pagoda_top": "ខេត្តទាំង ១២ ដែលមានថ្នាក់រៀននៅវត្តច្រើនជាងគេ",
        "male_label": "ប្រុស",
        "female_label": "ស្រី",
        "data_title": "តារាងទិន្នន័យ",
        "data_sub": "សូចនាករអប់រំសំខាន់ៗតាមរាជធានី-ខេត្ត សម្រាប់ស្វែងរក ច្រោះទិន្នន័យ និងទាញយកជាឯកសារ CSV",
        "search_prov": "ស្វែងរកខេត្ត",
        "search_placeholder": "វាយឈ្មោះខេត្តជាភាសាខ្មែរ ឬអង់គ្លេស...",
        "showing_rows": "កំពុងបង្ហាញ {shown} ក្នុងចំណោម {total} កំណត់ត្រា",
        "btn_download": "ទាញយកឯកសារ CSV",
        "col_year": "ឆ្នាំសិក្សា",
        "col_prov": "រាជធានី-ខេត្ត",
        "col_schools": "សាលារៀន",
        "col_dis": "សាលាលំបាក",
        "col_classes": "ថ្នាក់រៀន",
        "col_pagoda": "ថ្នាក់នៅវត្ត",
        "col_enrol": "សិស្សសរុប",
        "col_girl_pct": "សិស្សស្រី (%)",
        "col_rep_rate": "អត្រាត្រួតថ្នាក់ (%)",
        "col_teachers": "គ្រូបង្រៀន",
        "col_str": "សិស្ស/គ្រូ",
        "col_cls_size": "សិស្ស/ថ្នាក់",
        "ind_priority": "ពិន្ទុអាទិភាព (០–១០០)",
        "ind_rep": "អត្រាសិស្សត្រួតថ្នាក់ (%)",
        "ind_str": "សិស្សក្នុងគ្រូម្នាក់",
        "ind_dis_pct": "ភាគរយសាលាលំបាក (%)",
        "ind_enrol": "ចំនួនសិស្សសរុប",
        "ind_fem_teach": "ភាគរយគ្រូស្រី (%)",
        "tier_high": "អាទិភាពខ្ពស់",
        "tier_mod": "មធ្យម",
        "tier_low": "សម្ពាធទាប",
        "hover_enrol": "សិស្សសរុប",
        "hover_rep": "អត្រាត្រួតថ្នាក់",
        "hover_str": "សិស្សក្នុងគ្រូម្នាក់",
        "hover_dis": "សាលាជួបការលំបាក",
        "hover_cls": "សិស្សក្នុងមួយថ្នាក់",
        "about_title": "អំពីប្រព័ន្ធ CAMEDUSTATS",
        "about_sub": "ប្រព័ន្ធវិភាគស្ថិតិអប់រំសាធារណៈសម្រាប់ស្វែងយល់ពីស្ថានភាពអប់រំតាមរាជធានី-ខេត្តនៅកម្ពុជា",
        "about_goal_title": "គោលបំណងគម្រោង",
        "about_goal_body": "CAMEDUSTATS បំប្លែងទិន្នន័យស្ថិតិអប់រំសាធារណៈច្រើនឆ្នាំនៅកម្ពុជា ទៅជាសូចនាករប្រៀបធៀបតាមខេត្តដែលងាយយល់ និងងាយប្រើប្រាស់ ដើម្បីជួយនិស្សិត អ្នកស្រាវជ្រាវ និងអ្នករៀបចំផែនការអប់រំអាចកំណត់តំបន់មានអត្រាត្រួតថ្នាក់ខ្ពស់ កង្វះខាតគ្រូបង្រៀន គម្លាតយេនឌ័រ និងសាលាជួបការលំបាកនៅក្នុងវេទិកាតែមួយ",
        "about_data_title": "ប្រភពទិន្នន័យ និងវិសាលភាព",
        "about_data_items": [
            "ប្រភពគោល៖ ស្ថិតិ និងសូចនាករអប់រំសាធារណៈកម្ពុជា ចេញផ្សាយដោយក្រសួងអប់រំ យុវជន និងកីឡា",
            "វិសាលភាពភូមិសាស្ត្រ៖ គ្របដណ្ដប់ទាំង ២៥ រាជធានី-ខេត្ត នៃព្រះរាជាណាចក្រកម្ពុជា",
            "កាលបរិច្ឆេទទិន្នន័យ៖ រួមបញ្ចូលទិន្នន័យឆ្នាំសិក្សាពីឆ្នាំ ២០១៥–២០១៦ ដល់ ២០២០–២០២១ ដោយស្វ័យប្រវត្តិ",
            "ការសម្រួលទិន្នន័យ៖ កែតម្រូវឈ្មោះជួរឈរ អក្ខរាវិរុទ្ធឈ្មោះខេត្ត និងតម្លៃទទេរវាងឆ្នាំសិក្សាដោយស្វ័យប្រវត្តិ",
        ],
        "about_method_title": "សូចនាករសំខាន់ៗ និងវិធីសាស្ត្រគណនា",
        "about_method_items": [
            "អត្រាសិស្សត្រួតថ្នាក់ (%)៖ ចំនួនសិស្សត្រួតថ្នាក់ចែកនឹងសិស្សចុះឈ្មោះសរុប (t_repeat / t_enrol × 100)",
            "សិស្សក្នុងគ្រូម្នាក់៖ សមាមាត្រសិស្សសរុបធៀបនឹងចំនួនគ្រូបង្រៀនសកម្ម (t_enrol / t_teacher)",
            "សិស្សមធ្យមក្នុងមួយថ្នាក់៖ ចំនួនសិស្សសរុបចែកនឹងចំនួនថ្នាក់រៀនសរុប (t_enrol / no_class)",
            "ពិន្ទុអាទិភាព (០–១០០)៖ សន្ទស្សន៍រួមគណនាពីអត្រាត្រួតថ្នាក់ (៤០%) សិស្សក្នុងគ្រូម្នាក់ (៤០%) និងភាគរយសាលាលំបាក (២០%)",
            "ការបង្ហាញគ្រប់ឆ្នាំសិក្សា៖ ប្រើមធ្យមភាគប្រចាំឆ្នាំសម្រាប់ខេត្តនីមួយៗ ដើម្បីចៀសវាងការបូកជាន់ចំនួនសិស្សឆ្លងឆ្នាំ",
        ],
        "about_limits_title": "ដែនកំណត់ និងការប្រើប្រាស់ទិន្នន័យ",
        "about_limits_items": [
            "ទិន្នន័យកម្រិតខេត្តអាចមិនបង្ហាញភាពខុសគ្នាលម្អិតរវាងតំបន់ទីក្រុង និងជនបទនៅតាមស្រុក ឬសាលានីមួយៗឡើយ",
            "ឆ្នាំសិក្សាដែលមិនមានឯកសារក្នុងថតទិន្នន័យ (ឧទាហរណ៍ ២០១៩–២០២០) មិនត្រូវបានប៉ាន់ស្មានបំពេញបន្ថែមឡើយ",
            "តួលេខទាំងអស់ជាទិន្នន័យប្រវត្តិសាស្ត្រសម្រាប់ការវិភាគពិពណ៌នា និងការសិក្សាប្រៀបធៀបប៉ុណ្ណោះ",
        ],
        "about_stack_title": "បច្ចេកវិទ្យា និងការរៀបចំ",
        "about_stack_body": "អភិវឌ្ឍដោយប្រើ Python, Streamlit, Pandas និង Plotly ដោយគាំទ្រទាំងភាសាខ្មែរ និងភាសាអង់គ្លេស រចនាបថងងឹត និងភ្លឺ ព្រមទាំងអាចទាញយកទិន្នន័យជាឯកសារ CSV",
    },
}


def renderHtml(markup: str):
    cleaned = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def getThemeTokens(mode: str) -> dict:
    if mode == "dark":
        return {
            "bg": "#0F1115",
            "sidebar_bg": "#16181D",
            "surface": "#181B21",
            "surface_alt": "#20242C",
            "border": "#2A2E37",
            "text": "#F1F5F9",
            "muted": "#94A3B8",
            "accent": "#20BEFF",
            "accent_soft": "rgba(32, 190, 255, 0.14)",
            "btn_active_bg": "#252932",
            "btn_hover_bg": "#1F232B",
            "grid": "#242832",
            "land": "#1D212A",
            "ocean": "#11141B",
            "country_line": "#3A404E",
            "hover_bg": "#0B0D12",
            "hover_text": "#F8FAFC",
            "bar_primary": "#38BDF8",
            "bar_secondary": "#F59E0B",
            "bar_risk": "#FB7185",
            "bar_teal": "#2DD4BF",
            "bar_purple": "#A78BFA",
            "risk_high": "#FB7185",
            "risk_high_bg": "rgba(244, 63, 94, 0.16)",
            "risk_high_border": "rgba(244, 63, 94, 0.38)",
            "risk_mod": "#FBBF24",
            "risk_mod_bg": "rgba(245, 158, 11, 0.15)",
            "risk_mod_border": "rgba(245, 158, 11, 0.36)",
            "risk_low": "#34D399",
            "risk_low_bg": "rgba(16, 185, 129, 0.15)",
            "risk_low_border": "rgba(16, 185, 129, 0.35)",
        }
    return {
        "bg": "#F8FAFC",
        "sidebar_bg": "#FFFFFF",
        "surface": "#FFFFFF",
        "surface_alt": "#F1F5F9",
        "border": "#E2E8F0",
        "text": "#0F172A",
        "muted": "#64748B",
        "accent": "#0284C7",
        "accent_soft": "rgba(2, 132, 199, 0.10)",
        "btn_active_bg": "#EEF2F6",
        "btn_hover_bg": "#F1F5F9",
        "grid": "#E8EEF4",
        "land": "#F1F5F9",
        "ocean": "#E0F2FE",
        "country_line": "#94A3B8",
        "hover_bg": "#0F172A",
        "hover_text": "#FFFFFF",
        "bar_primary": "#0284C7",
        "bar_secondary": "#D97706",
        "bar_risk": "#E11D48",
        "bar_teal": "#0D9488",
        "bar_purple": "#7C3AED",
        "risk_high": "#BE123C",
        "risk_high_bg": "#FFE4E6",
        "risk_high_border": "#FECDD3",
        "risk_mod": "#B45309",
        "risk_mod_bg": "#FEF3C7",
        "risk_mod_border": "#FDE68A",
        "risk_low": "#047857",
        "risk_low_bg": "#D1FAE5",
        "risk_low_border": "#A7F3D0",
    }


def applyThemeAndCss(mode: str):
    tk = getThemeTokens(mode)
    baseCss = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.exists() else ""
    baseCss = re.sub(r"@import\s+url\([^)]*\);\s*", "", baseCss)
    compactBase = "\n".join(line.strip() for line in baseCss.splitlines() if line.strip())

    fontImport = (
        '@import url("https://fonts.googleapis.com/css2?'
        'family=Manrope:wght@400;500;600;700;800&'
        'family=Noto+Sans+Khmer:wght@400;500;600;700;800&display=swap");'
    )
    rootVars = (
        ":root {"
        f"--bg:{tk['bg']};"
        f"--sidebar-bg:{tk['sidebar_bg']};"
        f"--surface:{tk['surface']};"
        f"--surface-alt:{tk['surface_alt']};"
        f"--border:{tk['border']};"
        f"--text:{tk['text']};"
        f"--muted:{tk['muted']};"
        f"--accent:{tk['accent']};"
        f"--accent-soft:{tk['accent_soft']};"
        f"--btn-active-bg:{tk['btn_active_bg']};"
        f"--btn-hover-bg:{tk['btn_hover_bg']};"
        f"--risk-high:{tk['risk_high']};"
        f"--risk-high-bg:{tk['risk_high_bg']};"
        f"--risk-high-border:{tk['risk_high_border']};"
        f"--risk-mod:{tk['risk_mod']};"
        f"--risk-mod-bg:{tk['risk_mod_bg']};"
        f"--risk-mod-border:{tk['risk_mod_border']};"
        f"--risk-low:{tk['risk_low']};"
        f"--risk-low-bg:{tk['risk_low_bg']};"
        f"--risk-low-border:{tk['risk_low_border']};"
        "}"
    )

    st.markdown(
        f"<style>\n{fontImport}\n{rootVars}\n{compactBase}\n</style>",
        unsafe_allow_html=True,
    )


# ============================================================
# DATA LOADER & MULTI-YEAR AGGREGATION
# ============================================================

def extractYear(filename: str) -> str:
    match = re.search(r"(20\d{2})\s*[-–_]\s*(20\d{2})", filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return Path(filename).stem


def minMaxNorm(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0 or pd.isna(span):
        return pd.Series(0.0, index=series.index)
    return (series - series.min()) / span


def computeDerivedFields(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["male_enrol"] = (d["t_enrol"] - d["enrol_girl"]).clip(lower=0)
    d["male_repeat"] = (d["t_repeat"] - d["repeat_gir"]).clip(lower=0)
    d["repeater_rate"] = (d["t_repeat"] / d["t_enrol"].replace(0, pd.NA) * 100).fillna(0)
    d["female_repeat_rate"] = (d["repeat_gir"] / d["enrol_girl"].replace(0, pd.NA) * 100).fillna(0)
    d["male_repeat_rate"] = (d["male_repeat"] / d["male_enrol"].replace(0, pd.NA) * 100).fillna(0)
    d["female_enrol_pct"] = (d["enrol_girl"] / d["t_enrol"].replace(0, pd.NA) * 100).fillna(0)
    d["female_teacher_pct"] = (d["teacher_f"] / d["t_teacher"].replace(0, pd.NA) * 100).fillna(0)
    d["student_teacher_ratio"] = (d["t_enrol"] / d["t_teacher"].replace(0, pd.NA)).fillna(0)
    d["students_per_class"] = (d["t_enrol"] / d["no_class"].replace(0, pd.NA)).fillna(0)
    d["dis_school_pct"] = (d["dis_school"] / d["no_school"].replace(0, pd.NA) * 100).fillna(0)
    d["lat"] = d["prov_en"].map(lambda p: PROVINCE_COORDS.get(p, (None, None))[0])
    d["lon"] = d["prov_en"].map(lambda p: PROVINCE_COORDS.get(p, (None, None))[1])
    d["priority_score"] = (
        0.40 * minMaxNorm(d["repeater_rate"])
        + 0.40 * minMaxNorm(d["student_teacher_ratio"])
        + 0.20 * minMaxNorm(d["dis_school_pct"])
    ) * 100
    d["tier_key"] = pd.cut(
        d["priority_score"],
        bins=[-1, 35, 55, 101],
        labels=["tier_low", "tier_mod", "tier_high"],
    ).astype(str)
    return d


@st.cache_data
def loadAllDatasets(baseDirStr: str) -> pd.DataFrame:
    baseDir = Path(baseDirStr)
    candidates = []
    for folder in [baseDir, baseDir / "data"]:
        if folder.exists():
            candidates.extend(sorted(folder.glob("*.csv")))

    filesByYear = {}
    for csvPath in candidates:
        lower = csvPath.name.lower()
        if "cambodia" in lower or "education" in lower or re.search(r"20\d{2}-20\d{2}", lower):
            yr = extractYear(csvPath.name)
            if yr not in filesByYear or not re.search(r"_\d+\.csv$", lower):
                filesByYear[yr] = csvPath

    frames = []
    for yr in sorted(filesByYear.keys()):
        raw = pd.read_csv(filesByYear[yr])
        for badCol, goodCol in COLUMN_ALIASES.items():
            if badCol in raw.columns and goodCol not in raw.columns:
                raw = raw.rename(columns={badCol: goodCol})

        if "prov_en" not in raw.columns:
            continue

        raw["prov_en"] = raw["prov_en"].astype(str).str.strip().replace(PROVINCE_ALIASES)
        raw["prov_kh"] = (
            raw["prov_kh"].fillna("").astype(str).str.strip()
            if "prov_kh" in raw.columns
            else raw["prov_en"]
        )

        for col in ESSENTIAL_NUMERIC:
            if col not in raw.columns:
                raw[col] = 0.0
            raw[col] = pd.to_numeric(raw[col], errors="coerce").fillna(0.0)

        raw["academic_year"] = yr
        frames.append(raw[["academic_year", "prov_en", "prov_kh"] + ESSENTIAL_NUMERIC])

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    scored = [computeDerivedFields(grp) for _, grp in combined.groupby("academic_year", sort=False)]
    return pd.concat(scored, ignore_index=True)


def getProvincialSnapshot(df: pd.DataFrame, selectedPeriod: str, allYearsLabel: str) -> pd.DataFrame:
    if selectedPeriod == allYearsLabel:
        avgDf = df.groupby(["prov_en", "prov_kh"], as_index=False)[ESSENTIAL_NUMERIC].mean()
        return computeDerivedFields(avgDf)
    return df[df["academic_year"] == selectedPeriod].copy()


def computeYearlySummary(data: pd.DataFrame) -> pd.DataFrame:
    agg = data.groupby("academic_year", as_index=False)[ESSENTIAL_NUMERIC].sum()
    agg["repeater_rate"] = agg["t_repeat"] / agg["t_enrol"].replace(0, pd.NA) * 100
    agg["student_teacher_ratio"] = agg["t_enrol"] / agg["t_teacher"].replace(0, pd.NA)
    agg["students_per_class"] = agg["t_enrol"] / agg["no_class"].replace(0, pd.NA)
    agg["female_enrol_pct"] = agg["enrol_girl"] / agg["t_enrol"].replace(0, pd.NA) * 100
    agg["female_teacher_pct"] = agg["teacher_f"] / agg["t_teacher"].replace(0, pd.NA) * 100
    return agg.sort_values("academic_year").reset_index(drop=True)


# ============================================================
# FORMATTERS & UI COMPONENTS
# ============================================================

def fmtNum(val):
    try:
        return f"{int(round(float(val))):,}"
    except (ValueError, TypeError):
        return "—"


def fmtPct(val):
    try:
        return f"{float(val):.1f}%"
    except (ValueError, TypeError):
        return "—"


def fmtDec(val):
    try:
        return f"{float(val):.1f}"
    except (ValueError, TypeError):
        return "—"


def pageHeader(title, subtitle):
    renderHtml(
        f"""
        <div class="page-heading">
            <div class="page-title">{html.escape(title)}</div>
            <div class="page-subtitle">{html.escape(subtitle)}</div>
        </div>
        """
    )


def sectionTitle(title, description=None):
    desc = f'<div class="section-description">{html.escape(description)}</div>' if description else ""
    renderHtml(
        f"""
        <div class="section-heading">
            <div class="section-title">{html.escape(title)}</div>
            {desc}
        </div>
        """
    )


def metricCard(label, value, note):
    renderHtml(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-note">{html.escape(note)}</div>
        </div>
        """
    )


def styleChart(fig, tk: dict, height=420, isHorizontalBar=False, hasRightAxis=False):
    rightMargin = 82 if hasRightAxis else 42
    topMargin = 84 if hasRightAxis else 58
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=rightMargin, t=topMargin, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=tk["text"], size=13),
        title=dict(
            font=dict(family=FONT_FAMILY, size=17, color=tk["text"]),
            x=0.01,
            xanchor="left",
            y=0.96,
            yanchor="top",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left" if hasRightAxis else "right",
            x=0.0 if hasRightAxis else 1,
            font=dict(family=FONT_FAMILY, size=12.5, color=tk["muted"]),
            title_text="",
        ),
        hoverlabel=dict(
            bgcolor=tk["hover_bg"],
            bordercolor=tk["border"],
            font=dict(color=tk["hover_text"], size=13, family=FONT_FAMILY),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=tk["grid"],
        zeroline=False,
        linecolor=tk["border"],
        automargin=True,
        tickfont=dict(family=FONT_FAMILY, size=12.5, color=tk["muted"]),
        title_font=dict(family=FONT_FAMILY, size=13, color=tk["muted"]),
    )
    fig.update_yaxes(
        showgrid=not isHorizontalBar,
        gridcolor=tk["grid"],
        zeroline=False,
        linecolor=tk["border"],
        automargin=True,
        tickfont=dict(family=FONT_FAMILY, size=12.5, color=tk["muted"]),
        title_font=dict(family=FONT_FAMILY, size=13, color=tk["muted"]),
        ticksuffix="  " if isHorizontalBar else "",
    )
    if hasRightAxis:
        y2Title = (
            fig.layout.yaxis2.title.text
            if fig.layout.yaxis2 and fig.layout.yaxis2.title
            else ""
        )
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showgrid=False,
                zeroline=False,
                linecolor=tk["border"],
                automargin=True,
                tickformat=".1f",
                tickfont=dict(family=FONT_FAMILY, size=12.5, color=tk["muted"]),
                title=dict(
                    text=y2Title,
                    font=dict(family=FONT_FAMILY, size=13, color=tk["muted"]),
                    standoff=14,
                ),
            )
        )
    if isHorizontalBar:
        fig.update_layout(bargap=0.30)
    return fig


def showChart(fig, tk: dict, key=None, height=420, isHorizontalBar=False, hasRightAxis=False):
    st.plotly_chart(
        styleChart(
            fig,
            tk,
            height=height,
            isHorizontalBar=isHorizontalBar,
            hasRightAxis=hasRightAxis,
        ),
        use_container_width=True,
        config={"displayModeBar": False},
        key=key,
    )


# ============================================================
# INITIALIZE STATE & LOAD DATA
# ============================================================

if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "dark"
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "overview"

fullDf = loadAllDatasets(str(BASE_DIR))
if fullDf.empty:
    st.error("No Cambodia education CSV files found in the app folder.")
    st.stop()

AVAILABLE_YEARS = sorted(fullDf["academic_year"].unique().tolist())
SPAN_LABEL = (
    AVAILABLE_YEARS[0]
    if len(AVAILABLE_YEARS) == 1
    else f"{AVAILABLE_YEARS[0][:4]}–{AVAILABLE_YEARS[-1][-4:]}"
)
SPAN_FULL = (
    AVAILABLE_YEARS[0]
    if len(AVAILABLE_YEARS) == 1
    else f"{AVAILABLE_YEARS[0]} – {AVAILABLE_YEARS[-1]}"
)

applyThemeAndCss(st.session_state["theme_mode"])
tk = getThemeTokens(st.session_state["theme_mode"])
t = TEXT[st.session_state["lang"]]


# ============================================================
# SIDEBAR — CLEAN TEXT NAVIGATION + BOTTOM LOADED DATA BOX
# ============================================================

def setPage(pageKey: str):
    st.session_state["active_page"] = pageKey


NAV_PAGES = [
    ("overview", t["nav_overview"]),
    ("provincial", t["nav_provincial"]),
    ("equity", t["nav_equity"]),
    ("data", t["nav_data"]),
    ("about", t["nav_about"]),
]

with st.sidebar:
    renderHtml(
        f"""
        <div class="brand-header">
            <div class="brand-name">CAMEDUSTATS</div>
            <div class="brand-sub">{html.escape(t['brand_sub'])}</div>
        </div>
        <div class="sidebar-divider"></div>
        """
    )

    for pageKey, label in NAV_PAGES:
        isActive = st.session_state["active_page"] == pageKey
        st.button(
            label,
            key=f"nav_{pageKey}",
            use_container_width=True,
            type="primary" if isActive else "secondary",
            on_click=setPage,
            args=(pageKey,),
        )

    cycleText = (
        t["coverage_cycle_one"]
        if len(AVAILABLE_YEARS) == 1
        else t["coverage_cycle_many"].format(n=len(AVAILABLE_YEARS))
    )

    renderHtml(
        f"""
        <div class="sidebar-bottom-card">
            <div class="sidebar-info-label">{html.escape(t['coverage_label'])}</div>
            <div class="sidebar-info-value">{html.escape(cycleText)}</div>
            <div class="sidebar-info-small">{html.escape(SPAN_FULL)}<br>{html.escape(t['coverage_provs'].format(n=fullDf['prov_en'].nunique()))}</div>
        </div>
        """
    )


# ============================================================
# TOP-RIGHT COMPACT UTILITY CONTROLS (YEAR FILTER · LANGUAGE · THEME)
# ============================================================

allYearsOpt = t["all_years_opt"].format(span=SPAN_LABEL)
yearChoices = [allYearsOpt] + AVAILABLE_YEARS if len(AVAILABLE_YEARS) > 1 else AVAILABLE_YEARS

if "period_idx" not in st.session_state or st.session_state["period_idx"] >= len(yearChoices):
    st.session_state["period_idx"] = 0

topSpacer, topYear, topLang, topTheme = st.columns([4.4, 2.1, 1.5, 1.1])

with topYear:
    selectedPeriod = st.selectbox(
        "Year",
        yearChoices,
        index=st.session_state["period_idx"],
        label_visibility="collapsed",
        key="top_year_filter",
    )
    st.session_state["period_idx"] = yearChoices.index(selectedPeriod)

with topLang:
    langDisplayMap = {"en": "🌐  English", "km": "🌐  ភាសាខ្មែរ"}
    langOptions = ["en", "km"]
    pickedLang = st.selectbox(
        "Language",
        langOptions,
        index=langOptions.index(st.session_state["lang"]),
        format_func=lambda code: langDisplayMap[code],
        label_visibility="collapsed",
        key="top_lang_dropdown",
    )
    if pickedLang != st.session_state["lang"]:
        st.session_state["lang"] = pickedLang
        st.rerun()

with topTheme:
    themeLabels = {"dark": t["theme_dark"], "light": t["theme_light"]}
    themeOpts = ["dark", "light"]
    pickedTheme = st.selectbox(
        "Theme",
        themeOpts,
        index=themeOpts.index(st.session_state["theme_mode"]),
        format_func=lambda m: themeLabels[m],
        label_visibility="collapsed",
        key="top_theme_dropdown",
    )
    if pickedTheme != st.session_state["theme_mode"]:
        st.session_state["theme_mode"] = pickedTheme
        st.rerun()

isAllYears = selectedPeriod == allYearsOpt

fullDf["prov_display"] = fullDf["prov_kh"] if st.session_state["lang"] == "km" else fullDf["prov_en"]
fullDf["tier_display"] = fullDf["tier_key"].map(lambda k: t[k])

snapDf = getProvincialSnapshot(fullDf, selectedPeriod, allYearsOpt)
snapDf["prov_display"] = snapDf["prov_kh"] if st.session_state["lang"] == "km" else snapDf["prov_en"]
snapDf["tier_display"] = snapDf["tier_key"].map(lambda k: t[k])

yearlySummary = computeYearlySummary(fullDf)

totEnrol = snapDf["t_enrol"].sum()
totSchools = snapDf["no_school"].sum()
totClasses = snapDf["no_class"].sum()
totRepeat = snapDf["t_repeat"].sum()
totTeachers = snapDf["t_teacher"].sum()
totDis = snapDf["dis_school"].sum()
totPagoda = snapDf["clas_pagod"].sum()
natRepRate = totRepeat / totEnrol * 100 if totEnrol else 0
natStr = totEnrol / totTeachers if totTeachers else 0
natClassSize = totEnrol / totClasses if totClasses else 0

activePage = st.session_state["active_page"]


# ============================================================
# PAGE 1: OVERVIEW
# ============================================================

if activePage == "overview":
    subText = (
        t["overview_sub_all"].format(span=SPAN_FULL)
        if isAllYears
        else t["overview_sub_one"].format(year=selectedPeriod)
    )
    pageHeader(t["overview_title"], subText)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metricCard(
            t["kpi_enrol_avg"] if isAllYears else t["kpi_enrol"],
            fmtNum(totEnrol),
            t["kpi_enrol_note"].format(schools=fmtNum(totSchools)),
        )
    with c2:
        metricCard(
            t["kpi_repeat_avg"] if isAllYears else t["kpi_repeat"],
            fmtPct(natRepRate),
            t["kpi_repeat_note"].format(count=fmtNum(totRepeat)),
        )
    with c3:
        metricCard(
            t["kpi_str_avg"] if isAllYears else t["kpi_str"],
            fmtDec(natStr),
            t["kpi_str_note"].format(teachers=fmtNum(totTeachers)),
        )
    with c4:
        metricCard(
            t["kpi_dis_avg"] if isAllYears else t["kpi_dis"],
            fmtNum(totDis),
            t["kpi_dis_note"].format(pagoda=fmtNum(totPagoda)),
        )

    renderHtml("<div class='spacer-12'></div>")

    leftCol, rightCol = st.columns([1.45, 1])

    with leftCol:
        sectionTitle(t["map_sec"], t["map_desc"])
        mapMetric = st.selectbox(
            t["map_metric_label"],
            [
                ("priority_score", t["ind_priority"], "YlOrRd"),
                ("repeater_rate", t["ind_rep"], "Reds"),
                ("student_teacher_ratio", t["ind_str"], "Blues"),
                ("dis_school_pct", t["ind_dis_pct"], "OrRd"),
            ],
            format_func=lambda x: x[1],
            key="ov_map_metric",
        )
        mapFig = px.scatter_geo(
            snapDf,
            lat="lat",
            lon="lon",
            size="t_enrol",
            color=mapMetric[0],
            hover_name="prov_display",
            custom_data=["t_enrol", "repeater_rate", "student_teacher_ratio", "dis_school"],
            size_max=34,
            color_continuous_scale=mapMetric[2],
            labels={mapMetric[0]: mapMetric[1]},
        )
        mapFig.update_traces(
            marker=dict(line=dict(width=1.2, color=tk["bg"]), opacity=0.92),
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                f"{t['hover_enrol']}: %{{customdata[0]:,.0f}}<br>"
                f"{t['hover_rep']}: %{{customdata[1]:.1f}}%<br>"
                f"{t['hover_str']}: %{{customdata[2]:.1f}}<br>"
                f"{t['hover_dis']}: %{{customdata[3]:,.0f}}<extra></extra>"
            ),
        )
        mapFig.update_geos(
            resolution=50,
            showcountries=True,
            countrycolor=tk["country_line"],
            showland=True,
            landcolor=tk["land"],
            showocean=True,
            oceancolor=tk["ocean"],
            showcoastlines=True,
            coastlinecolor=tk["country_line"],
            lataxis_range=[9.8, 14.9],
            lonaxis_range=[102.0, 108.0],
            bgcolor="rgba(0,0,0,0)",
        )
        mapFig.update_layout(margin=dict(l=8, r=8, t=18, b=8))
        showChart(mapFig, tk, key="ov_map", height=430)

    with rightCol:
        sectionTitle(t["watchlist_sec"], t["watchlist_desc"])
        topFive = snapDf.sort_values("priority_score", ascending=False).head(5)
        rowsHtml = ""
        for _, row in topFive.iterrows():
            scoreVal = float(row["priority_score"])
            if scoreVal >= 55:
                lvlCls, lvlText = "risk-high", t["tier_high"]
            elif scoreVal >= 35:
                lvlCls, lvlText = "risk-mod", t["tier_mod"]
            else:
                lvlCls, lvlText = "risk-low", t["tier_low"]

            rowsHtml += (
                f"<div class='dataset-stat {lvlCls}'>"
                f"<div class='stat-info'>"
                f"<div class='stat-title-row'>"
                f"<span class='risk-dot {lvlCls}'></span>"
                f"<span class='stat-prov'>{html.escape(row['prov_display'])}</span>"
                f"</div>"
                f"<div class='stat-sub'>{fmtPct(row['repeater_rate'])} · {fmtDec(row['student_teacher_ratio'])} S/T · {fmtNum(row['dis_school'])} {html.escape(t['col_dis'])}</div>"
                f"</div>"
                f"<div class='score-wrap'>"
                f"<span class='score-pill {lvlCls}'>{scoreVal:.1f}</span>"
                f"<span class='risk-tag {lvlCls}'>{html.escape(lvlText)}</span>"
                f"</div>"
                f"</div>"
            )

        renderHtml(
            f"""
            <div class="dataset-panel">
                <div class="dataset-panel-subtitle">{html.escape(t['watchlist_sub'])}</div>
                {rowsHtml}
            </div>
            """
        )

    if len(AVAILABLE_YEARS) >= 2:
        renderHtml("<div class='spacer-12'></div>")
        sectionTitle(t["trend_sec"], t["trend_desc"])
        tr1, tr2 = st.columns(2)
        with tr1:
            fig = px.area(
                yearlySummary,
                x="academic_year",
                y="t_enrol",
                markers=True,
                title=t["chart_enrol_trend"],
                labels={"academic_year": t["col_year"], "t_enrol": t["col_enrol"]},
                color_discrete_sequence=[tk["bar_primary"]],
            )
            fig.update_traces(line=dict(width=2.8), fillcolor="rgba(56, 189, 248, 0.12)")
            showChart(fig, tk, key="ov_enrol_trend", height=350)
        with tr2:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=yearlySummary["academic_year"],
                    y=yearlySummary["repeater_rate"],
                    name=t["col_rep_rate"],
                    mode="lines+markers",
                    line=dict(color=tk["bar_risk"], width=2.8),
                    marker=dict(size=7),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=yearlySummary["academic_year"],
                    y=yearlySummary["student_teacher_ratio"],
                    name=t["col_str"],
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(color=tk["bar_secondary"], width=2.8, dash="dot"),
                    marker=dict(size=7),
                )
            )
            fig.update_layout(
                title=t["chart_dual_trend"],
                yaxis=dict(title=t["col_rep_rate"], showgrid=True, gridcolor=tk["grid"]),
                yaxis2=dict(title=t["col_str"], overlaying="y", side="right", showgrid=False),
            )
            showChart(fig, tk, key="ov_dual_trend", height=350)


# ============================================================
# PAGE 2: PROVINCIAL INSIGHTS
# ============================================================

elif activePage == "provincial":
    pageHeader(t["prov_title"], t["prov_sub"])
    sectionTitle(t["quad_sec"], t["quad_desc"])

    quadFig = px.scatter(
        snapDf,
        x="student_teacher_ratio",
        y="repeater_rate",
        size="t_enrol",
        color="tier_display",
        hover_name="prov_display",
        size_max=40,
        color_discrete_map={
            t["tier_high"]: tk["bar_risk"],
            t["tier_mod"]: tk["bar_secondary"],
            t["tier_low"]: tk["bar_teal"],
        },
        labels={
            "student_teacher_ratio": t["ind_str"],
            "repeater_rate": t["ind_rep"],
            "tier_display": "",
        },
        title=t["quad_title"].format(period=selectedPeriod),
        custom_data=["t_enrol", "dis_school", "students_per_class"],
    )
    quadFig.update_traces(
        marker=dict(line=dict(width=1.2, color=tk["bg"]), opacity=0.9),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            f"{t['hover_str']}: %{{x:.1f}}<br>"
            f"{t['hover_rep']}: %{{y:.1f}}%<br>"
            f"{t['hover_enrol']}: %{{customdata[0]:,.0f}}<br>"
            f"{t['hover_cls']}: %{{customdata[2]:.1f}}<br>"
            f"{t['hover_dis']}: %{{customdata[1]:,.0f}}<extra></extra>"
        ),
    )

    outliers = {
        snapDf["repeater_rate"].idxmax(),
        snapDf["student_teacher_ratio"].idxmax(),
        snapDf["priority_score"].idxmax(),
    }
    for idx in outliers:
        r = snapDf.loc[idx]
        quadFig.add_annotation(
            x=r["student_teacher_ratio"],
            y=r["repeater_rate"],
            text=r["prov_display"],
            showarrow=True,
            arrowhead=0,
            ax=0,
            ay=-28,
            font=dict(family=FONT_FAMILY, size=12, color=tk["text"]),
            bgcolor=tk["surface"],
            bordercolor=tk["border"],
            borderpad=4,
        )

    quadFig.add_vline(
        x=natStr,
        line_dash="dash",
        line_color=tk["muted"],
        annotation_text=f"{t['nat_avg']} ({natStr:.1f})",
        annotation_position="top right",
        annotation_font=dict(color=tk["muted"], family=FONT_FAMILY, size=12),
    )
    quadFig.add_hline(
        y=natRepRate,
        line_dash="dash",
        line_color=tk["muted"],
        annotation_text=f"{t['nat_avg']} ({natRepRate:.1f}%)",
        annotation_position="bottom right",
        annotation_font=dict(color=tk["muted"], family=FONT_FAMILY, size=12),
    )
    showChart(quadFig, tk, key="prov_quad", height=480)

    a, b = st.columns(2)
    with a:
        d = snapDf.sort_values("repeater_rate", ascending=True)
        fig = px.bar(
            d,
            x="repeater_rate",
            y="prov_display",
            orientation="h",
            title=t["rank_rep_title"],
            labels={"repeater_rate": t["col_rep_rate"], "prov_display": ""},
            color_discrete_sequence=[tk["bar_risk"]],
        )
        fig.add_vline(x=natRepRate, line_dash="dash", line_color=tk["muted"])
        showChart(fig, tk, key="prov_rep_rank", height=740, isHorizontalBar=True)

    with b:
        d = snapDf.sort_values("student_teacher_ratio", ascending=True)
        fig = px.bar(
            d,
            x="student_teacher_ratio",
            y="prov_display",
            orientation="h",
            title=t["rank_str_title"],
            labels={"student_teacher_ratio": t["col_str"], "prov_display": ""},
            color_discrete_sequence=[tk["bar_primary"]],
        )
        fig.add_vline(x=natStr, line_dash="dash", line_color=tk["muted"])
        showChart(fig, tk, key="prov_str_rank", height=740, isHorizontalBar=True)

    if len(AVAILABLE_YEARS) >= 2:
        sectionTitle(t["prov_trend_sec"], t["prov_trend_desc"])
        p1, p2 = st.columns([1, 2])
        with p1:
            indChoice = st.selectbox(
                t["select_indicator"],
                [
                    ("repeater_rate", t["ind_rep"]),
                    ("student_teacher_ratio", t["ind_str"]),
                    ("t_enrol", t["ind_enrol"]),
                    ("dis_school_pct", t["ind_dis_pct"]),
                ],
                format_func=lambda x: x[1],
                key="prov_trend_ind",
            )
        with p2:
            allProvNames = sorted(fullDf["prov_display"].unique().tolist())
            defaultProvs = snapDf.sort_values("priority_score", ascending=False)["prov_display"].head(4).tolist()
            selectedProvs = st.multiselect(
                t["select_provs"],
                allProvNames,
                default=defaultProvs,
                max_selections=6,
                key="prov_trend_list",
            )
        if selectedProvs:
            trDf = fullDf[fullDf["prov_display"].isin(selectedProvs)].sort_values("academic_year")
            fig = px.line(
                trDf,
                x="academic_year",
                y=indChoice[0],
                color="prov_display",
                markers=True,
                labels={"academic_year": t["col_year"], indChoice[0]: indChoice[1], "prov_display": ""},
            )
            fig.update_traces(line=dict(width=2.8), marker=dict(size=7))
            showChart(fig, tk, key="prov_trend_chart", height=400)


# ============================================================
# PAGE 3: EQUITY & WORKFORCE
# ============================================================

elif activePage == "equity":
    pageHeader(t["eq_title"], t["eq_sub"])

    girls = snapDf["enrol_girl"].sum()
    boys = totEnrol - girls
    girlRepRate = snapDf["repeat_gir"].sum() / girls * 100 if girls else 0
    boyRepRate = (totRepeat - snapDf["repeat_gir"].sum()) / boys * 100 if boys else 0
    femTeachers = snapDf["teacher_f"].sum()
    femEnrolPct = girls / totEnrol * 100 if totEnrol else 0
    femTeachPct = femTeachers / totTeachers * 100 if totTeachers else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metricCard(t["kpi_girl_enrol"], fmtPct(femEnrolPct), t["kpi_girl_enrol_note"].format(count=fmtNum(girls)))
    with k2:
        metricCard(t["kpi_boy_rep"], fmtPct(boyRepRate), t["kpi_boy_rep_note"].format(girl_rate=fmtPct(girlRepRate)))
    with k3:
        metricCard(t["kpi_fem_teach"], fmtPct(femTeachPct), t["kpi_fem_teach_note"].format(count=fmtNum(femTeachers)))
    with k4:
        metricCard(t["kpi_class_size"], fmtDec(natClassSize), t["kpi_class_size_note"].format(classes=fmtNum(totClasses)))

    renderHtml("<div class='spacer-12'></div>")

    a, b = st.columns(2)
    with a:
        d = snapDf.sort_values("male_repeat_rate", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=d["prov_display"], x=d["female_repeat_rate"], name=t["female_label"], orientation="h", marker_color=tk["bar_purple"]))
        fig.add_trace(go.Bar(y=d["prov_display"], x=d["male_repeat_rate"], name=t["male_label"], orientation="h", marker_color=tk["bar_risk"]))
        fig.update_layout(barmode="group", title=t["chart_gender_rep"], xaxis_title=t["col_rep_rate"])
        showChart(fig, tk, key="eq_gender_rep", height=760, isHorizontalBar=True)

    with b:
        d = snapDf.sort_values("female_teacher_pct", ascending=True)
        fig = px.bar(
            d,
            x="female_teacher_pct",
            y="prov_display",
            orientation="h",
            title=t["chart_fem_teach"],
            labels={"female_teacher_pct": t["ind_fem_teach"], "prov_display": ""},
            color_discrete_sequence=[tk["bar_teal"]],
        )
        fig.add_vline(x=50.0, line_dash="dash", line_color=tk["muted"])
        showChart(fig, tk, key="eq_fem_teach", height=760, isHorizontalBar=True)

    c, dCol = st.columns(2)
    with c:
        topDis = snapDf.sort_values("dis_school", ascending=True).tail(12)
        fig = px.bar(
            topDis,
            x="dis_school",
            y="prov_display",
            orientation="h",
            title=t["chart_dis_top"],
            labels={"dis_school": t["col_dis"], "prov_display": ""},
            color_discrete_sequence=[tk["bar_risk"]],
        )
        showChart(fig, tk, key="eq_dis_top", height=460, isHorizontalBar=True)

    with dCol:
        topPag = snapDf.sort_values("clas_pagod", ascending=True).tail(12)
        fig = px.bar(
            topPag,
            x="clas_pagod",
            y="prov_display",
            orientation="h",
            title=t["chart_pagoda_top"],
            labels={"clas_pagod": t["col_pagoda"], "prov_display": ""},
            color_discrete_sequence=[tk["bar_secondary"]],
        )
        showChart(fig, tk, key="eq_pagoda_top", height=460, isHorizontalBar=True)


# ============================================================
# PAGE 4: DATA TABLE
# ============================================================

elif activePage == "data":
    pageHeader(t["data_title"], t["data_sub"])

    query = st.text_input(t["search_prov"], placeholder=t["search_placeholder"], key="tbl_search")

    view = fullDf.copy() if isAllYears else fullDf[fullDf["academic_year"] == selectedPeriod].copy()
    if query:
        view = view[
            view["prov_en"].str.contains(query, case=False, na=False)
            | view["prov_kh"].str.contains(query, case=False, na=False)
        ]

    essentialCols = [
        "academic_year",
        "prov_display",
        "no_school",
        "dis_school",
        "no_class",
        "t_enrol",
        "female_enrol_pct",
        "repeater_rate",
        "t_teacher",
        "student_teacher_ratio",
        "students_per_class",
    ]
    outDf = view[essentialCols].copy()
    for col in ["female_enrol_pct", "repeater_rate", "student_teacher_ratio", "students_per_class"]:
        outDf[col] = outDf[col].round(1)
    for col in ["no_school", "dis_school", "no_class", "t_enrol", "t_teacher"]:
        outDf[col] = outDf[col].round(0).astype(int)

    outDf = outDf.rename(
        columns={
            "academic_year": t["col_year"],
            "prov_display": t["col_prov"],
            "no_school": t["col_schools"],
            "dis_school": t["col_dis"],
            "no_class": t["col_classes"],
            "t_enrol": t["col_enrol"],
            "female_enrol_pct": t["col_girl_pct"],
            "repeater_rate": t["col_rep_rate"],
            "t_teacher": t["col_teachers"],
            "student_teacher_ratio": t["col_str"],
            "students_per_class": t["col_cls_size"],
        }
    )

    renderHtml(
        f"<div class='table-meta'>{html.escape(t['showing_rows'].format(shown=len(outDf), total=len(fullDf)))}</div>"
    )
    st.dataframe(outDf, use_container_width=True, hide_index=True, height=520)

    st.download_button(
        t["btn_download"],
        data=outDf.to_csv(index=False).encode("utf-8-sig"),
        file_name="camedustats_data.csv",
        mime="text/csv",
    )


# ============================================================
# PAGE 5: ABOUT
# ============================================================

elif activePage == "about":
    pageHeader(t["about_title"], t["about_sub"])

    def renderAboutList(titleText, items):
        lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
        renderHtml(
            f"""
            <div class="about-card">
                <div class="about-card-title">{html.escape(titleText)}</div>
                <ul class="about-list">{lis}</ul>
            </div>
            """
        )

    renderHtml(
        f"""
        <div class="about-card">
            <div class="about-card-title">{html.escape(t['about_goal_title'])}</div>
            <div class="about-card-body">{html.escape(t['about_goal_body'])}</div>
        </div>
        """
    )

    colA, colB = st.columns(2)
    with colA:
        renderAboutList(t["about_data_title"], t["about_data_items"])
        renderAboutList(t["about_limits_title"], t["about_limits_items"])
    with colB:
        renderAboutList(t["about_method_title"], t["about_method_items"])
        renderHtml(
            f"""
            <div class="about-card">
                <div class="about-card-title">{html.escape(t['about_stack_title'])}</div>
                <div class="about-card-body">{html.escape(t['about_stack_body'])}</div>
            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

renderHtml(
    f"""
    <div class="app-footer">
        <span><strong>{html.escape(t['footer_left'])}</strong></span>
        <span>{html.escape(t['footer_right'].format(span=SPAN_FULL))}</span>
    </div>
    """
)