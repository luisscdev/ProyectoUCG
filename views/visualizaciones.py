"""Vista 'Visualizaciones' — gráficos interactivos con Plotly."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.ui.helpers import hero, section_title, divider, footer
from src.ui.styles import PLOTLY_TEMPLATE, PALETTE
from src.ui.data_loader import cargar_dataset
from src.declarative import (
    precio_promedio_por_modelo,
    precio_promedio_por_anio,
    distribucion_combustible,
    correlaciones,
)


def _apply_template(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig


def render() -> None:
    df = cargar_dataset()

    hero(
        title="Visualizaciones Interactivas",
        subtitle=(
            "Gráficos dinámicos construidos con Plotly. Pasa el mouse sobre los "
            "elementos para ver información detallada."
        ),
        badges=["Plotly", "Visualización", "Interactivo"],
    )

    section_title("Distribución del Precio", "Histograma con densidad superpuesta.")
    fig = px.histogram(df, x="price", nbins=60, opacity=0.85,
                       color_discrete_sequence=[PALETTE["primary"]])
    fig.update_layout(xaxis_title="Precio (£)", yaxis_title="Frecuencia", bargap=0.02)
    st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()

    section_title("Precio Promedio por Año", "Evolución temporal del precio.")
    serie = precio_promedio_por_anio(df)
    fig = px.line(serie, x="year", y="precio_promedio", markers=True,
                  color_discrete_sequence=[PALETTE["primary_light"]])
    fig.update_layout(xaxis_title="Año", yaxis_title="Precio promedio (£)")
    st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()

    col1, col2 = st.columns(2)

    with col1:
        section_title("Top 10 Modelos por Precio")
        top = precio_promedio_por_modelo(df, top_n=10)
        fig = px.bar(top, x="precio_promedio", y="model", orientation="h",
                     color="precio_promedio",
                     color_continuous_scale=[PALETTE["primary"], PALETTE["accent"]])
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          xaxis_title="Precio promedio (£)", yaxis_title="")
        st.plotly_chart(_apply_template(fig), use_container_width=True)

    with col2:
        section_title("Distribución por Combustible")
        dist = distribucion_combustible(df)
        col_porcentaje = dist.columns[-1]
        col_categoria = dist.columns[0]
        fig = px.pie(dist, values=col_porcentaje, names=col_categoria, hole=0.55,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()

    section_title("Precio vs Kilometraje", "Dispersión coloreada por año de fabricación.")
    sample = df.sample(min(3000, len(df)), random_state=42)
    fig = px.scatter(sample, x="mileage", y="price", color="year",
                     opacity=0.6, color_continuous_scale="Viridis",
                     hover_data=["model", "fuelType"])
    fig.update_layout(xaxis_title="Kilometraje", yaxis_title="Precio (£)")
    st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()

    section_title("Matriz de Correlación", "Mapa de calor de las correlaciones.")
    corr = correlaciones(df)
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        text=corr.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10, "color": "white"},
    ))
    st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()

    section_title("Box Plot del Precio por Tipo de Transmisión")
    fig = px.box(df, x="transmission", y="price",
                 color="transmission",
                 color_discrete_sequence=[PALETTE["primary"], PALETTE["primary_light"], PALETTE["accent"]])
    fig.update_layout(xaxis_title="Transmisión", yaxis_title="Precio (£)", showlegend=False)
    st.plotly_chart(_apply_template(fig), use_container_width=True)

    divider()
    footer()
