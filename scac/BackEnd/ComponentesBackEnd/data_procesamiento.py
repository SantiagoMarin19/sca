import pandas as pd
import numpy as np
from ComponentesBackEnd.logger_configuracion import logger

def limpiar_documento(doc):
    doc_str = str(doc).replace('E+', '').replace('.', '')
    return ''.join(filter(str.isdigit, doc_str))

def procesar_archivo_instructores(file_instru, file_sofia):
    # Leer archivo de instructores
    logger.info("Leyendo el archivo de instructores...")
    instru_df = pd.read_excel(file_instru, sheet_name="Validar nombre aprendiz", header=None, dtype=str)
    logger.info("Archivo de instructores leído correctamente.")
    
    # Validar que la celda D2 contiene el Código de Ficha
    logger.info("Extrayendo el Código de Ficha de la celda D2...")
    try:
        codigo_ficha = instru_df.iloc[1, 3]
        if pd.isna(codigo_ficha):
            raise ValueError("La celda D2 está vacía o no contiene un Código de Ficha válido.")
        logger.info(f"Código de Ficha identificado: {codigo_ficha}")
    except IndexError:
        logger.error("No se encontró la celda D2 en la hoja especificada.")
        raise ValueError("No se encontró la celda D2 en la hoja especificada.")

    # Procesar archivo de instructores
    if instru_df.iloc[9].isnull().any():
        encabezados = instru_df.iloc[10]
        instru_df = instru_df.iloc[11:]
    else :
        encabezados = instru_df.iloc[9]
        instru_df = instru_df.iloc[10:]
        
        
    instru_df.columns = encabezados
    instru_df.reset_index(drop=True, inplace=True)
    
    instru_df.rename(columns={
        #archivo 1
        "Tipo": "TIPO_INSTRU",
        "Documento de identificación": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombre completo CONSULTA": "NOMBRE_COMPLETO_SENA_INSTRU",
        #archivo2
        "Documento de identidad":"DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombres y Apellidos PROCURADURÍA/REGISTRADURÍA":"NOMBRE_COMPLETO_SENA_INSTRU",
    }, inplace=True)

    # Log de las columnas que se están renombrando
    logger.info("Renombrando las columnas en el archivo de instructores...")
    logger.debug(f"Columnas renombradas: {instru_df.columns.tolist()}")

    instru_df.dropna(subset=["NOMBRE_COMPLETO_SENA_INSTRU", "DOCUMENTO_DE_IDENTIFICACION_INSTRU"], inplace=True)

    # Leer y procesar archivo Sofía
    sofia_df = pd.read_excel(file_sofia, header=1)
    sofia_df.rename(columns={
        "Ficha": "FICHA",
        "Tipo Programa": "TIPO_PROGRAMA",
        "Nivel Formación": "NIVEL_FORMACION",
        "Denominación Programa": "DENOMINACION_PROGRAMA",
        "Tipo Documento": "TIPO_SOFIA",
        "No. Documento": "DOCUMENTO_DE_IDENTIFICACION_SOFIA",
        "Nombre Aprendiz": "NOMBRE_COMPLETO_SENA_SOFIA"
    }, inplace=True)

    # Log de las columnas que se están renombrando en el archivo Sofía
    logger.info("Renombrando las columnas en el archivo Sofía...")
    logger.debug(f"Columnas renombradas: {sofia_df.columns.tolist()}")

    sofia_filtrado = sofia_df[sofia_df["FICHA"] == int(codigo_ficha)]
    if sofia_filtrado.empty:
        logger.error(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")
        raise ValueError(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")

    # Log de las filas filtradas
    logger.info(f"Filas filtradas en Sofía para la ficha {codigo_ficha}: {sofia_filtrado.shape[0]} filas.")

    # Preparar columnas de comparación
    instru_df["DOCUMENTO_DE_IDENTIFICACION_COMP"] = instru_df["DOCUMENTO_DE_IDENTIFICACION_INSTRU"].apply(limpiar_documento)
    sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_COMP"] = sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_SOFIA"].apply(limpiar_documento)
    
    instru_df["DOCUMENTO_DE_IDENTIFICACION_INSTRU"] = instru_df["DOCUMENTO_DE_IDENTIFICACION_COMP"]
    sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_SOFIA"] = sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_COMP"]

    return instru_df, sofia_filtrado

def realizar_validacion(instru_df, sofia_filtrado):
    logger.info("Comenzando la validación y comparación de datos...")

    # Log de las columnas que se están comparando
    logger.debug(f"Columnas de Instructores: {instru_df.columns.tolist()}")
    logger.debug(f"Columnas de Sofía: {sofia_filtrado.columns.tolist()}")

    validacion_df = pd.merge(
        instru_df,
        sofia_filtrado,
        left_on="DOCUMENTO_DE_IDENTIFICACION_COMP",
        right_on="DOCUMENTO_DE_IDENTIFICACION_COMP",
        how='outer',
        suffixes=('_instru', '_sofia')
    )

    # Log de las filas del DataFrame resultante
    logger.info(f"Total de registros después de la comparación: {validacion_df.shape[0]} filas.")

    validacion_df['COINCIDENCIA'] = validacion_df.apply(verificar_discrepancias, axis=1)
    validacion_df.drop_duplicates(subset=['DOCUMENTO_DE_IDENTIFICACION_COMP'], keep='first', inplace=True)

    return validacion_df

def verificar_discrepancias(row):
    discrepancias = []
    
    if pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_INSTRU']) and not pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_SOFIA']):
        discrepancias.append("Documento sólo en Sofía")
    elif not pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_INSTRU']) and pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_SOFIA']):
        discrepancias.append("Documento sólo en Instructores")
    else:
        tipo_instru = str(row['TIPO_INSTRU']).strip()
        tipo_sofia = str(row['TIPO_SOFIA']).strip()
        if tipo_instru != tipo_sofia:
            discrepancias.append(f"Discrepancia en Tipo de Documento: Instructores ({tipo_instru}) vs Sofía ({tipo_sofia})")
        
        nombre_instru = str(row['NOMBRE_COMPLETO_SENA_INSTRU']).strip()
        nombre_sofia = str(row['NOMBRE_COMPLETO_SENA_SOFIA']).strip()
        if nombre_instru != nombre_sofia:
            discrepancias.append(f"Discrepancia en Nombre: Instructores ({nombre_instru}) vs Sofía ({nombre_sofia})")

    return "FALSO - " + "; ".join(discrepancias) if discrepancias else "VERDADERO"
