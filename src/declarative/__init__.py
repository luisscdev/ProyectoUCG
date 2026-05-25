"""Capa declarativa - queries sobre DataFrames."""
from .consultas import (
    precio_promedio_por_modelo, precio_promedio_por_anio,
    distribucion_combustible, distribucion_transmision,
    resumen_descriptivo, correlaciones, buscar_por_filtros, kpis_globales,
)
__all__ = [
    "precio_promedio_por_modelo", "precio_promedio_por_anio",
    "distribucion_combustible", "distribucion_transmision",
    "resumen_descriptivo", "correlaciones", "buscar_por_filtros", "kpis_globales",
]
