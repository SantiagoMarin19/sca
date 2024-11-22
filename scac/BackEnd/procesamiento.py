import pandas as pd
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def procesar_archivo_instructores(file_instru, file_sofia, plantilla_path):
    # Leer hoja "Validar nombre aprendiz" del archivo de instructores
    instru_df = pd.read_excel(file_instru, sheet_name="Validar nombre aprendiz", header=None)
    
    # Validar que la celda D2 contiene el Código de Ficha
    try:
        codigo_ficha = instru_df.iloc[1, 3]  # Fila 2, columna 4 (D2)
        if pd.isna(codigo_ficha):
            raise ValueError("La celda D2 está vacía o no contiene un Código de Ficha válido.")
    except IndexError:
        raise ValueError("No se encontró la celda D2 en la hoja especificada.")
    
    logger.info(f"Código de Ficha identificado: {codigo_ficha}")
    
    # Tomar los encabezados de la fila 10
    encabezados = instru_df.iloc[9]
    instru_df = instru_df.iloc[10:]  # Eliminar filas hasta la fila 10
    instru_df.columns = encabezados
    instru_df.reset_index(drop=True, inplace=True)
    
    # Renombrar columnas de Instructores
    instru_df.rename(columns={
        "Tipo": "TIPO",
        "Documento de identificación": "DOCUMENTO_DE_IDENTIFICACION",
        "Nombre completo SENA": "NOMBRE_COMPLETO_SENA"
    }, inplace=True)
    
    # Leer el archivo Sofía desde la fila correcta
    sofia_df = pd.read_excel(file_sofia, header=1)  # Cambiar header a 1 para leer desde la fila 2
    
    # Renombrar columnas de Sofía
    sofia_df.rename(columns={
        "Ficha": "FICHA",
        "Tipo Programa": "TIPO_PROGRAMA",
        "Nivel Formación": "NIVEL_FORMACION",
        "Denominación Programa": "DENOMINACION_PROGRAMA",
        "Tipo Documento": "TIPO",
        "No. Documento": "DOCUMENTO_DE_IDENTIFICACION",
        "Nombre Aprendiz": "NOMBRE_COMPLETO_SENA"
    }, inplace=True)
    
    logger.info(f"Columnas en Sofía después del renombrado: {sofia_df.columns}")
    
    # Filtrar registros de Sofía por Código Ficha
    sofia_filtrado = sofia_df[sofia_df["FICHA"] == int(codigo_ficha)]
    if sofia_filtrado.empty:
        logger.error(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")
        raise ValueError(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")
    logger.info(f"Registros filtrados en Sofía: {len(sofia_filtrado)}")
    
    # Asegurar que las columnas para merge tengan el mismo tipo
    instru_df["DOCUMENTO_DE_IDENTIFICACION"] = instru_df["DOCUMENTO_DE_IDENTIFICACION"].astype(str)
    sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION"] = sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION"].astype(str)
    
    # Realizar la validación
    validacion_df = pd.merge(
        instru_df,
        sofia_filtrado[[
            "FICHA", "TIPO_PROGRAMA", "NIVEL_FORMACION", "DENOMINACION_PROGRAMA",
            "TIPO", "DOCUMENTO_DE_IDENTIFICACION", "NOMBRE_COMPLETO_SENA"
        ]],
        on=['TIPO', 'DOCUMENTO_DE_IDENTIFICACION'],
        how='left',
        suffixes=('_x', '_y')
    )
    
    # Agregar columna de verificación
    validacion_df['COINCIDENCIA'] = validacion_df.apply(
        lambda row: "VERIFICADO" if row['NOMBRE_COMPLETO_SENA_x'] == row['NOMBRE_COMPLETO_SENA_y'] else "NO VERIFICADO",
        axis=1
    )
    
    # Exportar resultados
    output_path = "resultado_validaciones.xlsx"
    validacion_df.to_excel(output_path, index=False, engine='openpyxl')
    logger.info(f"Archivo de validaciones generado: {output_path}")

    # Devolver archivo como stream
    return open(output_path, "rb")
