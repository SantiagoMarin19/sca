from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from procesamiento import procesar_archivo_instructores
import traceback
import os
from io import BytesIO

router = APIRouter()

@router.post("/process-files/")
async def process_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    Endpoint para procesar dos archivos Excel y devolver un archivo de resultado.
    """
    try:
        # Ruta de la plantilla
        plantilla_path = "./plantilla.xlsx"
        if not os.path.exists(plantilla_path):
            raise HTTPException(status_code=500, detail="La plantilla no fue encontrada en el servidor.")
        
        # Procesar los archivos
        resultado = procesar_archivo_instructores(file1.file, file2.file)

        # Comprobar si se generó correctamente el archivo
        if resultado is None:
            raise HTTPException(status_code=500, detail="Error en el procesamiento de los archivos.")
        
        # Devolver el archivo como respuesta
        headers = {
            "Content-Disposition": "attachment; filename=PlantillaResultado.xlsx"
        }
        return StreamingResponse(resultado, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error al procesar archivos: {str(e)}. Trace: {error_trace}")
