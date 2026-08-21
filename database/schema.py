"""
SQL schema definitions for the portfolio CMS.
Run once via database.db.init_db() to create all tables.
"""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT DEFAULT '',
    headline TEXT DEFAULT '',
    about TEXT DEFAULT '',
    location TEXT DEFAULT '',
    email TEXT DEFAULT '',
    github_url TEXT DEFAULT '',
    linkedin_url TEXT DEFAULT '',
    portfolio_url TEXT DEFAULT '',
    resume_path TEXT DEFAULT '',
    profile_image_path TEXT DEFAULT '',
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    short_description TEXT DEFAULT '',
    detailed_description TEXT DEFAULT '',
    problem TEXT DEFAULT '',
    approach TEXT DEFAULT '',
    solution TEXT DEFAULT '',
    features TEXT DEFAULT '',          -- newline separated
    results TEXT DEFAULT '',
    category TEXT NOT NULL DEFAULT 'Other',   -- MIS/Excel Automation/VBA/Python/Web Development/Data Analytics/Dashboard/Other
    technologies TEXT DEFAULT '',      -- comma separated
    tags TEXT DEFAULT '',              -- comma separated
    github_url TEXT DEFAULT '',
    live_url TEXT DEFAULT '',
    documentation_url TEXT DEFAULT '',
    demo_video_url TEXT DEFAULT '',
    thumbnail_path TEXT DEFAULT '',
    screenshots TEXT DEFAULT '',       -- comma separated file paths
    sample_xlsx_path TEXT DEFAULT '',
    sample_xlsm_path TEXT DEFAULT '',
    pdf_doc_path TEXT DEFAULT '',
    status TEXT DEFAULT 'Completed',   -- Planning/In Development/Completed/Live/Archived
    version TEXT DEFAULT '',
    is_featured INTEGER DEFAULT 0,
    is_published INTEGER DEFAULT 1,
    excel_version TEXT DEFAULT '',
    uses_vba INTEGER DEFAULT 0,
    uses_python INTEGER DEFAULT 0,
    uses_power_query INTEGER DEFAULT 0,
    uses_power_pivot INTEGER DEFAULT 0,
    project_date TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,   -- Excel/Programming/Web/Data/Tools
    level TEXT DEFAULT '',    -- optional, only if user enters it
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    location TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    is_current INTEGER DEFAULT 0,
    description TEXT DEFAULT '',
    responsibilities TEXT DEFAULT '',
    achievements TEXT DEFAULT '',
    technologies TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    issuing_org TEXT DEFAULT '',
    issue_date TEXT DEFAULT '',
    credential_url TEXT DEFAULT '',
    description TEXT DEFAULT '',
    file_path TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT DEFAULT '',
    category TEXT DEFAULT 'Other',
    icon TEXT DEFAULT '',
    is_featured INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS site_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    site_title TEXT DEFAULT 'Abhishek Singh | Portfolio',
    subtitle TEXT DEFAULT 'MIS & Automation | Excel | Python | Data Analytics | Web Development',
    footer_text TEXT DEFAULT '© Abhishek Singh. Built with Python + Streamlit.',
    seo_description TEXT DEFAULT '',
    contact_email TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT DEFAULT '',
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS page_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT NOT NULL,
    project_id INTEGER,
    viewed_at TEXT DEFAULT (datetime('now'))
);
"""
