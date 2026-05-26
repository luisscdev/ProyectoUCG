"""Vista de Limpieza - Pipeline de preprocesamiento paso a paso."""

import streamlit as st
import pandas as pd
import plotly.express as px
from core import (
    cargar_datos, limpiar_espacios, quitar_duplicados,
    filtrar_precio_valido, agregar_antiguedad,
    aplicar_template, hero, kpi_card,
)


def render():
    df_crudo = cargar_datos()

    hero("Limpieza de Datos",
         "Proceso de limpieza y transformacion del dataset antes de modelar.",
         badges=["Limpieza", "Pipeline funcional"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Filas originales", f"{len(df_crudo):,}")
    with c2: kpi_card("Nulos totales", f"{int(df_crudo.isnull().sum().sum())}")
    with c3: kpi_card("Duplicados", f"{int(df_crudo.duplicated().sum())}")
    with c4: kpi_card("Columnas", f"{df_crudo.shape[1]}")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Pasos del Pipeline de Limpieza")

    pasos = [
        ("1. Eliminar espacios en blanco",
         "Limpiamos espacios al inicio/fin de la columna 'model'."),
        ("2. Quitar duplicados",
         "Eliminamos registros identicos para evitar sesgos."),
        ("3. Filtrar precios validos",
         "Conservamos vehiculos con precio entre £500 y £200.000."),
        ("4. Crear variable derivada",
         "Calculamos la antiguedad del vehiculo (2024 - anio)."),
    ]
    for titulo, desc in pasos:
        st.markdown(f"""
            <div class="card">
                <div style="font-weight: 700; color: #1C69D4; font-size: 1.05rem;">{titulo}</div>
                <div style="color: #475569; margin-top: 4px;">{desc}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Resultado Paso a Paso")
    df1 = limpiar_espacios(df_crudo)
    df2 = quitar_duplicados(df1)
    df3 = filtrar_precio_valido(df2)
    df4 = agregar_antiguedad(df3)

    etapas = pd.DataFrame({
        "Etapa": ["1. Crudo", "2. Sin espacios", "3. Sin duplicados",
                  "4. Precio valido", "5. + antiguedad"],
        "Filas": [len(df_crudo), len(df1), len(df2), len(df3), len(df4)],
    })
    fig = px.bar(etapas, x="Etapa", y="Filas", text="Filas",
                 color="Filas",
                 color_continuous_scale=["#1C69D4", "#5BA4F5"])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(height=380, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(aplicar_template(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Valores Nulos por Columna")
    nulos = df_crudo.isnull().sum().reset_index()
    nulos.columns = ["Columna", "Nulos"]
    fig = px.bar(nulos, x="Columna", y="Nulos", color="Nulos",
                 color_continuous_scale=["#2ECC71", "#E74C3C"])
    fig.update_layout(height=340, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(aplicar_template(fig), use_container_width=True)

    if df_crudo.isnull().sum().sum() == 0:
        st.success("El dataset no tiene valores nulos. Excelente!")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Dataset Despues de la Limpieza")
    st.dataframe(df4.head(20), use_container_width=True, hide_index=True)
