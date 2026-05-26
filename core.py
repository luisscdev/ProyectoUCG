"""
core.py - Modulo central del proyecto LS AutoPredict.

Contiene:
  - Constantes (rutas, columnas, paleta)
  - CSS personalizado
  - Clases POO (Vehiculo, PredictorPrecio)
  - Funciones puras del paradigma funcional
  - Queries declarativas con Pandas
  - Pipeline de Machine Learning (LazyPredict + Scikit-learn)
  - Helpers de UI (kpi_card, hero)

Cada vista de la carpeta views/ importa lo que necesita desde aqui.
"""

from __future__ import annotations
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Machine Learning
from sklearn.ensemble import (
    RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor,
)
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# ============================================================
# CONSTANTES
# ============================================================
RUTA_MODELO = Path("modelo_bmw.joblib")
RUTA_ICONO = Path("assets/ls_autopredict_icono.svg")
RUTA_LOGO = Path("assets/ls_autopredict_logo.png")
RUTA_PERFIL = Path("assets/perfil.png")


COLUMNAS_X = ["model", "year", "mileage", "transmission",
              "fuelType", "engineSize", "mpg", "tax"]

# Modelos que NO aceptan el argumento random_state
SIN_RANDOM_STATE = {
    "LinearRegression", "BayesianRidge", "OrthogonalMatchingPursuit",
    "HuberRegressor", "SVR", "KNeighborsRegressor",
}


# ============================================================
# CSS PERSONALIZADO
# ============================================================
CUSTOM_CSS = """
<style>
.stApp { background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%); }
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; color: #0F172A; }

h1 {
    font-weight: 700 !important;
    background: linear-gradient(135deg, #1C69D4 0%, #2A7BE8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
h2, h3 { color: #0F172A !important; font-weight: 600 !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8FAFC 0%, #EFF4FB 100%);
    border-right: 1px solid #E2E8F0;
}

.kpi {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 6px 0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    transition: all 0.2s ease;
}
.kpi:hover {
    border-color: #1C69D4;
    box-shadow: 0 4px 16px rgba(28, 105, 212, 0.12);
    transform: translateY(-1px);
}
.kpi-label {
    font-size: 0.78rem; color: #64748B;
    text-transform: uppercase; letter-spacing: 0.08em;
    font-weight: 600; margin-bottom: 6px;
}
.kpi-value { font-size: 1.8rem; font-weight: 700; color: #1C69D4; line-height: 1.1; }

.card {
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-left: 4px solid #1C69D4;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

.hero {
    padding: 36px 28px;
    background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 70%);
    border-radius: 20px;
    border: 1px solid #DBEAFE;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.hero-title {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(135deg, #0F172A 0%, #1C69D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
}
.hero-subtitle { font-size: 1.05rem; color: #475569; margin-top: 8px; }

.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.05em; background: #DBEAFE;
    color: #1C69D4; border: 1px solid #BFDBFE;
    margin-right: 6px; margin-bottom: 12px;
}

.stButton > button {
    background: linear-gradient(135deg, #1C69D4 0%, #2A7BE8 100%);
    color: white !important; border: none; border-radius: 10px;
    padding: 10px 20px; font-weight: 600;
    box-shadow: 0 4px 12px rgba(28,105,212,0.25);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(28,105,212,0.4);
}

.bio-avatar {
    width: 140px; height: 140px; border-radius: 50%;
    background: linear-gradient(135deg, #1C69D4, #5BA4F5);
    display: flex; align-items: center; justify-content: center;
    font-size: 4rem; font-weight: 700; color: white;
    margin: 0 auto; border: 4px solid #FFFFFF;
    box-shadow: 0 8px 24px rgba(28, 105, 212, 0.25);
}

hr {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, #DBEAFE, transparent);
    margin: 28px 0;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #F1F5F9;
    border-radius: 10px;
    padding: 8px 18px;
    border: 1px solid #E2E8F0;
    color: #475569;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1C69D4, #2A7BE8) !important;
    color: white !important;
    border-color: transparent !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
button[kind="header"] svg {
    color: #1C69D4 !important;
    fill: #1C69D4 !important;
    width: 22px !important;
    height: 22px !important;
}


</style>
"""


