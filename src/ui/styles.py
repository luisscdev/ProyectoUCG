"""
Estilos CSS personalizados para Streamlit.
Tema oscuro moderno con acentos azules estilo automotriz premium.
"""

import streamlit as st


CUSTOM_CSS = """
<style>
/* === Reset general === */
.stApp {
    background: linear-gradient(180deg, #0E1117 0%, #0A0D14 100%);
}

/* === Tipografía === */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
    letter-spacing: -0.01em;
}

/* === Encabezados === */
h1 {
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #1C69D4 0%, #5BA4F5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2, h3 {
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: #FAFAFA !important;
}

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12151C 0%, #0A0D14 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] .stMarkdown {
    color: #A8B3C7;
}

/* === Cards / Contenedores === */
.card {
    background: linear-gradient(145deg, rgba(28, 105, 212, 0.08), rgba(28, 105, 212, 0.02));
    border: 1px solid rgba(28, 105, 212, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.card:hover {
    border-color: rgba(28, 105, 212, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(28, 105, 212, 0.15);
}

/* === KPIs === */
.kpi {
    background: linear-gradient(145deg, #1A1D24, #12151C);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: left;
}

.kpi-label {
    font-size: 0.85rem;
    color: #6B7388;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FAFAFA;
    line-height: 1.1;
}

.kpi-delta {
    font-size: 0.85rem;
    color: #5BA4F5;
    margin-top: 4px;
}

/* === Hero === */
.hero {
    padding: 48px 32px;
    background: linear-gradient(135deg, rgba(28, 105, 212, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
    border-radius: 24px;
    border: 1px solid rgba(28, 105, 212, 0.2);
    margin-bottom: 32px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #FFFFFF 0%, #5BA4F5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #A8B3C7;
    font-weight: 400;
    max-width: 720px;
    line-height: 1.6;
}

/* === Botones === */
.stButton > button {
    background: linear-gradient(135deg, #1C69D4 0%, #2A7BE8 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(28, 105, 212, 0.3);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(28, 105, 212, 0.45);
    background: linear-gradient(135deg, #2A7BE8 0%, #3B8AF5 100%);
}

/* === Inputs === */
.stSelectbox > div > div,
.stNumberInput > div > div,
.stTextInput > div > div {
    background-color: #1A1D24 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
}

/* === DataFrames === */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: #1A1D24;
    border-radius: 10px;
    padding: 8px 18px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1C69D4, #2A7BE8) !important;
    color: white !important;
}

/* === Métricas nativas === */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    font-size: 0.85rem;
    color: #6B7388;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* === Divider === */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(28, 105, 212, 0.3), transparent);
    margin: 32px 0;
}

/* === Badge === */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: rgba(28, 105, 212, 0.15);
    color: #5BA4F5;
    border: 1px solid rgba(28, 105, 212, 0.3);
    margin-right: 8px;
}

.badge.success { background: rgba(46, 204, 113, 0.15); color: #2ECC71; border-color: rgba(46, 204, 113, 0.3); }
.badge.warn    { background: rgba(241, 196, 15, 0.15); color: #F1C40F; border-color: rgba(241, 196, 15, 0.3); }
.badge.purple  { background: rgba(155, 89, 182, 0.15); color: #BB8FCE; border-color: rgba(155, 89, 182, 0.3); }

/* === Footer === */
.footer {
    text-align: center;
    padding: 24px 0;
    color: #6B7388;
    font-size: 0.85rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    margin-top: 48px;
}

/* === Bio === */
.bio-card {
    background: linear-gradient(145deg, rgba(28, 105, 212, 0.06), rgba(155, 89, 182, 0.04));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 32px;
    margin: 16px 0;
}

.bio-avatar {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1C69D4, #BB8FCE);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    font-weight: 700;
    color: white;
    margin: 0 auto;
    border: 4px solid rgba(255, 255, 255, 0.1);
}

/* Esconder branding Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header [data-testid="stToolbar"] {visibility: hidden;}
</style>
"""


def inject_css() -> None:
    """Inyecta el CSS personalizado en la app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# === Color palette helper para plotly ===
PALETTE = {
    "primary": "#1C69D4",
    "primary_light": "#5BA4F5",
    "accent": "#BB8FCE",
    "success": "#2ECC71",
    "warning": "#F1C40F",
    "danger": "#E74C3C",
    "bg": "#0E1117",
    "surface": "#1A1D24",
    "text": "#FAFAFA",
    "muted": "#6B7388",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#FAFAFA", "family": "Inter, sans-serif"},
        "colorway": ["#1C69D4", "#5BA4F5", "#BB8FCE", "#2ECC71", "#F1C40F", "#E74C3C"],
        "xaxis": {"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.1)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.1)"},
        "hoverlabel": {"bgcolor": "#1A1D24", "font_color": "#FAFAFA", "bordercolor": "#1C69D4"},
    }
}
