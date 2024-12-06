import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from ComponentesBackEnd.logger_configuracion import logger

def ajustar_ancho_columnas(archivo):
    wb = openpyxl.load_workbook(archivo)
    hoja = wb.active

    for columna in hoja.columns:
        max_length = 0
        columna_letra = columna[0].column_letter
        for celda in columna:
            try:
                if celda.value:
                    max_length = max(max_length, len(str(celda.value)))
            except Exception as e:
                logger.warning(f"Error ajustando la celda {celda.coordinate}: {e}")

        hoja.column_dimensions[columna_letra].width = max_length + 2

    logger.info("Aplicando formato a los encabezados...")
    encabezado_fila = hoja[1]
    estilo_encabezado = {
        "fill": PatternFill(start_color="C6D8FD", end_color="C6D8FD", fill_type="solid"),
        "font": Font(size=12, bold=True, color="000000"),
        "alignment": Alignment(horizontal="center", vertical="center"),
    }

    for celda in encabezado_fila:
        celda.fill = estilo_encabezado["fill"]
        celda.font = estilo_encabezado["font"]
        celda.alignment = estilo_encabezado["alignment"]

    wb.save(archivo)
    logger.info(f"Ancho de columnas ajustado automáticamente en el archivo: {archivo}")