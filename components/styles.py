"""
Custom CSS injected once per page to move away from default Streamlit look.
Design direction: dark theme with vibrant Instagram-style gradient accents,
glassmorphism cards, glow-on-hover, and smooth animated transitions.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    :root {
        --bg-primary: #0a0a12;
        --bg-secondary: #12121e;
        --bg-card: #16162480;
        --border-color: #2a2a40;
        --text-primary: #f5f5fa;
        --text-secondary: #9a9ab5;
        --accent: #833ab4;
        --grad: linear-gradient(90deg, #405DE6 0%, #5851DB 20%, #833AB4 40%, #C13584 60%, #E1306C 80%, #FD1D1D 100%);
        --grad-soft: linear-gradient(135deg, rgba(131,58,180,0.18) 0%, rgba(253,29,29,0.18) 100%);
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #1a1030 0%, var(--bg-primary) 45%),
                    radial-gradient(circle at 100% 30%, #1a0e28 0%, var(--bg-primary) 50%);
    }
    #MainMenu, footer { visibility: hidden; }
    header [data-testid="stToolbar"] { visibility: hidden; }

    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }

    h1, h2, h3, h4 { color: var(--text-primary) !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    p, span, li, label { color: var(--text-secondary); }

    /* Hero */
    .hero-badge {
        display: inline-block; padding: 7px 16px; border-radius: 999px;
        background: var(--grad-soft); border: 1px solid rgba(193,53,132,0.4);
        color: #ff7ab8; font-size: 0.8rem; font-weight: 600; margin-bottom: 16px;
        letter-spacing: 0.02em;
    }
    .hero-title {
        font-size: 2.8rem; font-weight: 900; line-height: 1.12; margin: 0;
        background: var(--grad);
        background-size: 200% auto;
        -webkit-background-clip: text; background-clip: text; color: transparent;
        animation: shine 6s linear infinite;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }
    .hero-sub { font-size: 1.15rem; color: var(--text-secondary); margin-top: 12px; max-width: 640px; }

    /* Cards — glassmorphism with gradient glow on hover */
    .pf-card {
        background: var(--bg-card);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--border-color);
        border-radius: 18px; padding: 22px; margin-bottom: 18px;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        position: relative; overflow: hidden;
    }
    .pf-card::before {
        content: ""; position: absolute; inset: 0; border-radius: 18px;
        padding: 1px; background: var(--grad); opacity: 0;
        transition: opacity 0.3s ease;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor; mask-composite: exclude;
        pointer-events: none;
    }
    .pf-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 12px 40px rgba(131, 58, 180, 0.25), 0 4px 12px rgba(225, 48, 108, 0.15);
    }
    .pf-card:hover::before { opacity: 1; }

    .pf-card-title { font-size: 1.08rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
    .pf-card-desc { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.5; }

    .pf-tag {
        display: inline-block; background: rgba(131,58,180,0.12); color: #c9a3e8;
        border: 1px solid rgba(131,58,180,0.35); border-radius: 8px;
        padding: 3px 10px; font-size: 0.72rem; margin: 0 6px 6px 0; font-weight: 500;
        transition: transform 0.15s ease;
    }
    .pf-tag:hover { transform: translateY(-2px); }

    .pf-badge {
        display: inline-block; border-radius: 8px; padding: 4px 12px;
        font-size: 0.72rem; font-weight: 700; color: white; letter-spacing: 0.02em;
        background: var(--grad);
    }

    .pf-section-label {
        text-transform: uppercase; font-size: 0.78rem; font-weight: 800;
        letter-spacing: 0.1em; margin-bottom: 8px;
        background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent;
    }

    /* Buttons — gradient fill with glow */
    .stButton>button, .stLinkButton>a {
        border-radius: 10px !important; font-weight: 700 !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover, .stLinkButton>a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(131, 58, 180, 0.35);
    }
    .stButton>button[kind="primary"] {
        background: var(--grad) !important;
        background-size: 200% auto !important;
        border: none !important;
        transition: background-position 0.4s ease, transform 0.25s ease !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-position: right center !important;
        transform: translateY(-2px) scale(1.02);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .stButton>button:hover { transform: none; }

    /* Empty state */
    .pf-empty {
        text-align: center; padding: 40px 20px; color: var(--text-secondary);
        border: 1px dashed var(--border-color); border-radius: 14px;
    }

    hr { border-color: var(--border-color) !important; }

    /* Fade-in on load */
    .block-container { animation: fadein 0.5s ease; }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
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
