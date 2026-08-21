"""
Seeds the database with realistic, clearly-fictional demo content so the
portfolio looks complete immediately after install. Safe to run multiple
times — skips seeding if projects already exist.

Run once locally:  python seed_demo_data.py
"""

from database.db import init_db, fetch_one, insert_row

DEMO_PROJECTS = [
    {
        "title": "MIS Pro Dashboard (Demo)",
        "category": "Web Development",
        "short_description": "A Streamlit dashboard for daily MIS reporting with interactive charts and filters.",
        "detailed_description": "Sample project illustrating a multi-page MIS reporting dashboard built with Streamlit, Pandas, and Plotly.",
        "problem": "Manual daily reports took hours to compile from raw exports.",
        "approach": "Built a repeatable data pipeline to clean and aggregate exports automatically.",
        "solution": "A Streamlit app that ingests CSV exports and renders live KPI charts.",
        "features": "Interactive KPI cards\nDate-range filtering\nExportable charts\nRole-based demo login",
        "results": "",
        "technologies": "Python, Streamlit, Pandas, Plotly, SQLite",
        "tags": "MIS, Dashboard, Python",
        "status": "Live",
        "is_featured": 1,
        "is_published": 1,
        "uses_python": 1,
    },
    {
        "title": "Excel MIS Automation (Demo)",
        "category": "Excel Automation",
        "short_description": "Automated daily MIS reporting workflow using VBA and Power Query.",
        "detailed_description": "Sample Excel automation project showing a sanitized template for daily report generation.",
        "problem": "Daily report compilation was repetitive and error-prone when done manually.",
        "approach": "Automated data refresh with Power Query, formatting and distribution with VBA macros.",
        "solution": "A single-click macro that refreshes, formats, and exports the daily report.",
        "features": "One-click refresh macro\nPower Query data model\nConditional formatting\nAuto-generated PDF export",
        "results": "",
        "technologies": "Excel, VBA, Power Query",
        "tags": "Excel, VBA, Automation",
        "status": "Completed",
        "is_featured": 1,
        "is_published": 1,
        "uses_vba": 1,
        "uses_power_query": 1,
        "excel_version": "Microsoft 365",
    },
    {
        "title": "Attendance Automation (Demo)",
        "category": "VBA",
        "short_description": "VBA-based attendance tracking and summary generator.",
        "detailed_description": "Fictional sample showing an attendance tracker template with automated monthly summaries.",
        "problem": "Attendance summaries were compiled manually every month.",
        "approach": "Built VBA macros to validate entries and auto-generate summaries.",
        "solution": "A workbook that generates a monthly attendance summary with one click.",
        "features": "Data validation\nAuto summary sheet\nException flagging",
        "results": "",
        "technologies": "Excel, VBA",
        "tags": "Excel, VBA, HR",
        "status": "Completed",
        "is_featured": 0,
        "is_published": 1,
        "uses_vba": 1,
    },
    {
        "title": "Courier Tracking Dashboard (Demo)",
        "category": "Web Development",
        "short_description": "A Streamlit dashboard visualizing sample courier/dispatch data.",
        "detailed_description": "Fictional demo dashboard for tracking dispatch status across a sample courier dataset.",
        "problem": "Dispatch status was scattered across multiple sheets.",
        "approach": "Consolidated sample data into a single SQLite-backed dashboard.",
        "solution": "A searchable, filterable dispatch status dashboard.",
        "features": "Status filters\nSearch by ID\nDaily volume chart",
        "results": "",
        "technologies": "Python, Streamlit, SQLite",
        "tags": "Python, Dashboard, Logistics",
        "status": "Live",
        "is_featured": 1,
        "is_published": 1,
        "uses_python": 1,
    },
    {
        "title": "Inventory Analytics (Demo)",
        "category": "Data Analytics",
        "short_description": "Exploratory analysis and visualization of sample inventory data.",
        "detailed_description": "Fictional demo analyzing sample stock-level data to identify slow-moving inventory.",
        "problem": "Slow-moving stock was hard to identify from raw spreadsheets.",
        "approach": "Used Pandas to compute turnover ratios and flag outliers.",
        "solution": "A notebook-driven analysis with summary visualizations.",
        "features": "Turnover ratio calculation\nOutlier flagging\nCategory-wise breakdown",
        "results": "",
        "technologies": "Python, Pandas, Matplotlib",
        "tags": "Python, Data Analytics",
        "status": "Completed",
        "is_featured": 0,
        "is_published": 1,
        "uses_python": 1,
    },
    {
        "title": "Business Analytics Dashboard (Demo)",
        "category": "Dashboard",
        "short_description": "A sample multi-metric business analytics dashboard.",
        "detailed_description": "Fictional demo dashboard combining sales, inventory, and MIS metrics in one view.",
        "problem": "Business metrics lived in separate disconnected reports.",
        "approach": "Combined sample datasets into a unified SQLite schema.",
        "solution": "A single-pane dashboard with drill-down by metric.",
        "features": "Unified metric view\nDrill-down charts\nDate comparison",
        "results": "",
        "technologies": "Python, Streamlit, Plotly, SQLite",
        "tags": "Dashboard, MIS, Data Analytics",
        "status": "In Development",
        "is_featured": 0,
        "is_published": 1,
        "uses_python": 1,
    },
]

DEMO_SKILLS = [
    ("Advanced Excel", "Excel"), ("Pivot Tables", "Excel"), ("XLOOKUP", "Excel"),
    ("INDEX/MATCH", "Excel"), ("SUMIFS/COUNTIFS", "Excel"), ("Power Query", "Excel"),
    ("VBA", "Excel"), ("Dashboard Development", "Excel"),
    ("Python", "Programming"), ("Pandas", "Programming"), ("OpenPyXL", "Programming"), ("SQL", "Programming"),
    ("HTML", "Web"), ("CSS", "Web"), ("JavaScript", "Web"), ("Streamlit", "Web"),
    ("Data Cleaning", "Data"), ("Data Analysis", "Data"), ("Data Visualization", "Data"), ("MIS Reporting", "Data"),
    ("Git", "Tools"), ("GitHub", "Tools"), ("SQLite", "Tools"), ("Plotly", "Tools"),
]


def seed():
    init_db()

    if fetch_one("SELECT id FROM projects LIMIT 1"):
        print("Projects already exist — skipping project seed.")
    else:
        for p in DEMO_PROJECTS:
            insert_row("projects", p)
        print(f"Seeded {len(DEMO_PROJECTS)} demo projects.")

    if fetch_one("SELECT id FROM skills LIMIT 1"):
        print("Skills already exist — skipping skill seed.")
    else:
        for i, (name, category) in enumerate(DEMO_SKILLS):
            insert_row("skills", {"name": name, "category": category, "level": "", "sort_order": i})
        print(f"Seeded {len(DEMO_SKILLS)} skills.")


if __name__ == "__main__":
    seed()
