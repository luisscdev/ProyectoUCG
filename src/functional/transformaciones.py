"""
Módulo de Transformaciones — Paradigma Funcional.

Cada función recibe un DataFrame y devuelve uno nuevo, sin mutar el original.
Las funciones se diseñan para ser puras (sin efectos secundarios) y
componibles mediante `.pipe()` o `functools.reduce`.

Recursos del paradigma utilizados:
    * Funciones puras
    * Funciones de orden superior (map, filter, reduce)
    * Lambdas
    * Composición de funciones
"""

from __future__ import annotations
from functools import reduce
from typing import Callable, Iterable, List

import numpy as np
import pandas as pd


# ============================================================
# FUNCIONES PURAS DE TRANSFORMACIÓN
# ============================================================
def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve un DataFrame sin filas duplicadas."""
    return df.drop_duplicates().reset_index(drop=True)


def eliminar_atipicos_iqr(df: pd.DataFrame, columna: str, factor: float = 1.5) -> pd.DataFrame:
    """Elimina filas con valores atípicos en una columna usando el rango intercuartílico."""
    q1, q3 = df[columna].quantile([0.25, 0.75])
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - factor * iqr, q3 + factor * iqr
    return df[(df[columna] >= lim_inf) & (df[columna] <= lim_sup)].reset_index(drop=True)


def limpiar_espacios_modelo(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina espacios al inicio/fin de la columna 'model' (problema típico del dataset)."""
    out = df.copy()
    out["model"] = out["model"].astype(str).str.strip()
    return out


def agregar_antiguedad(df: pd.DataFrame, anio_ref: int = 2024) -> pd.DataFrame:
    """Crea la variable derivada 'antiguedad' a partir de 'year'."""
    return df.assign(antiguedad=lambda d: anio_ref - d["year"])


def agregar_km_por_anio(df: pd.DataFrame, anio_ref: int = 2024) -> pd.DataFrame:
    """Crea la variable derivada 'km_por_anio' (uso del vehículo)."""
    return df.assign(
        km_por_anio=lambda d: d["mileage"] / np.maximum(anio_ref - d["year"], 1)
    )


def filtrar_precio_valido(df: pd.DataFrame, minimo: int = 500, maximo: int = 200_000) -> pd.DataFrame:
    """Devuelve solo registros con precio dentro de un rango plausible."""
    return df[(df["price"] >= minimo) & (df["price"] <= maximo)].reset_index(drop=True)


# ============================================================
# COMPOSICIÓN DE FUNCIONES
# ============================================================
TransformacionDF = Callable[[pd.DataFrame], pd.DataFrame]


def componer(funciones: Iterable[TransformacionDF]) -> TransformacionDF:
    """Devuelve una nueva función que aplica todas las transformaciones en orden.

    Ejemplo:
        pipeline = componer([limpiar_espacios_modelo, eliminar_duplicados])
        df_limpio = pipeline(df)
    """
    return lambda df: reduce(lambda acc, fn: fn(acc), funciones, df)


def pipeline_default(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline estándar de preprocesamiento aplicado en toda la app."""
    return (
        df
        .pipe(limpiar_espacios_modelo)
        .pipe(eliminar_duplicados)
        .pipe(filtrar_precio_valido)
        .pipe(agregar_antiguedad)
        .pipe(agregar_km_por_anio)
    )


# ============================================================
# UTILITARIOS FUNCIONALES
# ============================================================
def aplicar_a_columnas(df: pd.DataFrame, columnas: List[str], fn: Callable) -> pd.DataFrame:
    """Aplica una función a un conjunto de columnas usando map (orden superior)."""
    out = df.copy()
    for col in columnas:
        out[col] = list(map(fn, out[col]))
    return out


def media_truncada(valores: Iterable[float], proporcion: float = 0.05) -> float:
    """Media recortada — ejemplo de uso de funciones de orden superior."""
    serie = pd.Series(list(valores)).sort_values()
    n = len(serie)
    k = int(n * proporcion)
    recortada = serie.iloc[k: n - k] if k > 0 else serie
    return float(recortada.mean())
