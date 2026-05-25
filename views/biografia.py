"""Vista 'Biografía' — información personal del autor."""

import streamlit as st
from src.ui.helpers import hero, section_title, divider, footer


def render() -> None:
    hero(
        title="Sobre el Autor",
        subtitle="Información personal y profesional del desarrollador del proyecto.",
        badges=["Biografía"],
    )

    # === Bloque principal ===
    col_avatar, col_info = st.columns([1, 2])

    with col_avatar:
        st.markdown(
            """
            <div style="text-align: center;">
                <div class="bio-avatar">LS</div>
                <div style="margin-top: 16px; font-size: 1.3rem; font-weight: 700; color: #FAFAFA;">
                    Luis Alexander Suárez Colimba
                </div>
                <div style="color: #5BA4F5; margin-top: 4px;">
                    Estudiante de Maestría · Desarrollador
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown("### Quién Soy")
        st.markdown(
            """
            Estudiante de la **Maestría en Inteligencia Artificial y Ciencia de Datos**
            en la **Universidad Casa Grande**. Me interesa el desarrollo de software
            combinado con el análisis de datos, especialmente los proyectos donde se
            puede pasar de un dataset crudo a una aplicación que use otra persona.
            """
        )

    divider()

    # === Datos clave ===
    section_title("Contacto")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card">
                <div style="color: #6B7388; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">
                    📧 Correo
                </div>
                <div style="font-size: 1rem; font-weight: 600; margin-top: 8px;">
                    luissuarez2t@gmail.com
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
                <div style="color: #6B7388; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">
                    🎓 Universidad
                </div>
                <div style="font-size: 1rem; font-weight: 600; margin-top: 8px;">
                    Universidad Casa Grande
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="card">
                <div style="color: #6B7388; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">
                    📍 Ubicación
                </div>
                <div style="font-size: 1rem; font-weight: 600; margin-top: 8px;">
                    Ecuador
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    divider()

    # === Formación ===
    section_title("Formación Académica")
    formaciones = [
        {
            "titulo": "Maestría en Inteligencia Artificial y Ciencia de Datos",
            "institucion": "Universidad Casa Grande",
            "periodo": "2025 — En curso",
        },
        {
            "titulo": "[Edita tu pregrado en views/biografia.py]",
            "institucion": "[Universidad]",
            "periodo": "[Año — Año]",
        },
    ]
    for f in formaciones:
        st.markdown(
            f"""
            <div class="card">
                <div style="font-weight: 700; color: #FAFAFA; font-size: 1.1rem;">{f['titulo']}</div>
                <div style="color: #5BA4F5; margin-top: 4px;">{f['institucion']} · {f['periodo']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    divider()

    # === Habilidades técnicas ===
    section_title("Habilidades Técnicas")
    habilidades = {
        "Lenguajes": ["Python", "SQL", "JavaScript", "TypeScript"],
        "Ciencia de Datos": ["Pandas", "NumPy", "Scikit-learn", "Plotly"],
        "Frameworks Web": ["Streamlit", "Angular", "FastAPI"],
        "Bases de Datos": ["PostgreSQL", "MongoDB"],
        "Herramientas": ["Git", "Docker", "GitHub"],
    }
    for categoria, items in habilidades.items():
        badges = "".join([f'<span class="badge">{i}</span>' for i in items])
        st.markdown(
            f"""
            <div style="margin-bottom: 16px;">
                <div style="color: #6B7388; font-size: 0.9rem; margin-bottom: 8px;">{categoria}</div>
                <div>{badges}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    divider()
    footer()
