import pandas as pd
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def procesar_archivo_instructores(file_instru, file_sofia):
    # Leer archivo de instructores
    instru_df = pd.read_excel(file_instru, sheet_name="Validar nombre aprendiz", header=None)

    # Validar que la celda D2 contiene el Código de Ficha
    try:
        codigo_ficha = instru_df.iloc[1, 3]  # Fila 2, columna 4 (D2)
        if pd.isna(codigo_ficha):
            raise ValueError("La celda D2 está vacía o no contiene un Código de Ficha válido.")
    except IndexError:
        raise ValueError("No se encontró la celda D2 en la hoja especificada.")

    logger.info(f"Código de Ficha identificado: {codigo_ficha}")

    # Tomar encabezados de la fila 10
    encabezados = instru_df.iloc[9]
    instru_df = instru_df.iloc[10:]  # Eliminar filas hasta la fila 10
    instru_df.columns = encabezados
    instru_df.reset_index(drop=True, inplace=True)

    # Renombrar columnas de instructores
    instru_df.rename(columns={
        "Tipo": "TIPO_INSTRU",
        "Documento de identificación": "DOCUMENTO_DE_IDENTIFICACION_INSTRU",
        "Nombre completo SENA": "NOMBRE_COMPLETO_SENA_INSTRU"
    }, inplace=True)

    # Filtrar datos sin nombre o identificación
    instru_df.dropna(subset=["NOMBRE_COMPLETO_SENA_INSTRU", "DOCUMENTO_DE_IDENTIFICACION_INSTRU"], inplace=True)

    # Leer archivo Sofía desde la fila correcta
    sofia_df = pd.read_excel(file_sofia, header=1)  # Leer desde fila 2
    sofia_df.rename(columns={
        "Ficha": "FICHA",
        "Tipo Programa": "TIPO_PROGRAMA",
        "Nivel Formación": "NIVEL_FORMACION",
        "Denominación Programa": "DENOMINACION_PROGRAMA",
        "Tipo Documento": "TIPO_SOFIA",
        "No. Documento": "DOCUMENTO_DE_IDENTIFICACION_SOFIA",
        "Nombre Aprendiz": "NOMBRE_COMPLETO_SENA_SOFIA"
    }, inplace=True)

    # Filtrar registros de Sofía por Código Ficha
    sofia_filtrado = sofia_df[sofia_df["FICHA"] == int(codigo_ficha)]
    if sofia_filtrado.empty:
        logger.error(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")
        raise ValueError(f"No se encontraron registros en Sofía para la ficha {codigo_ficha}.")
    logger.info(f"Registros filtrados en Sofía: {len(sofia_filtrado)}")

    # Crear columnas de comparación en formato de texto
    instru_df["DOCUMENTO_DE_IDENTIFICACION_COMP"] = instru_df["DOCUMENTO_DE_IDENTIFICACION_INSTRU"].astype(str)
    sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_COMP"] = sofia_filtrado["DOCUMENTO_DE_IDENTIFICACION_SOFIA"].astype(str)

    # Realizar la validación
    validacion_df = pd.merge(
        instru_df,
        sofia_filtrado,
        on=['DOCUMENTO_DE_IDENTIFICACION_COMP'],
        how='outer',
        suffixes=('_instru', '_sofia')
    )

    # Consolidar filas y manejar discrepancias en una sola fila
    def verificar_discrepancias(row):
        discrepancias = []
        if pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_INSTRU']) and not pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_SOFIA']):
            discrepancias.append("Discrepancias en el documento de identificacion ")
        elif not pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_INSTRU']) and pd.isna(row['DOCUMENTO_DE_IDENTIFICACION_SOFIA']):
            discrepancias.append("Discrepancias en el documento de identificacion ")
        else:
            if row['TIPO_INSTRU'] != row['TIPO_SOFIA']:
                discrepancias.append(f"Discrepancia en Tipo de Documento: Instructores ({row['TIPO_INSTRU']}) vs Sofía ({row['TIPO_SOFIA']})")
            if row['NOMBRE_COMPLETO_SENA_INSTRU'] != row['NOMBRE_COMPLETO_SENA_SOFIA']:
                discrepancias.append(f"Discrepancia en Nombre: Instructores ({row['NOMBRE_COMPLETO_SENA_INSTRU']}) vs Sofía ({row['NOMBRE_COMPLETO_SENA_SOFIA']})")

        return "FALSO - " + "; ".join(discrepancias) if discrepancias else "VERDADERO"

    validacion_df['COINCIDENCIA'] = validacion_df.apply(verificar_discrepancias, axis=1)

    # Renombrar columnas y reordenar
    columnas_ordenadas = [
        "FICHA", "TIPO_PROGRAMA", "NIVEL_FORMACION", "DENOMINACION_PROGRAMA",
        "TIPO_INSTRU", "TIPO_SOFIA", 
        "DOCUMENTO_DE_IDENTIFICACION_INSTRU", "DOCUMENTO_DE_IDENTIFICACION_SOFIA",
        "NOMBRE_COMPLETO_SENA_INSTRU", "NOMBRE_COMPLETO_SENA_SOFIA", "COINCIDENCIA"
    ]
    validacion_df = validacion_df[columnas_ordenadas]

    validacion_df.rename(columns={
        "FICHA": "Ficha",
        "TIPO_PROGRAMA": "Tipo Programa",
        "NIVEL_FORMACION": "Nivel Formación",
        "DENOMINACION_PROGRAMA": "Denominación Programa",
        "TIPO_INSTRU": "Tipo Documento Instructores",
        "TIPO_SOFIA": "Tipo Documento Sofía",
        "DOCUMENTO_DE_IDENTIFICACION_INSTRU": "No. Documento Instructores",
        "DOCUMENTO_DE_IDENTIFICACION_SOFIA": "No. Documento Sofía",
        "NOMBRE_COMPLETO_SENA_INSTRU": "Nombre Aprendiz Instructores",
        "NOMBRE_COMPLETO_SENA_SOFIA": "Nombre Aprendiz Sofía",
        "COINCIDENCIA": "COINCIDENCIA"
    }, inplace=True)

    # Guardar el resultado en un archivo Excel
    output_path = "resultado_validacion.xlsx"
    validacion_df.to_excel(output_path, index=False)
    logger.info(f"Archivo de resultado guardado en: {output_path}")

    return open(output_path, "rb")
