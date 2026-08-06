from fastapi import FastAPI
from contextlib import asynccontextmanager
import models
from database import engine, Base, SessionLocal
from seed import popular_banco_saf
from routers import clientes, anamnese, avaliacoes, medidas, catalogos

# Garante a criação das tabelas no PostgreSQL
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa ao LIGAR o servidor:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        popular_banco_saf(db)
    finally:
        db.close()
    yield
    # (Se precisar fechar conexões ao DESLIGAR o servidor, viria aqui depois do yield)

app = FastAPI(
    title="SAF - Sistema de Avaliação Física",
    description="Motor de cálculos, regras de negócio e persistência de dados",
    lifespan=lifespan
)

app.include_router(clientes.router)
app.include_router(anamnese.router)  
app.include_router(avaliacoes.router)
app.include_router(medidas.router)
app.include_router(catalogos.router)
