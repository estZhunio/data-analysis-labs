from dagster import Definitions
from .assets import (
    leer_datos,
    datos_procesados,
    metrica_incidencia_7d,
    metrica_factor_crec_7d,
    resumen_validaciones,
    reporte_excel_covid,
    check_fechas_validas,
    check_columnas_clave_no_nulas,
    check_unicidad_location_date,
    check_population_positiva,
    check_new_cases_no_negativos,
    check_incidencia_rango_valido
)

# Definir todos los assets y checks
all_assets = [
    leer_datos,
    datos_procesados,
    metrica_incidencia_7d,
    metrica_factor_crec_7d,
    resumen_validaciones,
    reporte_excel_covid
]

all_checks = [
    check_fechas_validas,
    check_columnas_clave_no_nulas,
    check_unicidad_location_date,
    check_population_positiva,
    check_new_cases_no_negativos,
    check_incidencia_rango_valido
]

# Crear las definiciones de Dagster
defs = Definitions(
    assets=all_assets,
    asset_checks=all_checks
)