"""Vista 'Predicción' — formulario para estimar el precio de un BMW."""

from pathlib import Path
import streamlit as st

from src.ui.helpers import hero, section_title, divider, footer, kpi_card
from src.ui.data_loader import cargar_dataset
from src.domain import Vehiculo, PredictorPrecio


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "predictor_bmw.joblib"


def render() -> None:
    df = cargar_dataset()
    predictor = PredictorPrecio(MODEL_PATH if MODEL_PATH.exists() else None)
    modo_demo = not predictor.esta_entrenado()

    hero(
        title="Predicción de Precio",
        subtitle=(
            "Ingresa las características del vehículo y obtén una estimación "
            "del precio basada en el modelo entrenado."
        ),
        badges=["Machine Learning", "Regresión"] + (["Modo demostración"] if modo_demo else ["Modelo entrenado"]),
    )

    if modo_demo:
        st.info(
            "🔧 El modelo aún no ha sido entrenado. La predicción actual usa una "
            "**heurística simple** con fines pedagógicos. Cuando ejecutes el "
            "entrenamiento con LazyPredict y guardes el `.joblib` en la carpeta "
            "`models/`, la app usará automáticamente el modelo real."
        )

    section_title("Características del Vehículo")

    col1, col2, col3 = st.columns(3)

    modelos = sorted(df["model"].unique().tolist())
    transmisiones = sorted(df["transmission"].unique().tolist())
    combustibles = sorted(df["fuelType"].unique().tolist())

    with col1:
        modelo = st.selectbox("Modelo BMW", modelos, index=modelos.index("3 Series") if "3 Series" in modelos else 0)
        anio = st.slider("Año de fabricación", 1996, 2024, 2018)
        kilometraje = st.number_input("Kilometraje", min_value=0, max_value=300_000, value=25_000, step=1000)

    with col2:
        transmision = st.selectbox("Transmisión", transmisiones)
        combustible = st.selectbox("Combustible", combustibles, index=combustibles.index("Diesel") if "Diesel" in combustibles else 0)
        tamano_motor = st.slider("Tamaño del motor (L)", 0.5, 6.6, 2.0, step=0.1)

    with col3:
        mpg = st.slider("Consumo (mpg)", 10.0, 200.0, 55.0, step=0.5)
        impuesto = st.number_input("Impuesto anual (£)", min_value=0, max_value=600, value=145, step=5)

    divider()

    if st.button("Calcular precio estimado", use_container_width=True, type="primary"):
        try:
            v = Vehiculo(
                modelo=modelo,
                anio=anio,
                kilometraje=int(kilometraje),
                transmision=transmision,
                combustible=combustible,
                tamano_motor=float(tamano_motor),
                mpg=float(mpg),
                impuesto=int(impuesto),
            )
            precio = predictor.predecir(v)

            st.markdown(f"""
                <div class="hero" style="text-align: center; margin-top: 24px;">
                    <div style="color: #6B7388; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em;">
                        Precio Estimado
                    </div>
                    <div class="hero-title" style="font-size: 4rem; margin: 16px 0;">
                        £ {precio:,.0f}
                    </div>
                    <div style="color: #A8B3C7;">
                        {v}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # KPIs de contexto
            c1, c2, c3 = st.columns(3)
            with c1:
                kpi_card("Antigüedad", f"{v.antiguedad()} años")
            with c2:
                kpi_card("Premium", "Sí" if v.es_premium() else "No")
            with c3:
                kpi_card("Confianza", "Demostración" if modo_demo else "Alta")

        except ValueError as e:
            st.error(f"Datos inválidos: {e}")

    divider()
    footer()
