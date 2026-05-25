"""
Módulo de Consultas — Paradigma Declarativo.

Cada función expresa QUÉ se desea obtener (no CÓMO), apoyándose en la
API declarativa de Pandas: groupby, agg, query, pivot_table.

Estas expresiones se leen casi como SQL y reemplazan bucles explícitos.
"""

from __future__ import annotations
import pandas as pd


def precio_promedio_por_modelo(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top-N modelos por precio promedio."""
    return (df.groupby("model", as_index=False)
              .agg(precio_promedio=("price", "mean"),
                   unidades=("price", "count"))
              .sort_values("precio_promedio", ascending=False)
              .head(top_n))


def precio_promedio_por_anio(df: pd.DataFrame) -> pd.DataFrame:
    """Evolución del precio promedio por año de fabricación."""
    return (df.groupby("year", as_index=False)
              .agg(precio_promedio=("price", "mean"),
                   unidades=("price", "count"))
              .sort_values("year"))


def distribucion_combustible(df: pd.DataFrame) -> pd.DataFrame:
    """Distribución porcentual por tipo de combustible."""
    return (df["fuelType"]
              .value_counts(normalize=True)
              .mul(100)
              .round(2)
              .reset_index()
              .rename(columns={"index": "fuelType", "fuelType": "porcentaje"}))


def distribucion_transmision(df: pd.DataFrame) -> pd.DataFrame:
    """Distribución por tipo de transmisión."""
    return (df["transmission"]
              .value_counts()
              .reset_index()
              .rename(columns={"index": "transmission", "transmission": "unidades"}))


def resumen_descriptivo(df: pd.DataFrame) -> pd.DataFrame:
    """Estadísticas descriptivas de variables numéricas (formato amigable)."""
    numericas = df.select_dtypes(include="number")
    return numericas.describe().T.round(2)


def correlaciones(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlación de Pearson entre variables numéricas."""
    return df.select_dtypes(include="number").corr().round(3)


def buscar_por_filtros(df: pd.DataFrame,
                       modelo: str | None = None,
                       anio_min: int | None = None,
                       anio_max: int | None = None,
                       combustible: str | None = None,
                       precio_max: int | None = None) -> pd.DataFrame:
    """Búsqueda flexible — los filtros None se ignoran."""
    consulta = df
    if modelo:
        consulta = consulta.query("model == @modelo")
    if anio_min is not None:
        consulta = consulta.query("year >= @anio_min")
    if anio_max is not None:
        consulta = consulta.query("year <= @anio_max")
    if combustible:
        consulta = consulta.query("fuelType == @combustible")
    if precio_max is not None:
        consulta = consulta.query("price <= @precio_max")
    return consulta.reset_index(drop=True)


def kpis_globales(df: pd.DataFrame) -> dict:
    """KPIs principales para la pantalla de inicio."""
    return {
        "total_vehiculos": int(len(df)),
        "modelos_unicos": int(df["model"].nunique()),
        "precio_promedio": float(df["price"].mean()),
        "precio_mediano": float(df["price"].median()),
        "anio_min": int(df["year"].min()),
        "anio_max": int(df["year"].max()),
        "km_promedio": float(df["mileage"].mean()),
    }
