"""
Módulo de Dominio — Paradigma Orientado a Objetos (POO).

Define la entidad Vehiculo, que encapsula los atributos y el comportamiento
asociado a un automóvil BMW usado dentro del dominio del problema.

Ilustra los pilares de la POO:
    * Encapsulamiento: los atributos viven dentro del objeto.
    * Abstracción: el resto del sistema usa Vehiculo sin saber su detalle interno.
    * Validación de invariantes: el constructor valida los rangos.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Literal, Dict, Any
import pandas as pd


TransmisionLiteral = Literal["Automatic", "Manual", "Semi-Auto"]
CombustibleLiteral = Literal["Diesel", "Petrol", "Hybrid", "Electric", "Other"]


@dataclass
class Vehiculo:
    """Representa un vehículo BMW usado con sus características técnicas."""

    modelo: str
    anio: int
    kilometraje: int
    transmision: TransmisionLiteral
    combustible: CombustibleLiteral
    tamano_motor: float
    mpg: float
    impuesto: int = 145  # valor por defecto razonable según el dataset

    def __post_init__(self) -> None:
        """Valida los invariantes del dominio tras la construcción."""
        self._validar()

    # ---------- Validación ----------
    def _validar(self) -> None:
        if not (1990 <= self.anio <= 2030):
            raise ValueError(f"Año fuera de rango razonable: {self.anio}")
        if self.kilometraje < 0:
            raise ValueError("El kilometraje no puede ser negativo.")
        if not (0 < self.tamano_motor <= 10):
            raise ValueError(f"Tamaño de motor inválido: {self.tamano_motor}")
        if self.mpg <= 0:
            raise ValueError("El consumo (mpg) debe ser positivo.")
        if self.impuesto < 0:
            raise ValueError("El impuesto no puede ser negativo.")

    # ---------- Comportamiento ----------
    def antiguedad(self, anio_referencia: int = 2024) -> int:
        """Devuelve la antigüedad del vehículo respecto a un año dado."""
        return max(anio_referencia - self.anio, 0)

    def es_premium(self) -> bool:
        """Heurística simple: motor grande y modelo de gama alta."""
        modelos_premium = {"7 Series", "8 Series", "X7", "M5", "M4", "X6"}
        return self.tamano_motor >= 3.0 or self.modelo in modelos_premium

    def to_dataframe(self) -> pd.DataFrame:
        """Convierte el objeto en un DataFrame de una fila listo para el modelo."""
        return pd.DataFrame([{
            "model": self.modelo,
            "year": self.anio,
            "mileage": self.kilometraje,
            "transmission": self.transmision,
            "fuelType": self.combustible,
            "engineSize": self.tamano_motor,
            "mpg": self.mpg,
            "tax": self.impuesto,
        }])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:
        return (f"BMW {self.modelo} {self.anio} · "
                f"{self.kilometraje:,} mi · {self.combustible} · "
                f"motor {self.tamano_motor}L")
