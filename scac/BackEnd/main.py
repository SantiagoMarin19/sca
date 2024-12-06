from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

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

# Registrar el router de la API
app.include_router(api_router, prefix="/api")

# Ruta de prueba para verificar que el servidor está funcionando
@app.get("/")
async def root():
    return {"message": "Backend funcionando correctamente"}

# El código para correr el backend sigue siendo: uvicorn main:app --reload