def inject_css():
    """Inyecta el CSS personalizado en la app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# PLOTLY THEME
# ============================================================
PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#0F172A", family="Inter, sans-serif"),
    colorway=["#1C69D4", "#5BA4F5", "#3B82F6", "#60A5FA", "#1E40AF", "#93C5FD"],
    xaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
    yaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
    hoverlabel=dict(bgcolor="#FFFFFF", font_color="#0F172A", bordercolor="#1C69D4"),
)


def aplicar_template(fig):
    """Aplica el template visual a una figura de plotly."""
    fig.update_layout(**PLOTLY_TEMPLATE)
    return fig


# ============================================================
# PARADIGMA ORIENTADO A OBJETOS (POO)
# ============================================================
class Vehiculo:
    """Clase que representa un vehiculo BMW (POO)."""

    def __init__(self, modelo, anio, kilometraje, transmision,
                 combustible, tamano_motor, mpg, impuesto=145):
        self.modelo = modelo
        self.anio = anio
        self.kilometraje = kilometraje
        self.transmision = transmision
        self.combustible = combustible
        self.tamano_motor = tamano_motor
        self.mpg = mpg
        self.impuesto = impuesto

    def antiguedad(self, anio_ref=2024):
        return max(anio_ref - self.anio, 0)

    def es_premium(self):
        modelos_top = {"7 Series", "8 Series", "X7", "M5", "X6"}
        return self.tamano_motor >= 3.0 or self.modelo in modelos_top

    def to_df(self):
        return pd.DataFrame([{
            "model": self.modelo, "year": self.anio,
            "mileage": self.kilometraje,
            "transmission": self.transmision,
            "fuelType": self.combustible,
            "engineSize": self.tamano_motor,
            "mpg": self.mpg, "tax": self.impuesto,
        }])

    def __str__(self):
        return (f"BMW {self.modelo} {self.anio} - "
                f"{self.kilometraje:,} mi - {self.combustible}")


class PredictorPrecio:
    """Estima el precio de un vehiculo (POO).

    Carga automaticamente el modelo entrenado si existe.
    Si no existe, usa una formula heuristica de respaldo.
    """

    def __init__(self):
        self.modelo_ml = None
        if RUTA_MODELO.exists():
            try:
                self.modelo_ml = joblib.load(RUTA_MODELO)
            except Exception:
                self.modelo_ml = None

    def esta_entrenado(self):
        return self.modelo_ml is not None

    def nombre_modelo(self):
        if self.modelo_ml is None:
            return "Heuristica de respaldo"
        try:
            return self.modelo_ml.named_steps["regressor"].__class__.__name__
        except Exception:
            return self.modelo_ml.__class__.__name__

    def predecir(self, vehiculo):
        if self.modelo_ml is None:
            base = 30000
            base -= (2024 - vehiculo.anio) * 1500
            base -= (vehiculo.kilometraje / 1000) * 35
            base += (vehiculo.tamano_motor - 2.0) * 2500
            if vehiculo.es_premium():
                base += 5000
            return max(base, 1500)
        return float(self.modelo_ml.predict(vehiculo.to_df())[0])


# ============================================================
# PARADIGMA FUNCIONAL (funciones puras)
# ============================================================
def limpiar_espacios(df):
    out = df.copy()
    out["model"] = out["model"].astype(str).str.strip()
    return out

def quitar_duplicados(df):
    return df.drop_duplicates().reset_index(drop=True)

def filtrar_precio_valido(df, minimo=500, maximo=200000):
    return df[(df["price"] >= minimo) &
              (df["price"] <= maximo)].reset_index(drop=True)

def agregar_antiguedad(df, anio_ref=2024):
    return df.assign(antiguedad=lambda d: anio_ref - d["year"])

def pipeline_limpieza(df):
    """Composicion funcional con .pipe()"""
    return (df.pipe(limpiar_espacios)
              .pipe(quitar_duplicados)
              .pipe(filtrar_precio_valido)
              .pipe(agregar_antiguedad))


# ============================================================
# PARADIGMA DECLARATIVO (queries con Pandas)
# ============================================================
def kpis(df):
    return {
        "total": len(df),
        "modelos": df["model"].nunique(),
        "precio_promedio": df["price"].mean(),
        "precio_mediano": df["price"].median(),
        "anio_min": int(df["year"].min()),
        "anio_max": int(df["year"].max()),
        "km_promedio": df["mileage"].mean(),
    }

def precio_por_anio(df):
    return (df.groupby("year", as_index=False)
              .agg(precio=("price", "mean"), unidades=("price", "count"))
              .sort_values("year"))

def top_modelos(df, n=10):
    return (df.groupby("model", as_index=False)
              .agg(precio=("price", "mean"), unidades=("price", "count"))
              .sort_values("precio", ascending=False)
              .head(n))


# ============================================================
# CARGA DEL DATASET
# ============================================================
@st.cache_data
def cargar_datos():
    posibles = [Path("data/dataset_bmw.csv"), Path("docs/dataset_bmw.csv")]
    for ruta in posibles:
        if ruta.exists():
            return pd.read_csv(ruta)
    st.error("No se encontro el archivo dataset_bmw.csv")
    st.stop()


# ============================================================
# MACHINE LEARNING - PIPELINE Y LAZYPREDICT
# ============================================================
def construir_preprocesador():
    """Pipeline de preprocesamiento: OneHot + StandardScaler.
    Usa sparse_output=False para compatibilidad con LazyPredict."""
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    return ColumnTransformer([
        ("cat", ohe, ["model", "transmission", "fuelType"]),
        ("num", StandardScaler(),
         ["year", "mileage", "engineSize", "mpg", "tax"]),
    ])


@st.cache_data(show_spinner=False)
def comparar_modelos_lazypredict(_df, n_sample=3000):
    """Compara varios algoritmos con LazyPredict sobre un sample."""
    from lazypredict.Supervised import LazyRegressor

    if len(_df) > n_sample:
        df_s = _df.sample(n_sample, random_state=42)
    else:
        df_s = _df

    X = df_s[COLUMNAS_X]
    y = df_s["price"].to_numpy()
    pre = construir_preprocesador()
    X_pre = pre.fit_transform(X)

    if hasattr(X_pre, "toarray"):
        X_pre = X_pre.toarray()
    X_pre = np.asarray(X_pre, dtype=np.float64)

    X_train, X_test, y_train, y_test = train_test_split(
        X_pre, y, test_size=0.2, random_state=42
    )
    reg = LazyRegressor(verbose=0, ignore_warnings=True, predictions=False)
    modelos, _ = reg.fit(X_train, X_test, y_train, y_test)

    out = modelos.reset_index()
    if "index" in out.columns:
        out = out.rename(columns={"index": "Modelo"})
    elif "Model" in out.columns:
        out = out.rename(columns={"Model": "Modelo"})
    return out


def _construir_mapeo_modelos():
    """Diccionario {nombre_lazypredict: clase_sklearn}."""
    from sklearn.ensemble import (
        BaggingRegressor, HistGradientBoostingRegressor, AdaBoostRegressor,
    )
    from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
    from sklearn.linear_model import (
        Lasso, ElasticNet, BayesianRidge, HuberRegressor,
        PoissonRegressor, OrthogonalMatchingPursuit,
    )
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor

    mapeo = {
        "RandomForestRegressor": RandomForestRegressor,
        "ExtraTreesRegressor": ExtraTreesRegressor,
        "GradientBoostingRegressor": GradientBoostingRegressor,
        "BaggingRegressor": BaggingRegressor,
        "HistGradientBoostingRegressor": HistGradientBoostingRegressor,
        "AdaBoostRegressor": AdaBoostRegressor,
        "DecisionTreeRegressor": DecisionTreeRegressor,
        "ExtraTreeRegressor": ExtraTreeRegressor,
        "LinearRegression": LinearRegression,
        "Ridge": Ridge, "Lasso": Lasso, "ElasticNet": ElasticNet,
        "BayesianRidge": BayesianRidge, "HuberRegressor": HuberRegressor,
        "PoissonRegressor": PoissonRegressor,
        "OrthogonalMatchingPursuit": OrthogonalMatchingPursuit,
        "SVR": SVR, "KNeighborsRegressor": KNeighborsRegressor,
    }
    try:
        from xgboost import XGBRegressor
        mapeo["XGBRegressor"] = XGBRegressor
    except ImportError:
        pass
    try:
        from lightgbm import LGBMRegressor
        mapeo["LGBMRegressor"] = LGBMRegressor
    except ImportError:
        pass
    return mapeo


MAPEO_MODELOS = _construir_mapeo_modelos()


def entrenar_y_guardar_modelo(df, nombre_modelo="RandomForestRegressor"):
    """Entrena el modelo elegido sobre todo el dataset y lo guarda."""
    clase = MAPEO_MODELOS.get(nombre_modelo, RandomForestRegressor)
    X = df[COLUMNAS_X]
    y = df["price"]

    if nombre_modelo in SIN_RANDOM_STATE:
        estimador = clase()
    else:
        try:
            estimador = clase(random_state=42)
        except TypeError:
            estimador = clase()

    pipeline = SkPipeline([
        ("pre", construir_preprocesador()),
        ("regressor", estimador),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metricas = {
        "r2": r2_score(y_test, y_pred),
        "mae": mean_absolute_error(y_test, y_pred),
        "rmse": mean_squared_error(y_test, y_pred) ** 0.5,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "modelo": nombre_modelo,
    }
    joblib.dump(pipeline, RUTA_MODELO)
    return pipeline, metricas


def obtener_mejor_modelo(ranking_df):
    """Devuelve (nombre, estado) del mejor modelo entrenable del ranking."""
    if ranking_df is None or len(ranking_df) == 0:
        return "RandomForestRegressor", "fallback"
    columna = "Modelo" if "Modelo" in ranking_df.columns else ranking_df.columns[0]
    for _, fila in ranking_df.iterrows():
        nombre = str(fila[columna])
        if nombre in MAPEO_MODELOS:
            return nombre, "ok"
    return "RandomForestRegressor", "no_soportado"


# ============================================================
# HELPERS DE UI
# ============================================================
def kpi_card(label, value):
    st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def hero(titulo, subtitulo, badges=None):
    badges_html = ""
    if badges:
        badges_html = "<div>" + "".join(
            f'<span class="badge">{b}</span>' for b in badges) + "</div>"
    st.markdown(f"""
        <div class="hero">
            {badges_html}
            <div class="hero-title">{titulo}</div>
            <div class="hero-subtitle">{subtitulo}</div>
        </div>
    """, unsafe_allow_html=True)
