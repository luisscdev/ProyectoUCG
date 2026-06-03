"""Vista de Predicción - LazyPredict (imagen) + prediccion con modelo preentrenado."""

from pathlib import Path
import streamlit as st
from core import (
    cargar_datos, pipeline_limpieza,
    Vehiculo, PredictorPrecio,
    hero, kpi_card,
)

RUTA_RANKING = Path("assets/screenshots/caputra_mejora_alogritmos.png")


def render():
    df = pipeline_limpieza(cargar_datos())
    predictor = PredictorPrecio()
    modelo_listo = predictor.esta_entrenado()
    nombre_modelo = predictor.nombre_modelo()

    hero("Predicción de Precio",
         "Sistema entrenado automaticamente con el mejor algoritmo seleccionado "
         "por LazyPredict. La aplicacion esta lista para predecir.",
         badges=["Machine Learning", "LazyPredict",
                 f"Modelo activo: {nombre_modelo}" if modelo_listo
                 else "Sin modelo entrenado"])

    tab1, tab2 = st.tabs([
        "📊 Ránking de Algorítmos (LazyPredict)",
        "🎯 Predecir Precio",
    ])

    # Franja azul con el nombre del algoritmo entrenado (visible en ambas pestañas)
    franja_algoritmo = f"""
        <div style="
            background: linear-gradient(135deg, #1C69D4 0%, #2A7BE8 100%);
            color: white;
            padding: 18px 28px;
            border-radius: 12px;
            margin: 16px 0 24px 0;
            box-shadow: 0 4px 14px rgba(28, 105, 212, 0.35);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        ">
            <div style="display:flex; align-items:center; gap:14px;">
                <span style="font-size: 1.8rem;">🤖</span>
                <div>
                    <div style="
                        font-size: 0.78rem;
                        letter-spacing: 0.12em;
                        text-transform: uppercase;
                        opacity: 0.9;
                    ">
                        Modelo entrenado con
                    </div>
                    <div style="
                        font-size: 1.5rem;
                        font-weight: 800;
                        margin-top: 2px;
                        line-height: 1.1;
                    ">
                        {nombre_modelo}
                    </div>
                </div>
            </div>
            <div style="
                background: rgba(255,255,255,0.18);
                padding: 6px 14px;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            ">
                {'✅ Activo' if modelo_listo else '⚠️ Sin entrenar'}
            </div>
        </div>
    """

    # ============================================================
    # TAB 1: SOLO LA IMAGEN DEL RANKING
    # ============================================================
    with tab1:
        st.markdown(franja_algoritmo, unsafe_allow_html=True)
        if RUTA_RANKING.exists():
            st.image(str(RUTA_RANKING), use_container_width=True)
        else:
            st.warning("No se encontró la imagen del ranking en "
                       "`assets/screenshots/caputra_mejora_alogritmos.png`")

    # ============================================================
    # TAB 2: PREDECIR
    # ============================================================
    with tab2:
        st.markdown(franja_algoritmo, unsafe_allow_html=True)

        if not modelo_listo:
            st.error(
                "⚠️ El modelo aun no esta disponible. Ejecuta una sola vez el "
                "script de entrenamiento desde la terminal:\n\n"
                "```bash\npython entrenar_modelo.py\n```"
            )

        st.markdown("### Características del Vehículo")

        col1, col2, col3 = st.columns(3)
        modelos = sorted(df["model"].unique().tolist())
        transmisiones = sorted(df["transmission"].unique().tolist())
        combustibles = sorted(df["fuelType"].unique().tolist())

        with col1:
            modelo = st.selectbox("Modelo BMW", modelos,
                index=modelos.index("3 Series") if "3 Series" in modelos else 0)
            anio = st.slider("Año", 1996, 2024, 2018)
            kilometraje = st.number_input("Kilometraje",
                0, 300000, 25000, step=1000)

        with col2:
            transmision = st.selectbox("Transmisión", transmisiones)
            combustible = st.selectbox("Combustible", combustibles,
                index=combustibles.index("Diesel") if "Diesel" in combustibles else 0)
            tamano_motor = st.slider("Tamaño motor (L)",
                0.5, 6.6, 2.0, step=0.1)

        with col3:
            mpg = st.slider("Consumo (mpg)", 10.0, 200.0, 55.0, step=0.5)
            impuesto = st.number_input("Impuesto (USD)", 0, 780, 190, step=5)

        st.markdown("<hr/>", unsafe_allow_html=True)

        if st.button("🎯 Calcular precio estimado",
                     use_container_width=True, key="predict_btn", type="primary"):
            v = Vehiculo(modelo, anio, int(kilometraje), transmision,
                         combustible, float(tamano_motor),
                         float(mpg), int(impuesto))
            precio = predictor.predecir(v)
            algoritmo = predictor.nombre_modelo()

            st.markdown(f"""
                <div class="hero" style="text-align: center;">
                    <div style="color: #64748B; font-size: 0.9rem;
                                text-transform: uppercase; letter-spacing: 0.1em;">
                        Precio Estimado
                    </div>
                    <div class="hero-title" style="font-size: 4rem; margin: 16px 0;">
                        $ {precio:,.0f}
                    </div>
                    <div style="color: #475569;">{v}</div>
                    <div style="margin-top: 16px;">
                        <span class="badge">Algoritmo usado: {algoritmo}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1: kpi_card("Algoritmo",
                              algoritmo.replace("Regressor", ""))
            with c2: kpi_card("Antigüedad", f"{v.antiguedad()} anios")
            with c3: kpi_card("Premium", "Sí" if v.es_premium() else "No")
            with c4: kpi_card("Fuente",
                              "Modelo ML" if modelo_listo else "Heurística")
