from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from solicitudes import router as solicitudes_router

# Crear una instancia de FastAPI
app = FastAPI()

# Configurar middleware CORS para permitir las solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto si tu frontend está en otra URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar el router de solicitudes
app.include_router(solicitudes_router, prefix="/api")

# Ruta de prueba para verificar que el servidor está funcionando
@app.get("/")
async def root():
    return {"message": "Backend funcionando correctamente"}

    # codigo para correr el backend uvicorn main:app --reload
    

