"""
Módulo de Predicción — Paradigma Orientado a Objetos (POO).

Encapsula la lógica de carga del modelo entrenado y la inferencia.
Permite cambiar el algoritmo subyacente sin modificar el código cliente
(principio de inversión de dependencias).
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd

from .vehiculo import Vehiculo


class PredictorPrecio:
    """Encapsula un modelo de regresión entrenado para estimar precios."""

    def __init__(self, ruta_modelo: Optional[Path] = None) -> None:
        self.ruta_modelo = ruta_modelo
        self.modelo = None
        if ruta_modelo and Path(ruta_modelo).exists():
            self.cargar(ruta_modelo)

    # ---------- Persistencia ----------
    def cargar(self, ruta: Path) -> None:
        self.modelo = joblib.load(ruta)
        self.ruta_modelo = Path(ruta)

    def esta_entrenado(self) -> bool:
        return self.modelo is not None

    # ---------- Inferencia ----------
    def predecir(self, vehiculo: Vehiculo) -> float:
        """Devuelve el precio estimado en libras esterlinas (£)."""
        if not self.esta_entrenado():
            # Modo demostración cuando aún no existe modelo entrenado.
            return self._estimacion_heuristica(vehiculo)
        df = vehiculo.to_dataframe()
        pred = self.modelo.predict(df)
        return float(pred[0])

    def predecir_lote(self, df: pd.DataFrame) -> np.ndarray:
        if not self.esta_entrenado():
            raise RuntimeError("El modelo aún no está entrenado.")
        return self.modelo.predict(df)

    # ---------- Heurística de respaldo ----------
    @staticmethod
    def _estimacion_heuristica(v: Vehiculo) -> float:
        """Fórmula simple para mostrar la app antes de entrenar el modelo real.

        No usar en producción — únicamente fines pedagógicos.
        """
        base = 30000.0
        depreciacion = (2024 - v.anio) * 1500
        descuento_km = (v.kilometraje / 1000) * 35
        bonus_motor = (v.tamano_motor - 2.0) * 2500
        ajuste_premium = 5000 if v.es_premium() else 0
        precio = base - depreciacion - descuento_km + bonus_motor + ajuste_premium
        return max(precio, 1500.0)
