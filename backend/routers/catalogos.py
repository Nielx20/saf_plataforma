# routers/catalogos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/api/v1/catalogos",
    tags=["Catálogos e Domínios de Avaliação"]
)

# --- DOMÍNIOS ---
@router.post("/dominios", response_model=schemas.DominioAvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_dominio(payload: schemas.DominioAvaliacaoCreate, db: Session = Depends(get_db)):
    if db.query(models.DominioAvaliacao).filter(models.DominioAvaliacao.id_dominio == payload.id_dominio).first():
        raise HTTPException(status_code=400, detail="ID de Domínio já cadastrado.")
    novo = models.DominioAvaliacao(**payload.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/dominios", response_model=List[schemas.DominioAvaliacaoResponse])
def listar_dominios(db: Session = Depends(get_db)):
    return db.query(models.DominioAvaliacao).all()

# --- PROTOCOLOS ---
@router.post("/protocolos", response_model=schemas.ProtocoloResponse, status_code=status.HTTP_201_CREATED)
def criar_protocolo(payload: schemas.ProtocoloCreate, db: Session = Depends(get_db)):
    if not db.query(models.DominioAvaliacao).filter(models.DominioAvaliacao.id_dominio == payload.id_dominio).first():
        raise HTTPException(status_code=400, detail=f"Domínio '{payload.id_dominio}' não existe no banco.")
    if db.query(models.Protocolo).filter(models.Protocolo.id_protocolo == payload.id_protocolo).first():
        raise HTTPException(status_code=400, detail="ID de Protocolo já cadastrado.")
    novo = models.Protocolo(**payload.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/protocolos", response_model=List[schemas.ProtocoloResponse])
def listar_protocolos(db: Session = Depends(get_db)):
    return db.query(models.Protocolo).all()

# --- CATÁLOGO DE MEDIDAS ---
@router.post("/variaveis", response_model=schemas.CatalogoMedidaResponse, status_code=status.HTTP_201_CREATED)
def criar_variavel_catalogo(payload: schemas.CatalogoMedidaCreate, db: Session = Depends(get_db)):
    if payload.id_protocolo and not db.query(models.Protocolo).filter(models.Protocolo.id_protocolo == payload.id_protocolo).first():
        raise HTTPException(status_code=400, detail=f"Protocolo '{payload.id_protocolo}' não encontrado.")
    if db.query(models.CatalogoMedida).filter(models.CatalogoMedida.id_variavel == payload.id_variavel).first():
        raise HTTPException(status_code=400, detail="ID de Variável já cadastrado no catálogo.")
    novo = models.CatalogoMedida(**payload.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/variaveis", response_model=List[schemas.CatalogoMedidaResponse])
def listar_variaveis_catalogo(db: Session = Depends(get_db)):
    return db.query(models.CatalogoMedida).all()