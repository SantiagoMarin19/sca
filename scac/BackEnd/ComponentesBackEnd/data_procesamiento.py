import pandas as pd
import numpy as np
from ComponentesBackEnd.logger_configuracion import logger

def limpiar_documento(doc):
    if pd.isna(doc):
        return doc
    return ''.join(filter(str.isdigit, str(doc)))




def procesar_archivo_sin_juicios(file_instru,file_sofia):
    instru_df = pd.read_excel(file_instru, sheet_name="Validar nombre aprendiz", header=None, dtype=str)
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
    else:
        encabezados = instru_df.iloc[9]
        instru_df = instru_df.iloc[10:]
        
    instru_df.columns = encabezados
    instru_df.reset_index(drop=True, inplace=True)
    
    instru_df.rename(columns={
        # archivo 1
        "Tipo": "TIPO_INSTRU",
        "Documento de identificación": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombre completo CONSULTA": "NOMBRE_COMPLETO_SENA_INSTRU",
        # archivo 2
        "Documento de identidad": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombres y Apellidos PROCURADURÍA/REGISTRADURÍA": "NOMBRE_COMPLETO_SENA_INSTRU",
    }, inplace=True)

    # Log de las columnas que se están renombrando
    logger.info("Renombrando las columnas en el archivo de instructores...")
    logger.debug(f"Columnas renombradas: {instru_df.columns.tolist()}")

    instru_df.dropna(subset=["NOMBRE_COMPLETO_SENA_INSTRU", "DOCUMENTO_DE_IDENTIFICACION_INSTRU"], inplace=True)
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def procesar_archivo_instructores(file_instru, file_sofia, file_juicio):
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
    else:
        encabezados = instru_df.iloc[9]
        instru_df = instru_df.iloc[10:]
        
    instru_df.columns = encabezados
    instru_df.reset_index(drop=True, inplace=True)
    
    instru_df.rename(columns={
        # archivo 1
        "Tipo": "TIPO_INSTRU",
        "Documento de identificación": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombre completo CONSULTA": "NOMBRE_COMPLETO_SENA_INSTRU",
        # archivo 2
        "Documento de identidad": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombres y Apellidos PROCURADURÍA/REGISTRADURÍA": "NOMBRE_COMPLETO_SENA_INSTRU",
    }, inplace=True)

    # Log de las columnas que se están renombrando
    logger.info("Renombrando las columnas en el archivo de instructores...")
    logger.debug(f"Columnas renombradas: {instru_df.columns.tolist()}")

    instru_df.dropna(subset=["NOMBRE_COMPLETO_SENA_INSTRU", "DOCUMENTO_DE_IDENTIFICACION_INSTRU"], inplace=True)
    
    # Leer y procesar archivo juicio
    logger.info("Leyendo el archivo de juicio...")
    juicio_df = pd.read_excel(file_juicio, header=12, dtype=str)
    logger.info("Archivo de juicio leído correctamente.")
    
    logger.info(f"Columnas originales: {juicio_df.columns}")
    
    juicio_df.rename(columns={
        "Número de Documento": "DOCUMENTO_DE_IDENTIFICACION_JUICIOS",
        "Juicio de Evaluación": "JUICIOS_EVALUATIVO"
    }, inplace=True)
    
    logger.info(f"Columnas renombradas: {juicio_df.columns.tolist()}")
    
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
    juicio_df["DOCUMENTO_DE_IDENTIFICACION_COMP"] = juicio_df["DOCUMENTO_DE_IDENTIFICACION_JUICIOS"].apply(limpiar_documento)
    
    instru_df["DOCUMENTO_DE_IDENTIFICACION_INSTRU"] = instru_df["DOCUMENTO_DE_IDENTIFICACION_COMP"]
    sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_SOFIA"] = sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_COMP"]
    juicio_df["DOCUMENTO_DE_IDENTIFICACION_JUICIOS"] = juicio_df["DOCUMENTO_DE_IDENTIFICACION_COMP"]
    
    # Verificar juicios evaluativos
    logger.info("Verificando juicios evaluativos...")
    juicio_counts = juicio_df.groupby("DOCUMENTO_DE_IDENTIFICACION_COMP").agg(
        total_juicios=pd.NamedAgg(column="JUICIOS_EVALUATIVO", aggfunc="count"),
        juicios_aprobados=pd.NamedAgg(column="JUICIOS_EVALUATIVO", aggfunc=lambda x: (x == "APROBADO").sum())
    ).reset_index()
    
    instru_df = pd.merge(instru_df, juicio_counts, left_on="DOCUMENTO_DE_IDENTIFICACION_COMP", right_on="DOCUMENTO_DE_IDENTIFICACION_COMP", how="left")
    instru_df["JUICIOS_EVALUATIVO"] = instru_df.apply(
        lambda row: f"Aprobó {row['juicios_aprobados']} de {row['total_juicios']} juicios" if pd.notna(row['total_juicios']) else "No tiene juicios",
        axis=1
    )
    instru_df.drop(columns=["total_juicios", "juicios_aprobados"], inplace=True)
    
    
    
    return instru_df, sofia_filtrado, juicio_df





def realizar_validacion(instru_df, sofia_filtrado, juicio_df):
    logger.info("Comenzando la validación y comparación de datos...")

    # Log de las columnas que se están comparando
    logger.debug(f"Columnas de Instructores: {instru_df.columns.tolist()}")
    logger.debug(f"Columnas de Sofía: {sofia_filtrado.columns.tolist()}")
    logger.debug(f"Columnas de Juicios: {juicio_df.columns.tolist()}")

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

def ajustar_nombre(nombre_instru, nombre_sofia):
    if pd.isna(nombre_instru) or pd.isna(nombre_sofia):
        return nombre_instru
    
    # Limpiar y ajustar ambos nombres
    nombre_instru_limpio = ''.join([char if char.isupper() else ' ' + char for char in str(nombre_instru)]).strip().upper()
    nombre_sofia_limpio = str(nombre_sofia).strip().replace(" ", "").upper()

    # Comparar los nombres
    if nombre_instru_limpio == nombre_sofia_limpio:
        return nombre_sofia  # Si coinciden, devolver el nombre de Sofía
    
    return nombre_instru  # Si no coinciden, devolver el nombre del instructor

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
        
        # Obtener y ajustar los nombres
        nombre_instru = str(row['NOMBRE_COMPLETO_SENA_INSTRU']).strip() if not pd.isna(row['NOMBRE_COMPLETO_SENA_INSTRU']) else ""
        nombre_sofia = str(row['NOMBRE_COMPLETO_SENA_SOFIA']).strip() if not pd.isna(row['NOMBRE_COMPLETO_SENA_SOFIA']) else ""
        
        # Llamar a la función para ajustar el nombre si hay discrepancia
        nombre_instru_ajustado = ajustar_nombre(nombre_instru, nombre_sofia)
        
        if nombre_instru_ajustado != nombre_sofia:
            discrepancias.append(f"Discrepancia en Nombre: Instructores ({nombre_instru}) vs Sofía ({nombre_sofia})")
        
        # Si los nombres coinciden, marcar como VERDADERO
        if nombre_instru_ajustado == nombre_sofia:
            return "VERDADERO"
    
    # Si hay discrepancias, retornarlas
    return "FALSO - " + "; ".join(discrepancias) if discrepancias else "VERDADERO"