import pandas as pd
from dagster import asset, AssetCheckResult, asset_check
import numpy as np

# ============================================================================
# LECTURA DE DATOS SIN TRANSFORMAR
# ============================================================================

@asset(description="Datos raw de COVID-19 desde compact.csv")
def leer_datos() -> pd.DataFrame:

    df = pd.read_csv('data/compact.csv')
    return df

# ============================================================================
# CHEQUEOS DE ENTRADA
# ============================================================================

@asset_check(asset=leer_datos)
def check_fechas_validas(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        Verifica que no hay fechas futuras en los datos
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
        description=f"Fechas futuras encontradas: {filas_afectadas} filas",
        metadata={"filas_afectadas": filas_afectadas}
    )

@asset_check(asset=leer_datos)
def check_columnas_esenciales(leer_datos: pd.DataFrame) -> AssetCheckResult:
    """
        Verifica que las columnas esenciales existen
    """
    columnas_requeridas = ['country', 'date', 'population']
    columnas_faltantes = [col for col in columnas_requeridas if col not in leer_datos.columns]
    
    if columnas_faltantes:
        return AssetCheckResult(
            passed=False,
            description=f"Columnas faltantes: {columnas_faltantes}"
        )
    
    passed = len(columnas_faltantes) == 0
    
    return AssetCheckResult(
        passed=passed,
        description="Todas las columnas esenciales están presentes",
        metadata={"columnas_verificadas": columnas_requeridas}
    )

# ============================================================================
# PASO 3: PROCESAMIENTO DE DATOS
# ============================================================================

@asset(description="Datos procesados y filtrados para Ecuador y Finland")
def datos_procesados(leer_datos: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa y filtra los datos para Ecuador y Perú
    """
    df = leer_datos.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Filtrar por paises interesados
    paises_interes = ['Ecuador', 'Finland']
    df = df[df['country'].isin(paises_interes)]
    
    # Seleccionar columnas esenciales
    columnas_esenciales = ['country', 'date', 'new_cases', 'people_vaccinated', 'population']
    columnas_disponibles = [col for col in columnas_esenciales if col in df.columns]
    df = df[columnas_disponibles]
    
    # Eliminar filas con valores nulos en new_cases
    if 'new_cases' in df.columns:
        df_limpio = df.dropna(subset=['new_cases'])
    else:
        df_limpio = df
    
    # Eliminar duplicados
    df_limpio = df_limpio.drop_duplicates(subset=['country', 'date'])
    
    # Ordenar por fecha
    df_limpio = df_limpio.sort_values(['country', 'date'])
    
    return df_limpio

# ============================================================================
# PASO 4: CALCULO DE METRICAS
# ============================================================================

@asset(description="Metrica A: Incidencia acumulada a 7 días por 100 mil habitantes")
def metrica_incidencia_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la incidencia acumulada a 7 días por 100 mil habitantes
    """
    if 'new_cases' not in datos_procesados.columns or 'population' not in datos_procesados.columns:
        return pd.DataFrame()
    
    df = datos_procesados.copy()
    
    # Calcular incidencia diaria por 100k habitantes
    df['incidencia_diaria'] = (df['new_cases'] / df['population']) * 100000
    
    # Calcular promedio móvil de 7 días por país
    df['incidencia_7d'] = df.groupby('country')['incidencia_diaria'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    # Formatear resultado
    resultado = df[['date', 'country', 'incidencia_7d']].rename(columns={
        'date': 'fecha',
        'country': 'pais'
    })
    
    return resultado

@asset(description="Métrica B: Factor de crecimiento semanal")
def metrica_factor_crec_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el factor de crecimiento semanal de casos
    """
    if 'new_cases' not in datos_procesados.columns:
        return pd.DataFrame()
    
    df = datos_procesados.copy()
    
    resultados = []
    
    for pais in df['country'].unique():
        df_pais = df[df['country'] == pais].sort_values('date')
        
        for i in range(7, len(df_pais)):
            # Semana actual (últimos 7 días)
            casos_semana_actual = df_pais.iloc[i-6:i+1]['new_cases'].sum()
            
            # Semana anterior (7 días previos)
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

# ============================================================================
# PASO 5: CHEQUEOS DE SALIDA
# ============================================================================

@asset_check(asset=metrica_incidencia_7d)
def check_incidencia_rango_valido(metrica_incidencia_7d: pd.DataFrame) -> AssetCheckResult:
    """
    Verifica que la incidencia está en un rango válido (0-2000)
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
        description=f"Valores de incidencia fuera del rango (0-2000): {filas_afectadas} filas",
        metadata={
            "filas_afectadas": filas_afectadas,
            "rango_valido": "0-2000"
        }
    )

# ============================================================================
# PASO 6: EXPORTACIÓN DE RESULTADOS
# ============================================================================

@asset(description="Reporte final en formato Excel")
def reporte_excel_covid(
    datos_procesados: pd.DataFrame,
    metrica_incidencia_7d: pd.DataFrame,
    metrica_factor_crec_7d: pd.DataFrame
) -> str:
    """
    Exporta todos los resultados a un archivo Excel
    """
    filename = "reporte_covid_pipeline.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Hoja 1: Datos procesados
        datos_procesados.to_excel(writer, sheet_name='Datos_Procesados', index=False)
        
        # Hoja 2: Métrica incidencia
        metrica_incidencia_7d.to_excel(writer, sheet_name='Incidencia_7d', index=False)
        
        # Hoja 3: Métrica factor crecimiento
        metrica_factor_crec_7d.to_excel(writer, sheet_name='Factor_Crec_7d', index=False)
    
    return filename