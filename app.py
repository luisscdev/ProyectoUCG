"""
Proyecto Final - Prediccion de Precio de Vehiculos BMW Usados
Autor: Luis Alexander Suarez Colimba
Maestria en Inteligencia Artificial y Ciencia de Datos - Universidad Casa Grande
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from pathlib import Path
import base64

# Machine Learning
import joblib
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Ruta donde se guarda el modelo entrenado
RUTA_MODELO = Path("modelo_bmw.joblib")

# Rutas de los assets (logo e icono)
RUTA_ICONO = Path("assets/ls_autopredict_icono.svg")
RUTA_LOGO = Path("assets/ls_autopredict_logo.png")


def cargar_svg(ruta: Path) -> str:
    """Lee el contenido de un archivo SVG para inyectarlo como HTML."""
    if ruta.exists():
        return ruta.read_text(encoding="utf-8")
    return ""

# ============================================================
# CONFIGURACION DE LA PAGINA
# ============================================================
st.set_page_config(
    page_title="LS AutoPredict | UCG",
    page_icon=str(RUTA_ICONO) if RUTA_ICONO.exists() else "🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ESTILOS CSS PERSONALIZADOS (TEMA OSCURO ELEGANTE)
# ============================================================
st.markdown("""
<style>
/* === Fondo general (tema claro) === */
.stApp { background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%); }
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; color: #0F172A; }

