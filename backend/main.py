from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import calculos, clientes, anamnese, auditoria  # <- adicionamos auditoria

# Garante a criação das tabelas no PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SAF - Sistema de Avaliação Física",
    description="Motor de cálculos, regras de negócio e persistência de dados"
)

# Libera o frontend (Vite, rodando em outra porta) a chamar essa API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculos.router)
app.include_router(clientes.router)
app.include_router(anamnese.router)
app.include_router(auditoria.router)  # <- rotas de consulta e checagem de integridade