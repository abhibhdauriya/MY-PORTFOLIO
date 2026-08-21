"""
Custom CSS injected once per page to move away from default Streamlit look.
Design direction: modern, minimal, professional. Dark theme base.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    :root {
        --bg-primary: #0f1117;
        --bg-secondary: #161923;
        --bg-card: #1a1e2a;
        --border-color: #262b3a;
        --text-primary: #f1f3f8;
        --text-secondary: #9aa1b5;
        --accent: #4f8cff;
        --accent-soft: rgba(79, 140, 255, 0.12);
    }

    .stApp { background-color: var(--bg-primary); }
    #MainMenu, footer, header { visibility: hidden; }

    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }

    h1, h2, h3, h4 { color: var(--text-primary) !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, li, label { color: var(--text-secondary); }

    /* Hero */
    .hero-badge {
        display: inline-block; padding: 6px 14px; border-radius: 999px;
        background: var(--accent-soft); color: var(--accent);
        font-size: 0.8rem; font-weight: 600; margin-bottom: 14px;
        letter-spacing: 0.02em;
    }
    .hero-title { font-size: 2.6rem; font-weight: 800; color: var(--text-primary); line-height: 1.15; margin: 0; }
    .hero-sub { font-size: 1.15rem; color: var(--text-secondary); margin-top: 10px; max-width: 640px; }

    /* Cards */
    .pf-card {
        background: var(--bg-card); border: 1px solid var(--border-color);
        border-radius: 14px; padding: 20px; margin-bottom: 16px;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pf-card:hover { border-color: var(--accent); transform: translateY(-2px); }

    .pf-card-title { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
    .pf-card-desc { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.5; }

    .pf-tag {
        display: inline-block; background: var(--bg-secondary); color: var(--text-secondary);
        border: 1px solid var(--border-color); border-radius: 6px;
        padding: 3px 9px; font-size: 0.72rem; margin: 0 6px 6px 0; font-weight: 500;
    }

    .pf-badge {
        display: inline-block; border-radius: 6px; padding: 3px 10px;
        font-size: 0.72rem; font-weight: 700; color: white; letter-spacing: 0.02em;
    }

    .pf-section-label {
        text-transform: uppercase; font-size: 0.78rem; font-weight: 700;
        letter-spacing: 0.08em; color: var(--accent); margin-bottom: 6px;
    }

    /* Buttons */
    .stButton>button, .stLinkButton>a {
        border-radius: 8px !important; font-weight: 600 !important;
        border: 1px solid var(--border-color) !important;
    }
    .stButton>button[kind="primary"] {
        background: var(--accent) !important; border-color: var(--accent) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: var(--bg-secondary); border-right: 1px solid var(--border-color); }

    /* Empty state */
    .pf-empty {
        text-align: center; padding: 40px 20px; color: var(--text-secondary);
        border: 1px dashed var(--border-color); border-radius: 12px;
    }

    hr { border-color: var(--border-color) !important; }
</style>
"""


def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def inject_seo_meta(description: str, site_title: str):
    """
    Best-effort SEO injection. Streamlit doesn't expose the document <head>
    directly, so this uses a small JS snippet to set the meta description
    and document title client-side. Search engines that execute JS (modern
    Googlebot) will pick this up; it's not a substitute for server-rendered
    meta tags, which Streamlit's architecture doesn't support.
    """
    st.markdown(
        f"""
        <script>
            document.title = {site_title!r};
            var meta = document.querySelector('meta[name="description"]');
            if (!meta) {{
                meta = document.createElement('meta');
                meta.name = "description";
                document.head.appendChild(meta);
            }}
            meta.content = {description!r};
        </script>
        """,
        unsafe_allow_html=True,
    )
