"""
Custom CSS injected once per page to move away from default Streamlit look.
Design direction: DARK theme with vibrant multi-color neon accents,
3D tilt-on-hover glass cards, floating animated gradient blobs,
glowing shimmer buttons, and smooth interactive transitions.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    :root {
        --bg-primary: #07070d;
        --bg-secondary: #0f0f1c;
        --bg-card: #16162466;
        --border-color: #2a2a40;
        --text-primary: #f5f5fa;
        --text-secondary: #a3a3c2;
        --accent: #833ab4;

        /* multi-color neon palette */
        --neon-1: #405DE6;
        --neon-2: #833AB4;
        --neon-3: #E1306C;
        --neon-4: #FD1D1D;
        --neon-5: #00e5ff;
        --neon-6: #ffb800;

        --grad: linear-gradient(90deg, var(--neon-1) 0%, var(--neon-2) 30%, var(--neon-3) 60%, var(--neon-4) 80%, var(--neon-6) 100%);
        --grad-soft: linear-gradient(135deg, rgba(131,58,180,0.22) 0%, rgba(253,29,29,0.22) 50%, rgba(0,229,255,0.18) 100%);
    }

    /* ===== Animated multi-blob 3D background ===== */
    .stApp {
        background: var(--bg-primary);
        position: relative;
        overflow-x: hidden;
    }
    .stApp::before, .stApp::after {
        content: ""; position: fixed; border-radius: 50%; filter: blur(90px);
        opacity: 0.35; z-index: 0; pointer-events: none;
    }
    .stApp::before {
        width: 520px; height: 520px; top: -120px; left: -100px;
        background: radial-gradient(circle, var(--neon-2), transparent 70%);
        animation: floatBlob1 16s ease-in-out infinite;
    }
    .stApp::after {
        width: 480px; height: 480px; bottom: -140px; right: -100px;
        background: radial-gradient(circle, var(--neon-5), transparent 70%);
        animation: floatBlob2 18s ease-in-out infinite;
    }
    @keyframes floatBlob1 {
        0%, 100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(80px, 60px) scale(1.15); }
    }
    @keyframes floatBlob2 {
        0%, 100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(-70px, -50px) scale(1.1); }
    }

    #MainMenu, footer { visibility: hidden; }
    header [data-testid="stToolbar"] { visibility: hidden; }

    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; position: relative; z-index: 1; }

    h1, h2, h3, h4 { color: var(--text-primary) !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    p, span, li, label { color: var(--text-secondary); }

    /* ===== Hero ===== */
    .hero-badge {
        display: inline-block; padding: 7px 16px; border-radius: 999px;
        background: var(--grad-soft); border: 1px solid rgba(193,53,132,0.5);
        color: #ff9ecf; font-size: 0.8rem; font-weight: 600; margin-bottom: 16px;
        letter-spacing: 0.02em;
        box-shadow: 0 0 18px rgba(225,48,108,0.25);
        animation: pulseBadge 3s ease-in-out infinite;
    }
    @keyframes pulseBadge {
        0%, 100% { box-shadow: 0 0 12px rgba(225,48,108,0.2); }
        50% { box-shadow: 0 0 24px rgba(225,48,108,0.45); }
    }

    .hero-title {
        font-size: 3rem; font-weight: 900; line-height: 1.12; margin: 0;
        background: var(--grad);
        background-size: 300% auto;
        -webkit-background-clip: text; background-clip: text; color: transparent;
        animation: shine 6s linear infinite;
        filter: drop-shadow(0 0 25px rgba(131,58,180,0.35));
    }
    @keyframes shine { to { background-position: 300% center; } }

    .hero-sub { font-size: 1.15rem; color: var(--text-secondary); margin-top: 12px; max-width: 640px; }

    /* ===== 3D Tilt Glass Cards ===== */
    .pf-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-color);
        border-radius: 20px; padding: 24px; margin-bottom: 20px;
        position: relative; overflow: hidden;
        transform-style: preserve-3d;
        will-change: transform;
        transition: transform 0.12s ease-out, box-shadow 0.3s ease, border-color 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    }
    .pf-card::before {
        content: ""; position: absolute; inset: 0; border-radius: 20px;
        padding: 1.5px; background: var(--grad); background-size: 250% auto; opacity: 0;
        transition: opacity 0.3s ease;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor; mask-composite: exclude;
        pointer-events: none;
    }
    .pf-card::after {
        content: ""; position: absolute; inset: 0; border-radius: 20px;
        background: radial-gradient(circle at var(--mx,50%) var(--my,50%), rgba(255,255,255,0.12), transparent 60%);
        opacity: 0; transition: opacity 0.3s ease; pointer-events: none;
    }
    .pf-card:hover {
        box-shadow: 0 20px 50px rgba(131, 58, 180, 0.35), 0 8px 24px rgba(225, 48, 108, 0.25), 0 0 0 1px rgba(0,229,255,0.08);
    }
    .pf-card:hover::before { opacity: 1; animation: borderShift 3s linear infinite; }
    .pf-card:hover::after { opacity: 1; }
    @keyframes borderShift { to { background-position: 250% center; } }

    .pf-card-title {
        font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;
        transform: translateZ(30px);
    }
    .pf-card-desc { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.5; transform: translateZ(20px); }

    .pf-tag {
        display: inline-block; background: rgba(131,58,180,0.14); color: #d3b3f0;
        border: 1px solid rgba(131,58,180,0.4); border-radius: 8px;
        padding: 3px 10px; font-size: 0.72rem; margin: 0 6px 6px 0; font-weight: 500;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    .pf-tag:hover {
        transform: translateY(-3px) scale(1.05);
        background: rgba(0,229,255,0.14); border-color: rgba(0,229,255,0.5);
        box-shadow: 0 4px 14px rgba(0,229,255,0.25);
    }

    .pf-badge {
        display: inline-block; border-radius: 8px; padding: 4px 12px;
        font-size: 0.72rem; font-weight: 700; color: white; letter-spacing: 0.02em;
        background: var(--grad); background-size: 250% auto;
        animation: borderShift 4s linear infinite;
        box-shadow: 0 0 14px rgba(131,58,180,0.4);
    }

    .pf-section-label {
        text-transform: uppercase; font-size: 0.78rem; font-weight: 800;
        letter-spacing: 0.1em; margin-bottom: 8px;
        background: var(--grad); background-size: 250% auto;
        -webkit-background-clip: text; background-clip: text; color: transparent;
        animation: borderShift 5s linear infinite;
    }

    /* ===== Buttons — gradient + shimmer sweep + 3D press ===== */
    .stButton>button, .stLinkButton>a {
        border-radius: 12px !important; font-weight: 700 !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.25s cubic-bezier(0.2,0.8,0.2,1) !important;
        position: relative !important; overflow: hidden !important;
    }
    .stButton>button:hover, .stLinkButton>a:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(131, 58, 180, 0.4);
    }
    .stButton>button:active, .stLinkButton>a:active {
        transform: translateY(0px) scale(0.98);
    }
    .stButton>button[kind="primary"] {
        background: var(--grad) !important;
        background-size: 250% auto !important;
        border: none !important;
        transition: background-position 0.5s ease, transform 0.25s ease, box-shadow 0.25s ease !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-position: right center !important;
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 12px 32px rgba(225, 48, 108, 0.45);
    }
    .stButton>button[kind="primary"]::after {
        content: ""; position: absolute; top: 0; left: -60%; width: 40%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.35), transparent);
        transform: skewX(-20deg);
        animation: shimmerSweep 3.2s ease-in-out infinite;
    }
    @keyframes shimmerSweep {
        0% { left: -60%; }
        50%, 100% { left: 130%; }
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary), #0a0a14);
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .stButton>button {
        text-align: left !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        transform: translateX(4px);
        background: var(--grad-soft) !important;
        border-color: rgba(131,58,180,0.5) !important;
        box-shadow: 0 0 16px rgba(131,58,180,0.25);
    }

    /* ===== Empty state ===== */
    .pf-empty {
        text-align: center; padding: 40px 20px; color: var(--text-secondary);
        border: 1px dashed var(--border-color); border-radius: 16px;
        background: var(--grad-soft);
    }

    hr {
        border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent) !important;
    }

    /* ===== Custom colorful scrollbar ===== */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb {
        background: var(--grad); border-radius: 10px;
    }

    /* ===== Fade-in on load ===== */
    .block-container { animation: fadein 0.6s ease; }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""


def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def inject_3d_tilt():
    """
    Adds real-time mouse-tracking 3D tilt to every element with class
    'pf-card'. Uses MutationObserver + event delegation so it keeps
    working even after Streamlit re-renders the DOM on every rerun.
    Call this ONCE per page, anywhere after inject_custom_css().
    """
    st.markdown(
        """
        <script>
        (function() {
            const MAX_TILT = 10; // degrees

            function handleMove(e) {
                const card = e.target.closest('.pf-card');
                if (!card) return;
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const px = (x / rect.width) - 0.5;
                const py = (y / rect.height) - 0.5;

                const rotateY = px * MAX_TILT * 2;
                const rotateX = -py * MAX_TILT * 2;

                card.style.transform =
                    `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px) scale(1.02)`;
                card.style.setProperty('--mx', (px * 100 + 50) + '%');
                card.style.setProperty('--my', (py * 100 + 50) + '%');
            }

            function handleLeave(e) {
                const card = e.target.closest('.pf-card');
                if (!card) return;
                card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)';
            }

            // Event delegation on the whole document so newly rendered
            // Streamlit cards are automatically covered, no re-binding needed.
            document.addEventListener('mousemove', handleMove, { passive: true });
            document.addEventListener('mouseleave', handleLeave, true);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


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
