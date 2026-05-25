"""
Carga del dataset con caché de Streamlit.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

# El dataset vive en data/ — copia local generada al iniciar el proyecto.
DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "dataset_bmw.csv"
FALLBACK_PATH = Path(__file__).resolve().parents[2] / "docs" / "dataset_bmw.csv"


@st.cache_data(show_spinner=False)
def cargar_dataset() -> pd.DataFrame:
    """Carga el dataset de vehículos BMW y aplica preprocesamiento estándar."""
    from src.functional import pipeline_default

    ruta = DATASET_PATH if DATASET_PATH.exists() else FALLBACK_PATH
    df = pd.read_csv(ruta)
    return pipeline_default(df)


@st.cache_data(show_spinner=False)
def cargar_dataset_crudo() -> pd.DataFrame:
    """Devuelve el dataset sin preprocesar (para mostrar comparaciones)."""
    ruta = DATASET_PATH if DATASET_PATH.exists() else FALLBACK_PATH
    return pd.read_csv(ruta)
