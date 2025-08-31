from dagster import Definitions
from .assets import (
    leer_datos,
    datos_procesados,
    metrica_incidencia_7d,
    metrica_factor_crec_7d,
    reporte_excel_covid,
    check_fechas_validas,
    check_columnas_esenciales,
    check_incidencia_rango_valido
)

# Definir todos los assets y checks
all_assets = [
    leer_datos,
    datos_procesados,
    metrica_incidencia_7d,
    metrica_factor_crec_7d,
    reporte_excel_covid
]

all_checks = [
    check_fechas_validas,
    check_columnas_esenciales,
    check_incidencia_rango_valido
]

# Crear las definiciones de Dagster
defs = Definitions(
    assets=all_assets,
    asset_checks=all_checks
)