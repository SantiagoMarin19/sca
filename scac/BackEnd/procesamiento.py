import pandas as pd
from ComponentesBackEnd.logger_configuracion import logger
from ComponentesBackEnd.excel_utils import ajustar_ancho_columnas
from ComponentesBackEnd.data_procesamiento import procesar_archivo_instructores, realizar_validacion

def procesar_archivos(file_instru, file_sofia):
    try:
        instru_df, sofia_filtrado = procesar_archivo_instructores(file_instru, file_sofia)
        validacion_df = realizar_validacion(instru_df, sofia_filtrado)

        # Renombrar columnas y reordenar
        logger.info("Renombrando columnas y reordenando...")
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
            "NOMBRE_COMPLETO_SENA_INSTRU": "Nombre Aprendiz Instructores Consulta",
            "NOMBRE_COMPLETO_SENA_SOFIA": "Nombre Aprendiz Sofía",
            "COINCIDENCIA": "COINCIDENCIA"
        }, inplace=True)

        output_path = "resultado_validacion.xlsx"
        validacion_df.to_excel(output_path, index=False)
        ajustar_ancho_columnas(output_path)
        logger.info(f"Archivo de resultado guardado en: {output_path}")

        return open(output_path, "rb")
    except Exception as e:
        logger.error(f"Error en el procesamiento: {str(e)}")
        raise