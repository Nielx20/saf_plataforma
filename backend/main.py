from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes, anamnese, calculos

app = FastAPI(
    title="SAF Plataforma API",
    description="API para gestão de anamneses e clientes",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers - SEM prefixo adicional aqui
# Os routers já têm o prefixo /api/v1 internamente
app.include_router(clientes.router)
app.include_router(anamnese.router)
app.include_router(calculos.router)

@app.get("/")
def read_root():
    return {"message": "API SAF Plataforma"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)