/* === Encabezados === */
h1 {
    font-weight: 700 !important;
    background: linear-gradient(135deg, #1C69D4 0%, #2A7BE8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
h2, h3 { color: #0F172A !important; font-weight: 600 !important; }

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8FAFC 0%, #EFF4FB 100%);
    border-right: 1px solid #E2E8F0;
}

/* === KPI Cards === */
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

/* === Cards azules === */
.card {
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-left: 4px solid #1C69D4;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

/* === Hero === */
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

/* === Badges === */
.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.05em; background: #DBEAFE;
    color: #1C69D4; border: 1px solid #BFDBFE;
    margin-right: 6px; margin-bottom: 12px;
}

/* === Botones === */
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
    background: linear-gradient(135deg, #2A7BE8 0%, #3B8AF5 100%);
}

/* === Bio Avatar === */
.bio-avatar {
    width: 140px; height: 140px; border-radius: 50%;
    background: linear-gradient(135deg, #1C69D4, #5BA4F5);
    display: flex; align-items: center; justify-content: center;
    font-size: 4rem; font-weight: 700; color: white;
    margin: 0 auto; border: 4px solid #FFFFFF;
    box-shadow: 0 8px 24px rgba(28, 105, 212, 0.25);
}

/* === SVGs responsive === */
.sidebar svg, [data-testid="stSidebar"] svg {
    max-width: 100%;
    height: auto;
}

/* === Divisor === */
hr {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, #DBEAFE, transparent);
    margin: 28px 0;
}

/* === DataFrames === */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}

/* === Tabs === */
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

/* === Inputs === */
.stSelectbox > div > div,
.stNumberInput > div > div,
.stTextInput > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
}

/* === Esconder branding Streamlit === */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ====================================================
   SIDEBAR: comportamiento NATIVO de Streamlit.
   Solo coloreamos el icono del boton expandir/contraer
   para que sea visible sobre fondo blanco.
   ==================================================== */

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
button[kind="header"] svg,
[data-testid="baseButton-headerNoPadding"] svg {
    color: #1C69D4 !important;
    fill: #1C69D4 !important;
    width: 22px !important;
    height: 22px !important;
}
</style>
""", unsafe_allow_html=True)

# Tema para graficos plotly (tema claro)
PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#0F172A", family="Inter, sans-serif"),
    colorway=["#1C69D4", "#5BA4F5", "#3B82F6", "#60A5FA", "#1E40AF", "#93C5FD"],
    xaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
    yaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
    hoverlabel=dict(bgcolor="#FFFFFF", font_color="#0F172A", bordercolor="#1C69D4"),
)
def _tpl(fig):
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
            "model": self.modelo, "year": self.anio, "mileage": self.kilometraje,
            "transmission": self.transmision, "fuelType": self.combustible,
            "engineSize": self.tamano_motor, "mpg": self.mpg, "tax": self.impuesto,
        }])

    def __str__(self):
        return f"BMW {self.modelo} {self.anio} · {self.kilometraje:,} mi · {self.combustible}"


class PredictorPrecio:
    """Estima el precio de un vehiculo (POO).

    Carga automaticamente el modelo entrenado con LazyPredict si existe.
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
        """Devuelve el nombre del algoritmo usado (ej. 'RandomForestRegressor')."""
        if self.modelo_ml is None:
            return "Heuristica de respaldo"
        try:
            return self.modelo_ml.named_steps["regressor"].__class__.__name__
        except Exception:
            return self.modelo_ml.__class__.__name__

    def predecir(self, vehiculo):
        if self.modelo_ml is None:
            # Heuristica de respaldo si todavia no hay modelo entrenado
            base = 30000
            base -= (2024 - vehiculo.anio) * 1500
            base -= (vehiculo.kilometraje / 1000) * 35
            base += (vehiculo.tamano_motor - 2.0) * 2500
            if vehiculo.es_premium():
                base += 5000
            return max(base, 1500)
        return float(self.modelo_ml.predict(vehiculo.to_df())[0])


# ============================================================
# ENTRENAMIENTO CON LAZYPREDICT
# ============================================================
COLUMNAS_X = ["model", "year", "mileage", "transmission", "fuelType", "engineSize", "mpg", "tax"]


def construir_preprocesador():
    """Pipeline de preprocesamiento: OneHot para categoricas, StandardScaler para numericas.

    Usa sparse_output=False para que LazyPredict y los modelos lineales
    no tengan problemas con matrices sparse.
    """
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        # Fallback para versiones antiguas de sklearn (<1.2) donde se llamaba 'sparse'
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    return ColumnTransformer([
        ("cat", ohe, ["model", "transmission", "fuelType"]),
        ("num", StandardScaler(), ["year", "mileage", "engineSize", "mpg", "tax"]),
    ])


@st.cache_data(show_spinner=False)
def comparar_modelos_lazypredict(_df, n_sample=3000):
    """Compara varios algoritmos con LazyPredict (sobre un sample para velocidad).

    Devuelve un DataFrame con el ranking de modelos.
    """
    from lazypredict.Supervised import LazyRegressor

    # Sampling para que sea rapido
    if len(_df) > n_sample:
        df_s = _df.sample(n_sample, random_state=42)
    else:
        df_s = _df

    X = df_s[COLUMNAS_X]
    y = df_s["price"].to_numpy()
    pre = construir_preprocesador()
    X_pre = pre.fit_transform(X)

    # LazyPredict no soporta matrices sparse -> convertir a denso
    if hasattr(X_pre, "toarray"):
        X_pre = X_pre.toarray()
    X_pre = np.asarray(X_pre, dtype=np.float64)

    X_train, X_test, y_train, y_test = train_test_split(
        X_pre, y, test_size=0.2, random_state=42
    )
    reg = LazyRegressor(verbose=0, ignore_warnings=True, predictions=False)
    modelos, _ = reg.fit(X_train, X_test, y_train, y_test)
    # LazyPredict devuelve el modelo como indice. Lo paso a columna y le pongo nombre consistente.
    out = modelos.reset_index()
    # El nombre puede venir como 'index' o como 'Model' segun la version
    if "index" in out.columns:
        out = out.rename(columns={"index": "Modelo"})
    elif "Model" in out.columns:
        out = out.rename(columns={"Model": "Modelo"})
    return out


# Mapeo de nombres de LazyPredict a clases reales de sklearn (y XGBoost / LightGBM)
def _construir_mapeo_modelos():
    """Devuelve un diccionario {nombre_lazypredict: clase_sklearn}."""
    from sklearn.ensemble import (
        BaggingRegressor, HistGradientBoostingRegressor,
        AdaBoostRegressor,
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
        "Ridge": Ridge,
        "Lasso": Lasso,
        "ElasticNet": ElasticNet,
        "BayesianRidge": BayesianRidge,
        "HuberRegressor": HuberRegressor,
        "PoissonRegressor": PoissonRegressor,
        "OrthogonalMatchingPursuit": OrthogonalMatchingPursuit,
        "SVR": SVR,
        "KNeighborsRegressor": KNeighborsRegressor,
    }
    # Opcionales segun la libreria este instalada
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

# Modelos que NO aceptan el argumento random_state
SIN_RANDOM_STATE = {
    "LinearRegression", "BayesianRidge", "OrthogonalMatchingPursuit",
    "HuberRegressor", "SVR", "KNeighborsRegressor",
}


def entrenar_y_guardar_modelo(df, nombre_modelo="RandomForestRegressor"):
    """Entrena el modelo elegido sobre todo el dataset y lo guarda en disco.

    Devuelve el pipeline entrenado y un diccionario con metricas.
    """
    clase = MAPEO_MODELOS.get(nombre_modelo, RandomForestRegressor)
    X = df[COLUMNAS_X]
    y = df["price"]

    # Instanciar el modelo con random_state si lo acepta
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
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
    """Devuelve el nombre del mejor modelo del ranking de LazyPredict
    que pueda ser entrenado (esta en MAPEO_MODELOS).

    Si el mejor no esta soportado, busca el siguiente.
    """
    if ranking_df is None or len(ranking_df) == 0:
        return "RandomForestRegressor", "fallback"
    columna = "Modelo" if "Modelo" in ranking_df.columns else ranking_df.columns[0]
    for _, fila in ranking_df.iterrows():
        nombre = str(fila[columna])
        if nombre in MAPEO_MODELOS:
            return nombre, "ok"
    return "RandomForestRegressor", "no_soportado"


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
    return df[(df["price"] >= minimo) & (df["price"] <= maximo)].reset_index(drop=True)

def agregar_antiguedad(df, anio_ref=2024):
    return df.assign(antiguedad=lambda d: anio_ref - d["year"])

def pipeline_limpieza(df):
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
# COMPONENTES REUTILIZABLES
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
        badges_html = "<div>" + "".join(f'<span class="badge">{b}</span>' for b in badges) + "</div>"
    st.markdown(f"""
        <div class="hero">
            {badges_html}
            <div class="hero-title">{titulo}</div>
            <div class="hero-subtitle">{subtitulo}</div>
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGINA: INICIO
# ============================================================
def pagina_inicio():
    df_crudo = cargar_datos()
    df = pipeline_limpieza(df_crudo)
    k = kpis(df)

    hero("Dashboard BMW",
         "Resumen del catalogo de vehiculos BMW usados. Usa el menu lateral para navegar.",
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
        fig = px.area(serie, x="year", y="precio", color_discrete_sequence=["#1C69D4"])
        fig.update_layout(xaxis_title="", yaxis_title="£", height=320)
        st.plotly_chart(_tpl(fig), use_container_width=True)

    with col2:
        st.markdown("### Distribucion por Combustible")
        dist = df["fuelType"].value_counts().reset_index()
        dist.columns = ["fuelType", "count"]
        fig = px.pie(dist, values="count", names="fuelType", hole=0.55,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=320)
        st.plotly_chart(_tpl(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Vista Previa del Dataset")
    st.dataframe(df.head(15), use_container_width=True, hide_index=True)


# ============================================================
# PAGINA: LIMPIEZA DE DATOS
# ============================================================
def pagina_limpieza():
    df_crudo = cargar_datos()

    hero("Limpieza de Datos",
         "Aqui se muestra el proceso de limpieza y transformacion aplicado al dataset.",
         badges=["Limpieza", "Pipeline funcional"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Filas originales", f"{len(df_crudo):,}")
    with c2: kpi_card("Nulos totales", f"{int(df_crudo.isnull().sum().sum())}")
    with c3: kpi_card("Duplicados", f"{int(df_crudo.duplicated().sum())}")
    with c4: kpi_card("Columnas", f"{df_crudo.shape[1]}")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Pasos del Pipeline de Limpieza")

    pasos = [
        ("1. Eliminar espacios en blanco", "Limpiamos espacios al inicio/fin de la columna 'model'."),
        ("2. Quitar duplicados", "Eliminamos registros identicos para evitar sesgos."),
        ("3. Filtrar precios validos", "Conservamos vehiculos con precio entre £500 y £200.000."),
        ("4. Crear variable derivada", "Calculamos la antiguedad del vehiculo (2024 - anio)."),
    ]
    for titulo, desc in pasos:
        st.markdown(f"""
            <div class="card">
                <div style="font-weight: 700; color: #5BA4F5; font-size: 1.05rem;">{titulo}</div>
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
        "Etapa": ["1. Crudo", "2. Sin espacios", "3. Sin duplicados", "4. Precio valido", "5. + antiguedad"],
        "Filas": [len(df_crudo), len(df1), len(df2), len(df3), len(df4)],
    })
    fig = px.bar(etapas, x="Etapa", y="Filas", text="Filas", color="Filas",
                 color_continuous_scale=["#1C69D4", "#BB8FCE"])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(height=380, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(_tpl(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Valores Nulos por Columna")
    nulos = df_crudo.isnull().sum().reset_index()
    nulos.columns = ["Columna", "Nulos"]
    fig = px.bar(nulos, x="Columna", y="Nulos", color="Nulos",
                 color_continuous_scale=["#2ECC71", "#E74C3C"])
    fig.update_layout(height=340, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(_tpl(fig), use_container_width=True)

    if df_crudo.isnull().sum().sum() == 0:
        st.success("El dataset no tiene valores nulos. Excelente!")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Dataset Despues de la Limpieza")
    st.dataframe(df4.head(20), use_container_width=True, hide_index=True)


# ============================================================
# PAGINA: ANALISIS EXPLORATORIO
# ============================================================
def pagina_analisis():
    df = pipeline_limpieza(cargar_datos())

    hero("Analisis Exploratorio",
         "Inspecciona los datos, revisa estadisticas y filtra registros segun tus criterios.",
         badges=["EDA", "Filtros", "Estadisticas"])

    st.markdown("### Estadisticas Descriptivas")
    st.dataframe(df.describe().round(2).T, use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Matriz de Correlacion")
    corr = df.select_dtypes(include=np.number).corr().round(2)
    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale="RdBu_r", zmin=-1, zmax=1,
        text=corr.values, texttemplate="%{text}",
        textfont={"size": 11, "color": "white"},
    ))
    fig.update_layout(height=460)
    st.plotly_chart(_tpl(fig), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Busqueda Filtrada")
    col1, col2, col3 = st.columns(3)
    with col1:
        modelo = st.selectbox("Modelo", ["Todos"] + sorted(df["model"].unique().tolist()))
    with col2:
        combustible = st.selectbox("Combustible", ["Todos"] + sorted(df["fuelType"].unique().tolist()))
    with col3:
        precio_max = st.number_input("Precio maximo (£)", 1000, 200000, 50000, step=1000)

    rango = st.slider("Rango de anios",
                      int(df["year"].min()), int(df["year"].max()),
                      (int(df["year"].min()), int(df["year"].max())))

    resultado = df.copy()
    if modelo != "Todos":
        resultado = resultado[resultado["model"] == modelo]
    if combustible != "Todos":
        resultado = resultado[resultado["fuelType"] == combustible]
    resultado = resultado[(resultado["year"] >= rango[0]) &
                          (resultado["year"] <= rango[1]) &
                          (resultado["price"] <= precio_max)]

    st.success(f"Se encontraron {len(resultado):,} registros")
    st.dataframe(resultado, use_container_width=True, hide_index=True)

    csv = resultado.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", data=csv,
                       file_name="bmw_filtrado.csv", mime="text/csv")


# ============================================================
# PAGINA: VISUALIZACIONES
# ============================================================
def pagina_visualizaciones():
    df = pipeline_limpieza(cargar_datos())

    hero("Visualizaciones Interactivas",
         "Graficos dinamicos organizados por categoria. Usa las pestañas para navegar.",
         badges=["Plotly", "Interactivo", "8 graficos"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribuciones",
        "🔄 Relaciones",
        "🏆 Rankings",
        "📈 Tendencias",
    ])

    # ============================================================
    # TAB 1: DISTRIBUCIONES
    # ============================================================
    with tab1:
        st.markdown("### Distribucion del Precio")
        st.markdown("<p style='color:#475569;'>Como se reparten los precios en el dataset.</p>",
                    unsafe_allow_html=True)
        fig = px.histogram(df, x="price", nbins=60, opacity=0.85,
                           color_discrete_sequence=["#1C69D4"])
        fig.update_layout(xaxis_title="Precio (£)", yaxis_title="Frecuencia",
                          bargap=0.02, height=380)
        st.plotly_chart(_tpl(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Precio por Transmision")
            fig = px.box(df, x="transmission", y="price", color="transmission",
                         color_discrete_sequence=["#1C69D4", "#5BA4F5", "#BB8FCE"])
            fig.update_layout(xaxis_title="", yaxis_title="Precio (£)",
                              showlegend=False, height=400)
            st.plotly_chart(_tpl(fig), use_container_width=True)

        with col2:
            st.markdown("### Precio por Combustible")
            fig = px.violin(df, x="fuelType", y="price", color="fuelType",
                            box=True, points=False,
                            color_discrete_sequence=["#1C69D4", "#5BA4F5", "#BB8FCE",
                                                     "#2ECC71", "#F1C40F"])
            fig.update_layout(xaxis_title="", yaxis_title="Precio (£)",
                              showlegend=False, height=400)
            st.plotly_chart(_tpl(fig), use_container_width=True)

    # ============================================================
    # TAB 2: RELACIONES
    # ============================================================
    with tab2:
        st.markdown("### Precio vs Kilometraje")
        st.markdown("<p style='color:#475569;'>A mayor kilometraje, ¿menor precio? "
                    "Cada punto es un vehiculo, el color indica el año.</p>",
                    unsafe_allow_html=True)
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(sample, x="mileage", y="price", color="year",
                         opacity=0.6, color_continuous_scale="Viridis",
                         hover_data=["model", "fuelType"])
        fig.update_layout(xaxis_title="Kilometraje", yaxis_title="Precio (£)", height=460)
        st.plotly_chart(_tpl(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        st.markdown("### Tamaño del Motor vs Precio Promedio")
        st.markdown("<p style='color:#475569;'>El tamaño de cada burbuja representa "
                    "la cantidad de vehiculos con ese tamaño de motor.</p>",
                    unsafe_allow_html=True)
        motor = (df.groupby("engineSize", as_index=False)
                   .agg(precio=("price", "mean"), unidades=("price", "count")))
        fig = px.scatter(motor, x="engineSize", y="precio", size="unidades",
                         color="precio", color_continuous_scale="Plasma",
                         hover_data={"unidades": True})
        fig.update_layout(xaxis_title="Tamaño del motor (L)",
                          yaxis_title="Precio promedio (£)", height=460)
        st.plotly_chart(_tpl(fig), use_container_width=True)

    # ============================================================
    # TAB 3: RANKINGS
    # ============================================================
    with tab3:
        st.markdown("### Top 10 Modelos BMW por Precio Promedio")
        st.markdown("<p style='color:#475569;'>Los modelos mas caros en promedio dentro del dataset.</p>",
                    unsafe_allow_html=True)
        top = top_modelos(df, n=10)
        fig = px.bar(top, x="precio", y="model", orientation="h", color="precio",
                     color_continuous_scale=["#1C69D4", "#BB8FCE"], text="precio")
        fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          xaxis_title="Precio promedio (£)", yaxis_title="",
                          height=480, coloraxis_showscale=False)
        st.plotly_chart(_tpl(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Distribucion por Combustible")
            dist = df["fuelType"].value_counts().reset_index()
            dist.columns = ["fuelType", "count"]
            fig = px.pie(dist, values="count", names="fuelType", hole=0.55,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_layout(height=420)
            st.plotly_chart(_tpl(fig), use_container_width=True)

        with col_b:
            st.markdown("### Distribucion por Transmision")
            dist_t = df["transmission"].value_counts().reset_index()
            dist_t.columns = ["transmission", "count"]
            fig = px.bar(dist_t, x="transmission", y="count", color="count",
                         color_continuous_scale=["#1C69D4", "#BB8FCE"], text="count")
            fig.update_traces(texttemplate="%{text:,}", textposition="outside")
            fig.update_layout(xaxis_title="", yaxis_title="Cantidad",
                              showlegend=False, height=420, coloraxis_showscale=False)
            st.plotly_chart(_tpl(fig), use_container_width=True)

    # ============================================================
    # TAB 4: TENDENCIAS
    # ============================================================
    with tab4:
        st.markdown("### Evolucion del Precio Promedio por Año")
        st.markdown("<p style='color:#475569;'>Como ha cambiado el precio promedio "
                    "a traves de los años de fabricacion.</p>",
                    unsafe_allow_html=True)
        serie = precio_por_anio(df)
        fig = px.line(serie, x="year", y="precio", markers=True,
                      color_discrete_sequence=["#5BA4F5"])
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        fig.update_layout(xaxis_title="Año", yaxis_title="Precio promedio (£)", height=440)
        st.plotly_chart(_tpl(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        st.markdown("### Cantidad de Vehiculos por Año")
        st.markdown("<p style='color:#475569;'>Cuantos vehiculos hay en el dataset por cada año.</p>",
                    unsafe_allow_html=True)
        fig = px.bar(serie, x="year", y="unidades",
                     color="unidades", color_continuous_scale=["#1C69D4", "#BB8FCE"])
        fig.update_layout(xaxis_title="Año", yaxis_title="Cantidad",
                          showlegend=False, height=440, coloraxis_showscale=False)
        st.plotly_chart(_tpl(fig), use_container_width=True)


# ============================================================
# PAGINA: PREDICCION
# ============================================================
def pagina_prediccion():
    df = pipeline_limpieza(cargar_datos())
    predictor = PredictorPrecio()
    modelo_listo = predictor.esta_entrenado()

    hero("Prediccion de Precio",
         "Compara modelos con LazyPredict, entrena el mejor y predice el precio de un BMW usado.",
         badges=["Machine Learning", "LazyPredict",
                 "Modelo entrenado" if modelo_listo else "Sin modelo"])

    tab1, tab2 = st.tabs(["⚙️ Comparar y Entrenar Modelos", "🎯 Predecir Precio"])

    # ============================================================
    # TAB 1: COMPARAR Y ENTRENAR
    # ============================================================
    with tab1:
        st.markdown("### Paso 1 — Comparar Algoritmos con LazyPredict")
        st.markdown(
            "LazyPredict entrena automaticamente varios algoritmos de regresion sobre un "
            "sample del dataset y devuelve un ranking ordenado por R² ajustado."
        )

        if st.button("🚀 Ejecutar LazyPredict", use_container_width=True, key="run_lazy"):
            with st.spinner("Comparando modelos... esto puede tardar 1-2 minutos."):
                ranking = comparar_modelos_lazypredict(df)
                st.session_state["ranking_lazy"] = ranking

        if "ranking_lazy" in st.session_state:
            ranking = st.session_state["ranking_lazy"]
            st.success(f"✅ Se evaluaron {len(ranking)} modelos.")
            st.dataframe(ranking.head(10), use_container_width=True, hide_index=True)

            top5 = ranking.head(5).copy()
            modelos = ranking['Modelo'].head(3)
            print('modelos => '+modelos)
            fig = px.bar(
                top5,
                x="Adjusted R-Squared" if "Adjusted R-Squared" in top5.columns else top5.columns[1],
                y="Modelo",
                orientation="h",
                color="Adjusted R-Squared" if "Adjusted R-Squared" in top5.columns else top5.columns[1],
                color_continuous_scale=["#1C69D4", "#BB8FCE"],
            )
            fig.update_layout(
                yaxis={"categoryorder": "total ascending"},
                title="Top 5 modelos por R² ajustado",
                height=360,
                coloraxis_showscale=False,
            )
            st.plotly_chart(_tpl(fig), use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("### Paso 2 — Entrenar Automaticamente el Mejor Modelo")
        st.markdown(
            "Se entrenara sobre todo el dataset el modelo que mejor R² ajustado obtuvo "
            "en LazyPredict. El resultado queda guardado y se usa para predecir precios."
        )

        # Mostrar cual seria el modelo elegido (si ya corrio LazyPredict)
        ranking_disponible = "ranking_lazy" in st.session_state
        if ranking_disponible:
            mejor, estado = obtener_mejor_modelo(st.session_state["ranking_lazy"])
            if estado == "ok":
                st.info(f"🏆 Modelo recomendado por LazyPredict: **{mejor}**")
            else:
                st.warning(
                    f"⚠️ El mejor modelo de LazyPredict no es entrenable directamente. "
                    f"Se usara **{mejor}** como respaldo."
                )
        else:
            mejor = "RandomForestRegressor"
            st.info(
                "💡 Ejecuta primero LazyPredict (Paso 1) para que el sistema elija "
                "automaticamente el mejor modelo. Si lo entrenas sin ejecutar antes, "
                f"se usara **{mejor}** por defecto."
            )

        if st.button(
            f"🎓 Entrenar y guardar el mejor modelo ({mejor})",
            use_container_width=True,
            key="train_btn",
            type="primary",
        ):
            with st.spinner(f"Entrenando {mejor}... esto puede tardar 1-2 minutos."):
                _, met = entrenar_y_guardar_modelo(df, mejor)
                st.session_state["metricas_modelo"] = met
            st.success(f"✅ Modelo {mejor} entrenado y guardado en `modelo_bmw.joblib`.")
            st.balloons()
            st.rerun()

        # Mostrar metricas si hay modelo
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
                st.info("Modelo cargado desde disco. Para ver metricas, vuelve a entrenarlo.")

    # ============================================================
    # TAB 2: PREDECIR
    # ============================================================
    # ============================================================
    # TAB 2: PREDECIR
    # ============================================================
    with tab2:
        if not modelo_listo:
            st.warning(
                "⚠️ Aun no hay un modelo entrenado. Ve a la pestaña anterior, "
                "ejecuta LazyPredict y entrena el modelo. Mientras tanto se usara una "
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
            kilometraje = st.number_input("Kilometraje", 0, 300000, 25000, step=1000)

        with col2:
            transmision = st.selectbox("Transmision", transmisiones)
            combustible = st.selectbox(
                "Combustible", combustibles,
                index=combustibles.index("Diesel") if "Diesel" in combustibles else 0,
            )
            tamano_motor = st.slider("Tamano motor (L)", 0.5, 6.6, 2.0, step=0.1)

        with col3:
            mpg = st.slider("Consumo (mpg)", 10.0, 200.0, 55.0, step=0.5)
            impuesto = st.number_input("Impuesto (£)", 0, 600, 145, step=5)

        st.markdown("<hr/>", unsafe_allow_html=True)

        if st.button("Calcular precio estimado", use_container_width=True, key="predict_btn"):
            v = Vehiculo(modelo, anio, int(kilometraje), transmision, combustible,
                         float(tamano_motor), float(mpg), int(impuesto))
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
            with c1: kpi_card("Algoritmo", nombre_algoritmo.replace("Regressor", ""))
            with c2: kpi_card("Antiguedad", f"{v.antiguedad()} anios")
            with c3: kpi_card("Premium", "Si" if v.es_premium() else "No")
            with c4: kpi_card("Fuente", "Modelo ML" if modelo_listo else "Heuristica")


# ============================================================
# PAGINA: BIOGRAFIA
# ============================================================
def pagina_biografia():
    hero("Sobre el Autor",
         "Informacion personal del desarrollador del proyecto.",
         badges=["Biografia"])

    col_avatar, col_info = st.columns([1, 2])

    with col_avatar:
        st.markdown("""
            <div style="text-align: center;">
                <div class="bio-avatar">LS</div>
                <div style="margin-top: 16px; font-size: 1.3rem; font-weight: 700; color: #0F172A;">
                    Luis Alexander Suarez Colimba
                </div>
                <div style="color: #5BA4F5; margin-top: 4px;">
                    Estudiante de Maestria
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("### Quien Soy")
        st.markdown("""
            Estudiante de la **Maestria en Inteligencia Artificial y Ciencia de Datos**
            en la **Universidad Casa Grande**. Me interesa combinar el desarrollo de
            software con el analisis de datos, especialmente en proyectos donde se
            puede pasar de un dataset crudo a una aplicacion que otra persona pueda usar.
        """)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Contacto")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">CORREO</div>
                <div style="font-weight: 600; margin-top: 6px;">luissuarez2t@gmail.com</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">UNIVERSIDAD</div>
                <div style="font-weight: 600; margin-top: 6px;">Universidad Casa Grande</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">UBICACION</div>
                <div style="font-weight: 600; margin-top: 6px;">Ecuador</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Formacion Academica")
    formaciones = [
        ("Maestria en IA y Ciencia de Datos", "Universidad Casa Grande", "2025 - En curso"),
        ("[Tu pregrado - edita aqui]", "[Universidad]", "[Anio - Anio]"),
    ]
    for titulo, inst, periodo in formaciones:
        st.markdown(f"""
            <div class="card">
                <div style="font-weight: 700; color: #0F172A; font-size: 1.1rem;">{titulo}</div>
                <div style="color: #1C69D4; margin-top: 4px;">{inst} · {periodo}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Habilidades Tecnicas")
    habs = {
        "Lenguajes": ["Python", "SQL", "JavaScript", "TypeScript"],
        "Ciencia de Datos": ["Pandas", "NumPy", "Scikit-learn", "Plotly"],
        "Frameworks": ["Streamlit", "Angular", "FastAPI"],
        "Bases de Datos": ["PostgreSQL", "MongoDB"],
        "Herramientas": ["Git", "Docker", "GitHub"],
    }
    for cat, items in habs.items():
        badges = "".join([f'<span class="badge">{i}</span>' for i in items])
        st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="color: #64748B; font-size: 0.9rem; margin-bottom: 6px;">{cat}</div>
                <div>{badges}</div>
            </div>
        """, unsafe_allow_html=True)


# ============================================================
# MENU LATERAL Y RUTEO
# ============================================================
with st.sidebar:
    if RUTA_LOGO.exists():
        st.image(str(RUTA_LOGO), use_container_width=True)
        st.markdown("""
            <div style="color: #64748B; font-size: 0.78rem; text-align: center;
                        margin-top: 6px; letter-spacing: 0.08em; text-transform: uppercase;">
                UCG · Proyecto Final
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <div style="font-size: 2rem;">🚗</div>
                <div style="font-weight: 700; font-size: 1.2rem; color: #0F172A;">
                    LS AutoPredict
                </div>
                <div style="color: #64748B; font-size: 0.85rem;">UCG · Proyecto Final</div>
            </div>
        """, unsafe_allow_html=True)

    seleccion = option_menu(
        menu_title=None,
        options=["Inicio", "Limpieza", "Analisis", "Visualizaciones", "Prediccion", "Biografia"],
        icons=["house-fill", "magic", "search", "bar-chart-fill", "calculator-fill", "person-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#1C69D4", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px", "text-align": "left", "margin": "4px 0",
                "padding": "12px 16px", "border-radius": "10px",
                "color": "#475569",
                "--hover-color": "#DBEAFE",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #1C69D4, #2A7BE8)",
                "color": "white", "font-weight": "600",
            },
        },
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
        <div style="color: #64748B; font-size: 0.78rem; text-align: center;">
            Luis Suarez · 2026<br>
            Maestria IA y Ciencia de Datos
        </div>
    """, unsafe_allow_html=True)


paginas = {
    "Inicio": pagina_inicio,
    "Limpieza": pagina_limpieza,
    "Analisis": pagina_analisis,
    "Visualizaciones": pagina_visualizaciones,
    "Prediccion": pagina_prediccion,
    "Biografia": pagina_biografia,
}
paginas[seleccion]()
