import pandas as pd

def crear_tabla_perfilado():
    """
    Script de exploración inicial según las instrucciones del proyecto
    Genera tabla_perfilado.csv requerida
    """
    print("=== EXPLORACIÓN INICIAL DE DATOS COVID-19 ===")
    
    # Leer el archivo
    df = pd.read_csv('data/compact.csv')
    print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # Filtrar por Ecuador y país comparativo (Finland)
    paises_interes = ['Ecuador', 'Finland']
    df_filtrado = df[df['country'].isin(paises_interes)]
    
    print(f"Datos filtrados para Ecuador y Finland: {len(df_filtrado)} registros")
    
    # Analisis basico requerido
    
    # 1. Columnas y tipos de datos
    columnas_tipos = df_filtrado.dtypes.to_dict()
    print("\n1. Columnas y tipos de datos:")
    for col, tipo in list(columnas_tipos.items())[:10]:  # Mostrar primeras 10
        print(f"   {col}: {tipo}")
    
    # 2. Mínimo y máximo de new_cases
    new_cases_min = df_filtrado['new_cases'].min()
    new_cases_max = df_filtrado['new_cases'].max()
    print(f"\n2. Rango new_cases: {new_cases_min} a {new_cases_max}")
    
    # 3. Porcentaje de valores faltantes
    missing_new_cases = (df_filtrado['new_cases'].isna().sum() / len(df_filtrado)) * 100
    missing_vaccinated = (df_filtrado['people_vaccinated'].isna().sum() / len(df_filtrado)) * 100
    
    print(f"\n3. Valores faltantes:")
    print(f"   new_cases: {missing_new_cases:.1f}%")
    print(f"   people_vaccinated: {missing_vaccinated:.1f}%")
    
    # 4. Rango de fechas
    fecha_min = df_filtrado['date'].min()
    fecha_max = df_filtrado['date'].max()
    print(f"\n4. Rango de fechas: {fecha_min} a {fecha_max}")
    
    # Información adicional útil
    registros_ecuador = len(df_filtrado[df_filtrado['country'] == 'Ecuador'])
    registros_finland = len(df_filtrado[df_filtrado['country'] == 'Finland'])
    
    # Crear tabla de perfilado como diccionario
    perfilado = {
        'total_filas_dataset': len(df),
        'total_columnas': len(df.columns),
        'paises_analizados': 'Ecuador, Finland',
        'registros_ecuador': registros_ecuador,
        'registros_finland': registros_finland,
        'fecha_inicio': fecha_min,
        'fecha_fin': fecha_max,
        'new_cases_minimo': new_cases_min,
        'new_cases_maximo': new_cases_max,
        'porcentaje_missing_new_cases': round(missing_new_cases, 1),
        'porcentaje_missing_people_vaccinated': round(missing_vaccinated, 1),
        'columnas_principales': 'country,date,new_cases,people_vaccinated,population'
    }
    
    # Convertir a DataFrame y guardar
    df_perfilado = pd.DataFrame([perfilado])
    df_perfilado.to_csv('tabla_perfilado.csv', index=False)
    
    print(f"\n=== RESUMEN DEL PERFILADO ===")
    for key, value in perfilado.items():
        print(f"{key}: {value}")
    
    print(f"\n✅ Tabla de perfilado guardada como 'tabla_perfilado.csv'")
    
    # Mostrar muestra de datos para verificación
    print(f"\n=== MUESTRA DE DATOS (Ecuador) ===")
    ecuador_sample = df_filtrado[df_filtrado['country'] == 'Ecuador'][['date', 'new_cases', 'people_vaccinated', 'population']].head(5)
    print(ecuador_sample)
    
    return perfilado

if __name__ == "__main__":
    crear_tabla_perfilado()