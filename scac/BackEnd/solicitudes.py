from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from procesamiento import procesar_archivos
import traceback
import os


router = APIRouter()

@router.post("/process-files/")
async def process_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    Endpoint para procesar dos archivos Excel y devolver un archivo de resultado.
    """
    try:
        plantilla_path = "./plantilla.xlsx"
        if not os.path.exists(plantilla_path):
           raise HTTPException(status_code=500, detail="La plantilla no fue encontrada en el servidor.")
        resultado = procesar_archivos(file1.file, file2.file, plantilla_path)

        if resultado is None:
            raise HTTPException(status_code=500, detail="Error en el procesamiento de los archivos.")

        headers = {
            "Content-Disposition": "attachment; filename=PlantillaResultado.xlsx"
        }

        return StreamingResponse(resultado, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    except Exception as e:
        error_trace = traceback.format_exc()
        return {"error": f"{str(e)}", "trace": error_trace}
