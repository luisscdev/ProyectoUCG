"""Vista 'Acerca del Proyecto' — problemática, objetivos y metodología."""

import streamlit as st
from src.ui.helpers import hero, section_title, divider, footer


def render() -> None:
    hero(
        title="Acerca del Proyecto",
        subtitle=(
            "Contexto académico, problemática abordada, objetivos y metodología "
            "utilizada para construir esta aplicación."
        ),
        badges=["Académico", "UCG", "Maestría IA"],
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Contexto", "Problemática", "Objetivos", "Metodología"])

    with tab1:
        section_title("Contexto Académico")
        st.markdown(
            """
            **Universidad:** Universidad Casa Grande
            **Programa:** Maestría en Inteligencia Artificial y Ciencia de Datos
            **Asignatura:** Paradigmas de Programación para Inteligencia Artificial y Análisis de Datos
            **Período:** C2026 P1
            **Autor:** Luis Alexander Suárez Colimba

            El proyecto integra los contenidos del módulo en un caso aplicado de ciencia
            de datos, evidenciando el uso combinado de tres paradigmas de programación
            sobre un mismo problema real.
            """
        )

    with tab2:
        section_title("Problemática")
        st.markdown(
            """
            La fijación de precios en el mercado de vehículos usados depende, en muchos
            casos, de la experiencia subjetiva de tasadores y vendedores. Esta práctica
            genera diferencias importantes entre lo que pide un vendedor y lo que está
            dispuesto a pagar un comprador.

            A esta situación se suma un problema de acceso: las herramientas
            profesionales de valoración suelen ser costosas o están limitadas a empresas
            grandes. El usuario común no cuenta con un mecanismo gratuito que le permita
            ingresar las características de un vehículo y recibir una estimación apoyada
            en datos reales.

            En el ámbito formativo, muchos proyectos de ciencia de datos se resuelven con
            un único estilo de programación, desaprovechando que Python es un lenguaje
            multiparadigma.

            > **Pregunta de investigación:** ¿es posible construir una aplicación
            > accesible que estime el precio de un BMW usado con razonable precisión y, al
            > mismo tiempo, evidencie el uso combinado de los paradigmas orientado a
            > objetos, funcional y declarativo en un mismo proyecto?
            """
        )

    with tab3:
        section_title("Objetivos")
        st.markdown("#### Objetivo General")
        st.markdown(
            """
            Desarrollar una aplicación en Streamlit que prediga el precio de
            vehículos BMW usados mediante técnicas de aprendizaje automático
            supervisado, integrando los paradigmas orientado a objetos, funcional y
            declarativo.
            """
        )

        st.markdown("#### Objetivos Específicos")
        objetivos = [
            "Realizar el análisis exploratorio del dataset.",
            "Preparar los datos con codificación y escalado.",
            "Comparar varios algoritmos con LazyPredict y seleccionar el mejor.",
            "Diseñar una arquitectura modular con separación clara de paradigmas.",
            "Construir una interfaz Streamlit usable y publicarla en Streamlit Cloud.",
        ]
        for i, obj in enumerate(objetivos, 1):
            st.markdown(f"**{i}.** {obj}")

    with tab4:
        section_title("Metodología CRISP-DM")
        st.markdown(
            """
            El proyecto sigue la metodología **CRISP-DM** (Cross-Industry Standard
            Process for Data Mining), un estándar de facto en proyectos de ciencia
            de datos. Sus seis fases son:
            """
        )
        fases = [
            ("1. Comprensión del negocio",
             "Definir el alcance, los objetivos y la pregunta que debe responder el modelo."),
            ("2. Comprensión de los datos",
             "Estadísticas descriptivas, distribuciones, matriz de correlación."),
            ("3. Preparación de los datos",
             "Limpieza, codificación de variables categóricas, escalado."),
            ("4. Modelado",
             "Comparación con LazyPredict y ajuste fino con GridSearchCV."),
            ("5. Evaluación",
             "Métricas R², RMSE y MAE sobre el conjunto de prueba."),
            ("6. Despliegue",
             "Interfaz Streamlit y publicación en Streamlit Cloud."),
        ]
        for titulo, descripcion in fases:
            st.markdown(
                f"""
                <div class="card">
                    <strong style="color: #5BA4F5;">{titulo}</strong><br>
                    <span style="color: #A8B3C7;">{descripcion}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    divider()
    footer()
