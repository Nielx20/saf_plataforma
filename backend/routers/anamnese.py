# backend/routers/anamnese.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import AnamneseCriar, AnamneseAtualizar, AnamneseResposta

router = APIRouter(prefix="/api/v1/anamneses", tags=["Banco de Anamneses (tbAnamneses)"])

@router.post("", response_model=AnamneseResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_anamnese(dados: AnamneseCriar, db: Session = Depends(get_db)):
    # 1. Verifica se o cliente vinculado realmente existe em tbClientes
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == dados.id_cliente).first()
    if not cliente:
        raise HTTPException(
            status_code=400, 
            detail=f"Cliente {dados.id_cliente} não encontrado. Cadastre o cliente antes de criar uma anamnese."
        )

    # 2. Verifica se o ID de Anamnese já está em uso (ex: AN0001)
    anamnese_existente = db.query(models.Anamnese).filter(
        models.Anamnese.id_anamnese == dados.id_anamnese
    ).first()
    if anamnese_existente:
        raise HTTPException(
            status_code=400, 
            detail="ID Anamnese já cadastrado. IDs são únicos e não reutilizados."
        )

    # 3. Cria e salva a nova Anamnese
    nova_anamnese = models.Anamnese(**dados.model_dump())
    db.add(nova_anamnese)
    db.commit()
    db.refresh(nova_anamnese)
    return nova_anamnese


@router.get("", response_model=List[AnamneseResposta])
def listar_anamneses(id_cliente: str = None, db: Session = Depends(get_db)):
    """Lista todas as anamneses ou filtra pelo histórico de um ID Cliente."""
    query = db.query(models.Anamnese)
    if id_cliente:
        query = query.filter(models.Anamnese.id_cliente == id_cliente)
    return query.order_by(models.Anamnese.data_anamnese.desc()).all()


@router.get("/{id_anamnese}", response_model=AnamneseResposta)
def consultar_anamnese(id_anamnese: str, db: Session = Depends(get_db)):
    anamnese = db.query(models.Anamnese).filter(
        models.Anamnese.id_anamnese == id_anamnese
    ).first()
    if not anamnese:
        raise HTTPException(status_code=404, detail="ID Anamnese não encontrado.")
    return anamnese


@router.put("/{id_anamnese}", response_model=AnamneseResposta)
def atualizar_anamnese(id_anamnese: str, dados_atualizacao: AnamneseAtualizar, db: Session = Depends(get_db)):
    anamnese = db.query(models.Anamnese).filter(
        models.Anamnese.id_anamnese == id_anamnese
    ).first()
    if not anamnese:
        raise HTTPException(status_code=404, detail="ID Anamnese não encontrado para atualização.")

    dados_dict = dados_atualizacao.model_dump(exclude_unset=True, exclude_none=True)
    for campo, valor in dados_dict.items():
        setattr(anamnese, campo, valor)

    db.commit()
    db.refresh(anamnese)
    return anamnese


@router.delete("/{id_anamnese}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_anamnese(id_anamnese: str, db: Session = Depends(get_db)):
    anamnese = db.query(models.Anamnese).filter(
        models.Anamnese.id_anamnese == id_anamnese
    ).first()
    if not anamnese:
        raise HTTPException(status_code=404, detail="ID Anamnese não encontrado para remoção.")

    db.delete(anamnese)
    db.commit()
    return None