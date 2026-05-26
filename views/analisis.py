"""Vista de Analisis - Estadisticas y busqueda filtrada."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from core import (
    cargar_datos, pipeline_limpieza,
    aplicar_template, hero,
)


def render():
    df = pipeline_limpieza(cargar_datos())

    hero("Analisis Exploratorio",
         "Inspecciona los datos, revisa estadisticas y filtra registros "
         "segun tus criterios.",
         badges=["EDA", "Filtros", "Estadisticas"])

    st.markdown("### Estadisticas Descriptivas")
    st.dataframe(df.describe().round(2).T, use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Matriz de Correlacion")
    corr = df.select_dtypes(include=np.number).corr().round(2)
    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale="RdBu_r", zmin=-1, zmax=1,
        text=corr.values, texttemplate="%{text}",
        textfont={"size": 11, "color": "white"},
    ))
    fig.update_layout(height=460)
    st.plotly_chart(aplicar_template(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Busqueda Filtrada")
    col1, col2, col3 = st.columns(3)
    with col1:
        modelo = st.selectbox("Modelo",
            ["Todos"] + sorted(df["model"].unique().tolist()))
    with col2:
        combustible = st.selectbox("Combustible",
            ["Todos"] + sorted(df["fuelType"].unique().tolist()))
    with col3:
        precio_max = st.number_input("Precio maximo (£)",
            1000, 200000, 50000, step=1000)

    rango = st.slider("Rango de anios",
                      int(df["year"].min()), int(df["year"].max()),
                      (int(df["year"].min()), int(df["year"].max())))

    resultado = df.copy()
    if modelo != "Todos":
        resultado = resultado[resultado["model"] == modelo]
    if combustible != "Todos":
        resultado = resultado[resultado["fuelType"] == combustible]
    resultado = resultado[(resultado["year"] >= rango[0]) &
                          (resultado["year"] <= rango[1]) &
                          (resultado["price"] <= precio_max)]

    st.success(f"Se encontraron {len(resultado):,} registros")
    st.dataframe(resultado, use_container_width=True, hide_index=True)

    csv = resultado.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", data=csv,
                       file_name="bmw_filtrado.csv", mime="text/csv")
