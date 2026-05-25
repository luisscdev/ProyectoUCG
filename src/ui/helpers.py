"""
Componentes reutilizables para las vistas Streamlit.
"""

from __future__ import annotations
import streamlit as st


def kpi_card(label: str, value: str, delta: str | None = None) -> None:
    """Muestra una tarjeta KPI con estilo personalizado."""
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, badges: list[str] | None = None) -> None:
    """Bloque hero llamativo en la parte superior de la vista."""
    badges_html = ""
    if badges:
        badges_html = "<div style='margin-bottom: 16px;'>" + "".join(
            f'<span class="badge">{b}</span>' for b in badges
        ) + "</div>"
    st.markdown(
        f"""
        <div class="hero">
            {badges_html}
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, description: str | None = None) -> None:
    """Título de sección con descripción opcional."""
    st.markdown(f"### {title}")
    if description:
        st.markdown(
            f"<p style='color: #A8B3C7; margin-top: -8px; margin-bottom: 16px;'>{description}</p>",
            unsafe_allow_html=True,
        )


def footer() -> None:
    """Pie de página común."""
    st.markdown(
        """
        <div class="footer">
            Universidad Casa Grande · Maestría en Inteligencia Artificial y Ciencia de Datos<br>
            Proyecto Final · Paradigmas de Programación para IA y Análisis de Datos · 2026
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider() -> None:
    """Línea divisora estilizada."""
    st.markdown("<hr/>", unsafe_allow_html=True)
