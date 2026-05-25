"""Vista 'Exploración' — Tabla, estadísticas y búsqueda filtrada."""

import streamlit as st
from src.ui.helpers import hero, section_title, divider, footer, kpi_card
from src.ui.data_loader import cargar_dataset, cargar_dataset_crudo
from src.declarative import resumen_descriptivo, correlaciones, buscar_por_filtros


def render() -> None:
    df = cargar_dataset()
    df_crudo = cargar_dataset_crudo()

    hero(
        title="Exploración del Dataset",
        subtitle="Inspecciona los datos, revisa estadísticas y filtra registros según tus criterios.",
        badges=["Exploración", "Filtros"],
    )

    # Calidad rápida
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Filas originales", f"{len(df_crudo):,}")
    with c2:
        kpi_card("Filas limpias", f"{len(df):,}")
    with c3:
        kpi_card("Valores nulos", f"{df_crudo.isnull().sum().sum()}")
    with c4:
        kpi_card("Variables", f"{df.shape[1]}")

    divider()

    section_title("Vista Previa")
    n_filas = st.slider("Filas a mostrar", 5, 100, 15)
    st.dataframe(df.head(n_filas), use_container_width=True, hide_index=True)

    divider()

    section_title("Estadísticas Descriptivas")
    st.dataframe(resumen_descriptivo(df), use_container_width=True)

    divider()

    section_title("Matriz de Correlación")
    st.dataframe(
        correlaciones(df).style.background_gradient(cmap="RdBu_r", vmin=-1, vmax=1),
        use_container_width=True,
    )

    divider()

    section_title("Búsqueda Filtrada")
    col1, col2, col3 = st.columns(3)
    with col1:
        modelo = st.selectbox("Modelo", ["Todos"] + sorted(df["model"].unique().tolist()))
    with col2:
        combustible = st.selectbox("Combustible", ["Todos"] + sorted(df["fuelType"].unique().tolist()))
    with col3:
        precio_max = st.number_input("Precio máximo (£)", min_value=1000, max_value=200_000, value=50_000, step=1000)

    rango_anios = st.slider(
        "Rango de años",
        int(df["year"].min()), int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max())),
    )

    resultado = buscar_por_filtros(
        df,
        modelo=None if modelo == "Todos" else modelo,
        anio_min=rango_anios[0],
        anio_max=rango_anios[1],
        combustible=None if combustible == "Todos" else combustible,
        precio_max=precio_max,
    )
    st.success(f"Se encontraron {len(resultado):,} registros.")
    st.dataframe(resultado, use_container_width=True, hide_index=True)

    # Botón de descarga
    csv = resultado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar resultados (CSV)",
        data=csv,
        file_name="bmw_filtrado.csv",
        mime="text/csv",
    )

    footer()
