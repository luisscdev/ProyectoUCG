"""Vista de inicio — Dashboard con KPIs y vista rápida del dataset."""

import streamlit as st
import plotly.express as px

from src.ui.helpers import hero, kpi_card, section_title, divider, footer
from src.ui.styles import PLOTLY_TEMPLATE, PALETTE
from src.ui.data_loader import cargar_dataset
from src.declarative import kpis_globales, distribucion_combustible, precio_promedio_por_anio


def _t(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig


def render() -> None:
    df = cargar_dataset()
    k = kpis_globales(df)

    hero(
        title="Dashboard BMW",
        subtitle=(
            "Resumen general del catálogo de vehículos BMW usados. "
            "Usa el menú lateral para explorar el dataset, generar visualizaciones "
            "o predecir el precio de un vehículo."
        ),
        badges=["Dashboard", "10.781 vehículos", "Actualizado"],
    )

    # KPIs principales
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Vehículos", f"{k['total_vehiculos']:,}")
    with c2:
        kpi_card("Modelos únicos", f"{k['modelos_unicos']}")
    with c3:
        kpi_card("Precio promedio", f"£ {k['precio_promedio']:,.0f}")
    with c4:
        kpi_card("Precio mediano", f"£ {k['precio_mediano']:,.0f}")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        kpi_card("Año mínimo", f"{k['anio_min']}")
    with c6:
        kpi_card("Año máximo", f"{k['anio_max']}")
    with c7:
        kpi_card("Km promedio", f"{k['km_promedio']:,.0f}")
    with c8:
        kpi_card("Precio máximo", f"£ {df['price'].max():,.0f}")

    divider()

    # Mini-gráficos
    col1, col2 = st.columns(2)

    with col1:
        section_title("Precio Promedio por Año")
        serie = precio_promedio_por_anio(df)
        fig = px.area(serie, x="year", y="precio_promedio",
                      color_discrete_sequence=[PALETTE["primary"]])
        fig.update_layout(xaxis_title="", yaxis_title="£", height=320)
        st.plotly_chart(_t(fig), use_container_width=True)

    with col2:
        section_title("Distribución por Combustible")
        dist = distribucion_combustible(df)
        col_porcentaje = dist.columns[-1]
        col_categoria = dist.columns[0]
        fig = px.pie(dist, values=col_porcentaje, names=col_categoria, hole=0.55,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=320)
        st.plotly_chart(_t(fig), use_container_width=True)

    divider()

    section_title("Últimos Registros del Dataset")
    st.dataframe(df.head(15), use_container_width=True, hide_index=True)

    footer()
