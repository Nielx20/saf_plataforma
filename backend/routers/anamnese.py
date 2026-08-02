

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
from schemas import AnamneseCriar, AnamneseResposta

router = APIRouter(
    prefix="/api/v1/anamneses",
    tags=["Banco de Anamneses (tbAnamneses)"]
)

@router.post("", response_model=AnamneseResposta)
def criar_anamnese(anamnese: AnamneseCriar, db: Session = Depends(get_db)):
    # 1. Verifica se o cliente existe antes de criar a anamnese
    cliente_existente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == anamnese.id_cliente
    ).first()

    if not cliente_existente:
        raise HTTPException(
            status_code=404, 
            detail=f"Cliente com ID '{anamnese.id_cliente}' não encontrado. Impossível vincular anamnese."
        )

    # 2. Salva a nova anamnese no banco
    nova_anamnese = models.Anamnese(**anamnese.model_dump())
    db.add(nova_anamnese)
    db.commit()
    db.refresh(nova_anamnese)
    return nova_anamnese


@router.get("/cliente/{id_cliente}", response_model=List[AnamneseResposta])
def listar_anamneses_por_cliente(id_cliente: str, db: Session = Depends(get_db)):
    # Retorna o histórico de anamneses daquele cliente
    anamneses = db.query(models.Anamnese).filter(
        models.Anamnese.id_cliente == id_cliente
    ).all()
    return anamneses