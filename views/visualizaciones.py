"""Vista de Visualizaciones - Graficos interactivos en pestanias."""

import streamlit as st
import plotly.express as px
from core import (
    cargar_datos, pipeline_limpieza, precio_por_anio, top_modelos,
    aplicar_template, hero,
)


def render():
    df = pipeline_limpieza(cargar_datos())

    hero("Visualizaciones Interactivas",
         "Graficos dinamicos organizados por categoria. "
         "Usa las pestanias para navegar.",
         badges=["Plotly", "Interactivo", "8 graficos"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribuciones", "🔄 Relaciones",
        "🏆 Rankings", "📈 Tendencias",
    ])

    # ------ TAB 1: DISTRIBUCIONES ------
    with tab1:
        st.markdown("### Distribucion del Precio")
        fig = px.histogram(df, x="price", nbins=60, opacity=0.85,
                           color_discrete_sequence=["#1C69D4"])
        fig.update_layout(xaxis_title="Precio (£)", yaxis_title="Frecuencia",
                          bargap=0.02, height=380)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Precio por Transmision")
            fig = px.box(df, x="transmission", y="price",
                         color="transmission",
                         color_discrete_sequence=["#1C69D4", "#5BA4F5", "#BB8FCE"])
            fig.update_layout(xaxis_title="", yaxis_title="Precio (£)",
                              showlegend=False, height=400)
            st.plotly_chart(aplicar_template(fig), use_container_width=True)

        with col2:
            st.markdown("### Precio por Combustible")
            fig = px.violin(df, x="fuelType", y="price",
                            color="fuelType", box=True, points=False,
                            color_discrete_sequence=["#1C69D4", "#5BA4F5",
                                                     "#BB8FCE", "#2ECC71", "#F1C40F"])
            fig.update_layout(xaxis_title="", yaxis_title="Precio (£)",
                              showlegend=False, height=400)
            st.plotly_chart(aplicar_template(fig), use_container_width=True)

    # ------ TAB 2: RELACIONES ------
    with tab2:
        st.markdown("### Precio vs Kilometraje")
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(sample, x="mileage", y="price", color="year",
                         opacity=0.6, color_continuous_scale="Viridis",
                         hover_data=["model", "fuelType"])
        fig.update_layout(xaxis_title="Kilometraje",
                          yaxis_title="Precio (£)", height=460)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("### Tamanio del Motor vs Precio Promedio")
        motor = (df.groupby("engineSize", as_index=False)
                   .agg(precio=("price", "mean"), unidades=("price", "count")))
        fig = px.scatter(motor, x="engineSize", y="precio", size="unidades",
                         color="precio", color_continuous_scale="Plasma",
                         hover_data={"unidades": True})
        fig.update_layout(xaxis_title="Tamanio del motor (L)",
                          yaxis_title="Precio promedio (£)", height=460)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

    # ------ TAB 3: RANKINGS ------
    with tab3:
        st.markdown("### Top 10 Modelos BMW por Precio Promedio")
        top = top_modelos(df, n=10)
        fig = px.bar(top, x="precio", y="model", orientation="h",
                     color="precio",
                     color_continuous_scale=["#1C69D4", "#BB8FCE"], text="precio")
        fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          xaxis_title="Precio promedio (£)", yaxis_title="",
                          height=480, coloraxis_showscale=False)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Distribucion por Combustible")
            dist = df["fuelType"].value_counts().reset_index()
            dist.columns = ["fuelType", "count"]
            fig = px.pie(dist, values="count", names="fuelType", hole=0.55,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_layout(height=420)
            st.plotly_chart(aplicar_template(fig), use_container_width=True)

        with col_b:
            st.markdown("### Distribucion por Transmision")
            dist_t = df["transmission"].value_counts().reset_index()
            dist_t.columns = ["transmission", "count"]
            fig = px.bar(dist_t, x="transmission", y="count",
                         color="count",
                         color_continuous_scale=["#1C69D4", "#BB8FCE"],
                         text="count")
            fig.update_traces(texttemplate="%{text:,}", textposition="outside")
            fig.update_layout(xaxis_title="", yaxis_title="Cantidad",
                              showlegend=False, height=420,
                              coloraxis_showscale=False)
            st.plotly_chart(aplicar_template(fig), use_container_width=True)

    # ------ TAB 4: TENDENCIAS ------
    with tab4:
        st.markdown("### Evolucion del Precio Promedio por Anio")
        serie = precio_por_anio(df)
        fig = px.line(serie, x="year", y="precio", markers=True,
                      color_discrete_sequence=["#5BA4F5"])
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        fig.update_layout(xaxis_title="Anio",
                          yaxis_title="Precio promedio (£)", height=440)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("### Cantidad de Vehiculos por Anio")
        fig = px.bar(serie, x="year", y="unidades", color="unidades",
                     color_continuous_scale=["#1C69D4", "#BB8FCE"])
        fig.update_layout(xaxis_title="Anio", yaxis_title="Cantidad",
                          showlegend=False, height=440,
                          coloraxis_showscale=False)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)
