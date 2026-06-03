"""
entrenar_modelo.py - Script de entrenamiento ejecutado una sola vez.

Este script NO forma parte de la aplicacion Streamlit; se ejecuta
manualmente desde la terminal:

    python entrenar_modelo.py

Lo que hace:
    1. Carga el dataset (Excel con precios en USD)
    2. Aplica el pipeline de limpieza funcional
    3. Ejecuta LazyPredict para identificar el mejor algoritmo
    4. Entrena ese algoritmo sobre todo el dataset
    5. Guarda el modelo en modelo_bmw.joblib (listo para que la app
       lo cargue automaticamente al iniciar)

Después de ejecutar este script, la aplicacion Streamlit puede ser
desplegada y queda lista para predecir sin necesidad de re-entrenar.
"""

import time
from pathlib import Path

from core import (
    cargar_datos, pipeline_limpieza,
    comparar_modelos_lazypredict, entrenar_y_guardar_modelo,
    obtener_mejor_modelo, RUTA_MODELO,
)


def main():
    print("=" * 60)
    print("ENTRENAMIENTO DEL MODELO LS AUTOPREDICT")
    print("=" * 60)

    # 1. Cargar y limpiar datos
    print("\n[1/4] Cargando dataset...")
    df_crudo = cargar_datos()
    df = pipeline_limpieza(df_crudo)
    print(f"      Dataset limpio: {len(df):,} registros")
    print(f"      Precio MIN: $ {df['price'].min():,}")
    print(f"      Precio MAX: $ {df['price'].max():,}")
    print(f"      Precio MEDIANA: $ {df['price'].median():,.0f}")

    # 2. Comparar modelos con LazyPredict
    print("\n[2/4] Comparando modelos con LazyPredict (puede tardar 1-2 min)...")
    t0 = time.time()
    ranking = comparar_modelos_lazypredict(df)
    t_lazy = time.time() - t0
    print(f"      LazyPredict termino en {t_lazy:.1f}s")
    print(f"      Se evaluaron {len(ranking)} algoritmos")

    print("\n      Top 5 modelos:")
    print(ranking.head(5).to_string(index=False))

    # 3. Seleccionar el mejor algoritmo automaticamente
    print("\n[3/4] Seleccionando el mejor algoritmo...")
    mejor, estado = obtener_mejor_modelo(ranking)
    if estado == "ok":
        print(f"      Modelo elegido por LazyPredict: {mejor}")
    else:
        print(f"      Fallback a: {mejor}")

    # 4. Entrenar y guardar el modelo final
    print(f"\n[4/4] Entrenando {mejor} sobre el dataset completo...")
    t0 = time.time()
    pipeline, metricas = entrenar_y_guardar_modelo(df, mejor)
    t_train = time.time() - t0

    print(f"      Entrenamiento terminado en {t_train:.1f}s")
    print("\n" + "=" * 60)
    print("METRICAS DEL MODELO FINAL")
    print("=" * 60)
    print(f"   Modelo:     {metricas['modelo']}")
    print(f"   R²:         {metricas['r2']:.4f}")
    print(f"   MAE:        $ {metricas['mae']:,.0f}")
    print(f"   RMSE:       $ {metricas['rmse']:,.0f}")
    print(f"   n_train:    {metricas['n_train']:,} registros")
    print(f"   n_test:     {metricas['n_test']:,} registros")

    print(f"\n✅ Modelo guardado en: {RUTA_MODELO.resolve()}")
    print("✅ La aplicacion Streamlit ya esta lista para predecir.")
    print("=" * 60)


if __name__ == "__main__":
    main()
