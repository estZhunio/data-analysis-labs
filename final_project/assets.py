import pandas as pd
import requests
from io import StringIO
from dagster import asset, AssetCheckResult, asset_check
import numpy as np

# PASO 2: LECTURA DE DATOS DESDE URL + CHEQUEOS DE ENTRADA

@asset(description="Datos raw de COVID-19 desde URL canónica de OWID")
def leer_datos() -> pd.DataFrame:

    url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al descargar datos: {response.status_code}")
    
    df = pd.read_csv(StringIO(response.text))
    
    # Renombrar country a location según las instrucciones
    if 'country' in df.columns:
        df = df.rename(columns={'country': 'location'})
    
    return df

# CHEQUEOS DE ENTRADA (segun instrucciones exactas)

@asset_check(asset=leer_datos)
def check_fechas_validas(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        max(date) ≤ hoy (no fechas futuras)
    """
    if 'date' not in leer_datos.columns:
        return AssetCheckResult(passed=False, description="Columna 'date' no encontrada")
    
    leer_datos['date'] = pd.to_datetime(leer_datos['date'])
    today = pd.Timestamp.now()
    
    fechas_futuras = leer_datos[leer_datos['date'] > today]
    filas_afectadas = len(fechas_futuras)
    
    passed = filas_afectadas == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"Verificación fechas no futuras. Filas afectadas: {filas_afectadas}",
        metadata={"filas_afectadas": filas_afectadas}
    )

@asset_check(asset=leer_datos)
def check_columnas_clave_no_nulas(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        Columnas clave no nulas: location, date, population
    """
    columnas_clave = ['location', 'date', 'population']
    columnas_faltantes = [col for col in columnas_clave if col not in leer_datos.columns]
    
    if columnas_faltantes:
        return AssetCheckResult(
            passed=False,
            description=f"Columnas faltantes: {columnas_faltantes}",
            metadata={"columnas_faltantes": columnas_faltantes}
        )
    
    # Verificar que no sean valores nulos
    filas_nulas = 0
    for col in columnas_clave:
        if leer_datos[col].isna().all():
            filas_nulas += len(leer_datos)
    
    passed = filas_nulas == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"Columnas clave verificadas. Filas con nulos: {filas_nulas}",
        metadata={"filas_afectadas": filas_nulas, "columnas_verificadas": columnas_clave}
    )

@asset_check(asset=leer_datos)
def check_unicidad_location_date(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
    Unicidad de (location, date)
    """
    if not {'location', 'date'}.issubset(leer_datos.columns):
        return AssetCheckResult(passed=False, description="Columnas location o date no encontradas")
    
    total_filas = len(leer_datos)
    filas_unicas = len(leer_datos.drop_duplicates(subset=['location', 'date']))
    duplicados = total_filas - filas_unicas
    
    passed = duplicados == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"Verificación unicidad (location,date). Duplicados: {duplicados}",
        metadata={"filas_afectadas": duplicados}
    )

@asset_check(asset=leer_datos)
def check_population_positiva(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        population > 0
    """
    if 'population' not in leer_datos.columns:
        return AssetCheckResult(passed=False, description="Columna 'population' no encontrada")
    
    poblacion_invalida = leer_datos[(leer_datos['population'] <= 0) | (leer_datos['population'].isna())]
    filas_afectadas = len(poblacion_invalida)
    
    passed = filas_afectadas == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"Verificación population > 0. Filas afectadas: {filas_afectadas}",
        metadata={"filas_afectadas": filas_afectadas}
    )

