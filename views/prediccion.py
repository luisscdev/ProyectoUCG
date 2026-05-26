"""Vista de Prediccion - LazyPredict + entrenamiento + estimacion."""

import streamlit as st
import plotly.express as px
from core import (
    cargar_datos, pipeline_limpieza,
    Vehiculo, PredictorPrecio,
    comparar_modelos_lazypredict, entrenar_y_guardar_modelo,
    obtener_mejor_modelo, aplicar_template,
    hero, kpi_card,
)


def render():
    df = pipeline_limpieza(cargar_datos())
    predictor = PredictorPrecio()
    modelo_listo = predictor.esta_entrenado()

    hero("Prediccion de Precio",
         "Compara modelos con LazyPredict, entrena el mejor y predice el "
         "precio de un BMW usado.",
         badges=["Machine Learning", "LazyPredict",
                 "Modelo entrenado" if modelo_listo else "Sin modelo"])

    tab1, tab2 = st.tabs(["⚙️ Comparar y Entrenar Modelos",
                           "🎯 Predecir Precio"])

    # ------ TAB 1: COMPARAR Y ENTRENAR ------
    with tab1:
        st.markdown("### Paso 1 — Comparar Algoritmos con LazyPredict")
        st.markdown(
            "LazyPredict entrena automaticamente varios algoritmos de "
            "regresion sobre un sample del dataset y devuelve un ranking "
            "ordenado por R² ajustado."
        )

        if st.button("🚀 Ejecutar LazyPredict",
                     use_container_width=True, key="run_lazy"):
            with st.spinner("Comparando modelos... esto puede tardar 1-2 minutos."):
                ranking = comparar_modelos_lazypredict(df)
                st.session_state["ranking_lazy"] = ranking

        if "ranking_lazy" in st.session_state:
            ranking = st.session_state["ranking_lazy"]
            st.success(f"✅ Se evaluaron {len(ranking)} modelos.")
            st.dataframe(ranking.head(10),
                         use_container_width=True, hide_index=True)

            top5 = ranking.head(5).copy()
            col_r2 = ("Adjusted R-Squared" if "Adjusted R-Squared" in top5.columns
                      else top5.columns[1])
            fig = px.bar(top5, x=col_r2, y="Modelo", orientation="h",
                         color=col_r2,
                         color_continuous_scale=["#1C69D4", "#BB8FCE"])
            fig.update_layout(yaxis={"categoryorder": "total ascending"},
                              title="Top 5 modelos por R² ajustado",
                              height=360, coloraxis_showscale=False)
            st.plotly_chart(aplicar_template(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("### Paso 2 — Entrenar Automaticamente el Mejor Modelo")
        st.markdown(
            "Se entrenara sobre todo el dataset el modelo que mejor "
            "R² ajustado obtuvo en LazyPredict."
        )

        ranking_disponible = "ranking_lazy" in st.session_state
        if ranking_disponible:
            mejor, estado = obtener_mejor_modelo(st.session_state["ranking_lazy"])
            if estado == "ok":
                st.info(f"🏆 Modelo recomendado por LazyPredict: **{mejor}**")
            else:
                st.warning(
                    f"⚠️ El mejor modelo de LazyPredict no es entrenable "
                    f"directamente. Se usara **{mejor}** como respaldo."
                )
        else:
            mejor = "RandomForestRegressor"
            st.info(
                "💡 Ejecuta primero LazyPredict (Paso 1) para que el sistema "
                "elija automaticamente el mejor modelo. Si lo entrenas sin "
                f"ejecutar antes, se usara **{mejor}** por defecto."
            )

        if st.button(f"🎓 Entrenar y guardar el mejor modelo ({mejor})",
                     use_container_width=True, key="train_btn", type="primary"):
            with st.spinner(f"Entrenando {mejor}..."):
                _, met = entrenar_y_guardar_modelo(df, mejor)
                st.session_state["metricas_modelo"] = met
            st.success(f"✅ Modelo {mejor} entrenado y guardado.")
            st.balloons()
            st.rerun()

        if modelo_listo or "metricas_modelo" in st.session_state:
            met = st.session_state.get("metricas_modelo")
            if met:
                st.markdown("#### Metricas del Modelo Entrenado")
                m1, m2, m3, m4 = st.columns(4)
                with m1: kpi_card("R²", f"{met['r2']:.4f}")
                with m2: kpi_card("MAE (£)", f"{met['mae']:,.0f}")
                with m3: kpi_card("RMSE (£)", f"{met['rmse']:,.0f}")
                with m4: kpi_card("Modelo", met["modelo"].replace("Regressor", ""))
            else:
                st.info("Modelo cargado desde disco. "
                        "Para ver metricas, vuelve a entrenarlo.")

    # ------ TAB 2: PREDECIR ------
    with tab2:
        if not modelo_listo:
            st.warning(
                "⚠️ Aun no hay un modelo entrenado. Ve a la pestania anterior "
                "y ejecuta LazyPredict + Entrenar. Mientras tanto se usara una "
                "formula heuristica de respaldo."
            )
        else:
            st.success(
                f"✅ Modelo activo: **{predictor.nombre_modelo()}** "
                f"(cargado desde `modelo_bmw.joblib`)."
            )

        st.markdown("### Caracteristicas del Vehiculo")

        col1, col2, col3 = st.columns(3)
        modelos = sorted(df["model"].unique().tolist())
        transmisiones = sorted(df["transmission"].unique().tolist())
        combustibles = sorted(df["fuelType"].unique().tolist())

        with col1:
            modelo = st.selectbox("Modelo BMW", modelos,
                index=modelos.index("3 Series") if "3 Series" in modelos else 0)
            anio = st.slider("Anio", 1996, 2024, 2018)
            kilometraje = st.number_input("Kilometraje",
                0, 300000, 25000, step=1000)

        with col2:
            transmision = st.selectbox("Transmision", transmisiones)
            combustible = st.selectbox("Combustible", combustibles,
                index=combustibles.index("Diesel") if "Diesel" in combustibles else 0)
            tamano_motor = st.slider("Tamanio motor (L)",
                0.5, 6.6, 2.0, step=0.1)

        with col3:
            mpg = st.slider("Consumo (mpg)", 10.0, 200.0, 55.0, step=0.5)
            impuesto = st.number_input("Impuesto (£)", 0, 600, 145, step=5)

        st.markdown("<hr/>", unsafe_allow_html=True)

        if st.button("Calcular precio estimado",
                     use_container_width=True, key="predict_btn"):
            v = Vehiculo(modelo, anio, int(kilometraje), transmision,
                         combustible, float(tamano_motor),
                         float(mpg), int(impuesto))
            precio = predictor.predecir(v)
            nombre_algoritmo = predictor.nombre_modelo()

            st.markdown(f"""
                <div class="hero" style="text-align: center;">
                    <div style="color: #64748B; font-size: 0.9rem;
                                text-transform: uppercase; letter-spacing: 0.1em;">
                        Precio Estimado
                    </div>
                    <div class="hero-title" style="font-size: 4rem; margin: 16px 0;">
                        £ {precio:,.0f}
                    </div>
                    <div style="color: #475569;">{v}</div>
                    <div style="margin-top: 16px;">
                        <span class="badge">Algoritmo usado: {nombre_algoritmo}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1: kpi_card("Algoritmo",
                              nombre_algoritmo.replace("Regressor", ""))
            with c2: kpi_card("Antiguedad", f"{v.antiguedad()} anios")
            with c3: kpi_card("Premium", "Si" if v.es_premium() else "No")
            with c4: kpi_card("Fuente",
                              "Modelo ML" if modelo_listo else "Heuristica")
