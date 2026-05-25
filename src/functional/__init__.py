"""Capa funcional - transformaciones puras de DataFrames."""
from .transformaciones import (
    eliminar_duplicados, eliminar_atipicos_iqr, limpiar_espacios_modelo,
    agregar_antiguedad, agregar_km_por_anio, filtrar_precio_valido,
    componer, pipeline_default, aplicar_a_columnas, media_truncada,
)
__all__ = [
    "eliminar_duplicados", "eliminar_atipicos_iqr", "limpiar_espacios_modelo",
    "agregar_antiguedad", "agregar_km_por_anio", "filtrar_precio_valido",
    "componer", "pipeline_default", "aplicar_a_columnas", "media_truncada",
]
