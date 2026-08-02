from fastapi import FastAPI
import models
from database import engine
from routers import calculos, clientes, anamnese  # <- importamos anamnese

# Garante a criação das tabelas no PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SAF - Sistema de Avaliação Física",
    description="Motor de cálculos, regras de negócio e persistência de dados"
)

app.include_router(calculos.router)
app.include_router(clientes.router)
app.include_router(anamnese.router)  