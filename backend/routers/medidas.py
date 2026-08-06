# routers/medidas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from services.calculadora_fisica import processar_calculos_automaticos

router = APIRouter(
    prefix="/api/v1/medidas-protocolos",
    tags=["Medidas e Protocolos Aplicados"]
)

# =====================================================================
# ROTAS: PROTOCOLOS APLICADOS
# =====================================================================
@router.post("/protocolos", response_model=schemas.ProtocoloAplicadoResponse, status_code=status.HTTP_201_CREATED)
def criar_protocolo_aplicado(payload: schemas.ProtocoloAplicadoCreate, db: Session = Depends(get_db)):
    # 1. Verifica se a Avaliação titular existe
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == payload.id_avaliacao).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Avaliação '{payload.id_avaliacao}' não encontrada no sistema."
        )

    # 2. Verifica unicidade do ID do protocolo aplicado
    existente = db.query(models.ProtocoloAplicado).filter(
        models.ProtocoloAplicado.id_protocolo_aplicado == payload.id_protocolo_aplicado
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do Protocolo Aplicado já existe no banco de dados."
        )

    novo_protocolo = models.ProtocoloAplicado(**payload.model_dump())
    db.add(novo_protocolo)
    db.commit()
    db.refresh(novo_protocolo)
    return novo_protocolo

@router.get("/protocolos/avaliacao/{id_avaliacao}", response_model=List[schemas.ProtocoloAplicadoResponse])
def listar_protocolos_da_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    return db.query(models.ProtocoloAplicado).filter(models.ProtocoloAplicado.id_avaliacao == id_avaliacao).all()


# =====================================================================
# ROTAS: MEDIDAS - FORMATO LONGO
# =====================================================================
@router.post("/medidas", response_model=schemas.MedidaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_medida(payload: schemas.MedidaCreate, db: Session = Depends(get_db)):
    # 1. Verifica se a Avaliação titular existe
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == payload.id_avaliacao).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Avaliação '{payload.id_avaliacao}' não encontrada no sistema."
        )

    # 2. Verifica unicidade do ID da medida
    existente = db.query(models.Medida).filter(models.Medida.id_medida == payload.id_medida).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da Medida já cadastrado."
        )

    nova_medida = models.Medida(**payload.model_dump())
    db.add(nova_medida)
    db.commit()
    db.refresh(nova_medida)

    processar_calculos_automaticos(db=db, id_avaliacao=payload.id_avaliacao)

    return nova_medida

@router.get("/medidas/avaliacao/{id_avaliacao}", response_model=List[schemas.MedidaResponse])
def listar_medidas_da_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    """Retorna todas as variáveis (peso, altura, IMC, dobras...) de uma avaliação física."""
    return db.query(models.Medida).filter(models.Medida.id_avaliacao == id_avaliacao).all()

@router.put("/medidas/{id_medida}", response_model=schemas.MedidaResponse)
def atualizar_medida(id_medida: str, payload: schemas.MedidaUpdate, db: Session = Depends(get_db)):
    medida = db.query(models.Medida).filter(models.Medida.id_medida == id_medida).first()
    if not medida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medida '{id_medida}' não encontrada.")

    dados_atualizar = payload.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizar.items():
        setattr(medida, chave, valor)

    db.commit()
    db.refresh(medida)

    processar_calculos_automaticos(db=db, id_avaliacao=medida.id_avaliacao)
    
    return medida

@router.delete("/medidas/{id_medida}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medida(id_medida: str, db: Session = Depends(get_db)):
    medida = db.query(models.Medida).filter(models.Medida.id_medida == id_medida).first()
    if not medida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medida '{id_medida}' não encontrada.")
    db.delete(medida)
    db.commit()
    return None

