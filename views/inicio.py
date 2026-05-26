"""Vista de Inicio - Dashboard con KPIs y graficos principales."""

import streamlit as st
import plotly.express as px
from core import (
    cargar_datos, pipeline_limpieza, kpis,
    precio_por_anio, aplicar_template,
    hero, kpi_card,
)


def render():
    df_crudo = cargar_datos()
    df = pipeline_limpieza(df_crudo)
    k = kpis(df)

    hero("Dashboard BMW",
         "Resumen del catalogo de vehiculos BMW usados. "
         "Usa el menu lateral para navegar.",
         badges=["Dashboard", f"{k['total']:,} vehiculos", "Streamlit"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Vehiculos", f"{k['total']:,}")
    with c2: kpi_card("Modelos", f"{k['modelos']}")
    with c3: kpi_card("Precio promedio", f"£ {k['precio_promedio']:,.0f}")
    with c4: kpi_card("Precio mediano", f"£ {k['precio_mediano']:,.0f}")

    c5, c6, c7, c8 = st.columns(4)
    with c5: kpi_card("Anio minimo", f"{k['anio_min']}")
    with c6: kpi_card("Anio maximo", f"{k['anio_max']}")
    with c7: kpi_card("Km promedio", f"{k['km_promedio']:,.0f}")
    with c8: kpi_card("Precio maximo", f"£ {df['price'].max():,.0f}")

    st.markdown("<hr/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Precio Promedio por Anio")
        serie = precio_por_anio(df)
        fig = px.area(serie, x="year", y="precio",
                      color_discrete_sequence=["#1C69D4"])
        fig.update_layout(xaxis_title="", yaxis_title="£", height=320)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

    with col2:
        st.markdown("### Distribucion por Combustible")
        dist = df["fuelType"].value_counts().reset_index()
        dist.columns = ["fuelType", "count"]
        fig = px.pie(dist, values="count", names="fuelType", hole=0.55,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=320)
        st.plotly_chart(aplicar_template(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Vista Previa del Dataset")
    st.dataframe(df.head(15), use_container_width=True, hide_index=True)
