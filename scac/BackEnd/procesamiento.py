import pandas as pd
from io import BytesIO

def procesar_archivos(file1, file2, plantilla_path):
    # Cargar todas las hojas del archivo Excel como un diccionario de DataFrames
    archinstru_sheets = pd.read_excel(file1, sheet_name=None)  # Lee todas las hojas
    archsofia_sheets = pd.read_excel(file2, sheet_name=None)  # Lee todas las hojas
    plantilla = pd.read_excel(plantilla_path)  # Solo una hoja, si es el caso

    # Acceder a las hojas por su nombre
    archinstru = pd.concat(archinstru_sheets.values(), ignore_index=True)
    archsofia = pd.concat(archsofia_sheets.values(), ignore_index=True)

    # Normalizar los nombres de las columnas para evitar problemas de comparación
    archinstru.columns = archinstru.columns.str.strip().str.upper()
    archsofia.columns = archsofia.columns.str.strip().str.upper()
    plantilla.columns = plantilla.columns.str.strip().str.upper()

    # Columnas de la plantilla
    columnas_plantilla = ['FICHA', 'TIPO PROGRAMA', 'NIVEL FORMACION', 'DENOMINACION PROGRAMA', 
                          'TIPO DE DOCUMENTO', 'No. DOCUMENTO', 'NOMBRE APRENDIZ EN SOFIA', 
                          'NOMBRE DE VALIDACION', 'VERIFICACION']

    # Diccionario de mapeo para relacionar columnas de archinstru y archsofia con la plantilla
    mapeo_columnas = {
        'FICHA': ['FICHA', 'CODIGO FICHA'],  # En ambos
        'TIPO PROGRAMA': ['TIPO PROGRAMA'],  # Solo en archsofia
        'NIVEL FORMACION': ['NIVEL FORMACION'],  # Solo en archsofia
        'DENOMINACION PROGRAMA': ['DENOMINACION PROGRAMA', 'PROGRAMA DE FORMACION'],  # En ambos
        'TIPO DOCUMENTO': ['TIPO DOCUMENTO', 'TIPO'],  # En ambos
        'No. DOCUMENTO': ['No. DOCUMENTO', 'DOCUMENTO DE IDENTIFICACION'],  # En ambos
        'NOMBRE APRENDIZ EN SOFIA': ['NOMBRE APRENDIZ', 'NOMBRE COMPLETO SENA'],  # En ambos
        'NOMBRE DE VALIDACION': ['NOMBRE COMPLETO CONSULTA'],  # Solo en archinstru
    }

    # Unir ambos DataFrames (archinstru y archsofia) en un solo DataFrame combinado
    df_combined = pd.concat([archinstru, archsofia], ignore_index=True)

    # Crear un DataFrame para la plantilla final con las columnas requeridas
    resultado = pd.DataFrame(columns=columnas_plantilla)

    # Rellenar las columnas de la plantilla combinando los datos
    for columna_plantilla, posibles_nombres in mapeo_columnas.items():
     datos_combinados = pd.Series(dtype="object")
    for nombre in posibles_nombres:
        if nombre in df_combined.columns:
            # Filtrar NaN antes de combinar
            datos_combinados = datos_combinados.combine_first(df_combined[nombre].dropna())
    
    resultado[columna_plantilla] = datos_combinados

    # # Determinar el estado de los aprendices (Coincide/No Coincide)
    # resultado['ESTADO'] = resultado.apply(
    #     lambda row: 'Coincide' if (
    #         row['No. DOCUMENTO'] in archinstru['DOCUMENTO DE IDENTIFICACION'].values and
    #         row['NOMBRE APRENDIZ EN SOFIA'] in archinstru['NOMBRE COMPLETO CONSULTA'].values and
    #         row['DENOMINACION PROGRAMA'] in archinstru['PROGRAMA DE FORMACION'].values and
    #         row['TIPO DE DOCUMENTO'] in archinstru['TIPO DOCUMENTO'].values and
    #         row['TIPO PROGRAMA'] in archsofia['TIPO PROGRAMA'].values and
    #         row['NIVEL FORMACION'] in archsofia['NIVEL FORMACION'].values and
    #         row['NOMBRE DE VALIDACION'] in archinstru['NOMBRE COMPLETO CONSULTA'].values and
    #         row['FICHA'] in archinstru['FICHA'].values
    #     ) else 'No Coincide', 
    #     axis=1
    # )

    # Guardar el resultado en un archivo Excel
    output = BytesIO()
    resultado.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)  # Regresar al inicio del archivo
    print(archinstru.columns)
    return output
