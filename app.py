"""
LS AutoPredict - Prediccion de precio de vehiculos BMW usados.

Autor: Luis Alexander Suarez Colimba
Maestria en Inteligencia Artificial y Ciencia de Datos
Universidad Casa Grande

Arquitectura:
    - core.py     -> Helpers compartidos (POO, Funcional, Declarativo, ML)
    - views/      -> Una pagina por archivo
    - app.py      -> Entry point: configuracion, sidebar y ruteo
"""

import streamlit as st
from streamlit_option_menu import option_menu

import core
from views import inicio, limpieza, analisis, visualizaciones, prediccion, biografia


# ============================================================
# CONFIGURACION DE LA PAGINA
# ============================================================
st.set_page_config(
    page_title="LS AutoPredict | UCG",
    page_icon=str(core.RUTA_ICONO) if core.RUTA_ICONO.exists() else "🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

core.inject_css()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    if core.RUTA_LOGO.exists():
        st.image(str(core.RUTA_LOGO), width="content")
        st.markdown("""
            <div style="color: #64748B; font-size: 0.78rem; text-align: center;
                        margin-top: 6px; letter-spacing: 0.08em;
                        text-transform: uppercase;">
               🏛️ UCG · Proyecto Final
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <div style="font-size: 2rem;">🚗</div>
                <div style="font-weight: 700; font-size: 1.2rem; color: #0F172A;">
                    LS AutoPredict
                </div>
                <div style="color: #64748B; font-size: 0.85rem;">
                    UCG · Proyecto Final
                </div>
            </div>
        """, unsafe_allow_html=True)

    seleccion = option_menu(
        menu_title=None,
        options=["Inicio", "Limpieza", "Analisis",
                 "Visualizaciones", "Prediccion", "Biografia"],
        icons=["house-fill", "magic", "search",
               "bar-chart-fill", "calculator-fill", "person-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#1C69D4", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px", "text-align": "left", "margin": "4px 0",
                "padding": "12px 16px", "border-radius": "10px",
                "color": "#475569",
                "--hover-color": "#DBEAFE",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #1C69D4, #2A7BE8)",
                "color": "white", "font-weight": "600",
            },
        },
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
        <div style="color: #64748B; font-size: 0.78rem; text-align: center;">
           🚀 Luis Suárez · 2026<br>
           🎓 Maestria IA y Ciencia de Datos
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# RUTEO
# ============================================================
PAGINAS = {
    "Inicio": inicio.render,
    "Limpieza": limpieza.render,
    "Analisis": analisis.render,
    "Visualizaciones": visualizaciones.render,
    "Prediccion": prediccion.render,
    "Biografia": biografia.render,
}

PAGINAS[seleccion]()