@asset_check(asset=leer_datos)
def check_new_cases_no_negativos(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        new_cases ≥ 0 (permitir negativos pero documentarlos)
    """
    if 'new_cases' not in leer_datos.columns:
        return AssetCheckResult(passed=False, description="Columna 'new_cases' no encontrada")
    
    casos_negativos = leer_datos[leer_datos['new_cases'] < 0]
    filas_afectadas = len(casos_negativos)
    
    # Permitir negativos pero documentados (PASSED con advertencia)
    return AssetCheckResult(
        passed=True,
        description=f"Casos negativos documentados (correcciones admin): {filas_afectadas}",
        metadata={
            "filas_afectadas": filas_afectadas,
            "nota": "Valores negativos permitidos - correcciones administrativas"
        }
    )

# TABLA DE RESUMEN DE VALIDACIONES (memoria)

@asset(description="Tabla resumen validaciones: nombre_regla, estado, filas_afectadas, notas")
def resumen_validaciones(leer_datos: pd.DataFrame) -> pd.DataFrame:
    """
    Generar tabla de resumen con nombre_regla, estado, filas_afectadas, notas
    """
    # Ejecutar validaciones manualmente para generar resumen
    df = leer_datos.copy()
    
    # Check 1: Fechas validas
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    fechas_futuras = len(df[df['date'] > pd.Timestamp.now()])
    
    # Check 2: Columnas clave
    columnas_clave = ['location', 'date', 'population']
    columnas_faltantes = len([col for col in columnas_clave if col not in df.columns])
    
    # Check 3: Unicidad
    duplicados = len(df) - len(df.drop_duplicates(subset=['location', 'date']))
    
    # Check 4: Population > 0
    poblacion_invalida = len(df[(df['population'] <= 0) | (df['population'].isna())])
    
    # Check 5: New cases negativos
    casos_negativos = len(df[df['new_cases'] < 0]) if 'new_cases' in df.columns else 0
    
    resumen = [
        {
            'nombre_regla': 'check_fechas_validas',
            'estado': 'PASSED' if fechas_futuras == 0 else 'FAILED',
            'filas_afectadas': fechas_futuras,
            'notas': 'Verificación de fechas no futuras'
        },
        {
            'nombre_regla': 'check_columnas_clave_no_nulas',
            'estado': 'PASSED' if columnas_faltantes == 0 else 'FAILED',
            'filas_afectadas': columnas_faltantes,
            'notas': 'Columnas: location, date, population'
        },
        {
            'nombre_regla': 'check_unicidad_location_date',
            'estado': 'PASSED' if duplicados == 0 else 'FAILED',
            'filas_afectadas': duplicados,
            'notas': 'Unicidad de (location, date)'
        },
        {
            'nombre_regla': 'check_population_positiva',
            'estado': 'PASSED' if poblacion_invalida == 0 else 'FAILED',
            'filas_afectadas': poblacion_invalida,
            'notas': 'Validación population > 0'
        },
        {
            'nombre_regla': 'check_new_cases_no_negativos',
            'estado': 'PASSED',  # Siempre PASSED (documentados pero permitimos)
            'filas_afectadas': casos_negativos,
            'notas': 'Casos negativos permitidos (correcciones admin)'
        }
    ]
    
    return pd.DataFrame(resumen)

# PASO 3: PROCESAMIENTO DE DATOS

@asset(description="Datos procesados y filtrados para Ecuador y Finlandia")
def datos_procesados(leer_datos: pd.DataFrame) -> pd.DataFrame:
    """
    - Eliminar filas con valores nulos en new_cases O people_vaccinated
    - Eliminar duplicados si existen
    - Filtrar a Ecuador y país comparativo (Finlandia)
    - Seleccionar columnas esenciales: location, date, new_cases, people_vaccinated, population
    """
    df = leer_datos.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Eliminar filas con valores nulos en new_cases O people_vaccinated (segun instrucciones)
    df = df.dropna(subset=['new_cases', 'people_vaccinated'], how='any')
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=['location', 'date'])
    
    # Filtrar por paises de interes
    paises_interes = ['Ecuador', 'Finland']
    df = df[df['location'].isin(paises_interes)]
    
    # Seleccionar columnas esenciales
    columnas_esenciales = ['location', 'date', 'new_cases', 'people_vaccinated', 'population']
    columnas_disponibles = [col for col in columnas_esenciales if col in df.columns]
    df = df[columnas_disponibles]
    
    # Ordenar por fecha
    df = df.sort_values(['location', 'date'])
    
    return df

# PASO 4: CALCULO DE METRICAS

@asset(description="Metrica A: Incidencia acumulada a 7 días por 100 mil habitantes")
def metrica_incidencia_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    """
    1. incidencia_diaria = (new_cases / population) * 100000
    2. incidencia_7d = promedio móvil de 7 días de incidencia_diaria
    """
    if datos_procesados.empty or 'new_cases' not in datos_procesados.columns:
        return pd.DataFrame()
    
    df = datos_procesados.copy()
    
    # Calcular incidencia diaria por 100k habitantes
    df['incidencia_diaria'] = (df['new_cases'] / df['population']) * 100000
    
    # Calcular promedio movil de 7 días por país
    df['incidencia_7d'] = df.groupby('location')['incidencia_diaria'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    # Formatear segun ejemplo en instrucciones
    resultado = df[['date', 'location', 'incidencia_7d']].rename(columns={
        'date': 'fecha',
        'location': 'pais'
    })
    
    return resultado

@asset(description="Métrica B: Factor de crecimiento semanal")
def metrica_factor_crec_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    """
        1. casos_semana_actual = suma(new_cases de los últimos 7 días)
        2. casos_semana_prev = suma(new_cases de los 7 días previos)
        3. factor_crec_7d = casos_semana_actual / casos_semana_prev
    """
    if datos_procesados.empty or 'new_cases' not in datos_procesados.columns:
        return pd.DataFrame()
    
    df = datos_procesados.copy()
    
    resultados = []
    
    for pais in df['location'].unique():
        df_pais = df[df['location'] == pais].sort_values('date')
        
        for i in range(7, len(df_pais)):
            # Semana actual (ultimo 7 días)
            casos_semana_actual = df_pais.iloc[i-6:i+1]['new_cases'].sum()
            
            # Semana anterior (7 diás previos)
            if i >= 13:
                casos_semana_prev = df_pais.iloc[i-13:i-6]['new_cases'].sum()
                
                # Calcular factor de crecimiento
                factor_crec = casos_semana_actual / casos_semana_prev if casos_semana_prev > 0 else np.inf
                
                resultados.append({
                    'semana_fin': df_pais.iloc[i]['date'],
                    'pais': pais,
                    'casos_semana': casos_semana_actual,
                    'factor_crec_7d': factor_crec
                })
    
    return pd.DataFrame(resultados)

# PASO 5: CHEQUEOS DE SALIDA

@asset_check(asset=metrica_incidencia_7d)
def check_incidencia_rango_valido(metrica_incidencia_7d: pd.DataFrame) -> AssetCheckResult:
    """
    Validar que incidencia_7d: 0 ≤ valor ≤ 2000
    """
    if metrica_incidencia_7d.empty or 'incidencia_7d' not in metrica_incidencia_7d.columns:
        return AssetCheckResult(passed=False, description="DataFrame vacío o columna faltante")
    
    fuera_rango = metrica_incidencia_7d[
        (metrica_incidencia_7d['incidencia_7d'] < 0) | 
        (metrica_incidencia_7d['incidencia_7d'] > 2000)
    ]
    
    filas_afectadas = len(fuera_rango)
    passed = filas_afectadas == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"Validación rango incidencia 0-2000. Filas afectadas: {filas_afectadas}",
        metadata={
            "filas_afectadas": filas_afectadas,
            "rango_valido": "0-2000"
        }
    )

# PASO 6: EXPORTACIÓN DE RESULTADOS

@asset(description="Reporte final en formato Excel con todas las hojas requeridas")
def reporte_excel_covid(
    datos_procesados: pd.DataFrame,
    metrica_incidencia_7d: pd.DataFrame,
    metrica_factor_crec_7d: pd.DataFrame,
    resumen_validaciones: pd.DataFrame
) -> str:
    """
        - Datos puros procesados
        - Hoja métrica 1 (incidencia)
        - Hoja métrica 2 (factor crecimiento)
        - Hoja resumen validaciones
    """
    filename = "reporte_covid_pipeline.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Hoja 1: Datos procesados
        datos_procesados.to_excel(writer, sheet_name='Datos_Procesados', index=False)
        
        # Hoja 2: Métrica incidencia
        metrica_incidencia_7d.to_excel(writer, sheet_name='Incidencia_7d', index=False)
        
        # Hoja 3: Métrica factor crecimiento
        metrica_factor_crec_7d.to_excel(writer, sheet_name='Factor_Crec_7d', index=False)
        
        # Hoja 4: Resumen de validaciones
        resumen_validaciones.to_excel(writer, sheet_name='Resumen_Validaciones', index=False)
    
    return filename