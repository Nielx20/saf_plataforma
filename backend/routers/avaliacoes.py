
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/api/v1/avaliacoes",
    tags=["Avaliações Físicas"]
)

@router.post("/", response_model=schemas.AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_avaliacao(payload: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o ID de avaliação já existe (Unicidade)
    existente = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == payload.id_avaliacao).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID Avaliação já cadastrado. IDs são únicos e não reutilizados."
        )

    # 2. Verifica se o Cliente existe no banco
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == payload.id_cliente).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente com ID '{payload.id_cliente}' não encontrado."
        )

    # 3. Verifica se a Anamnese existe no banco
    anamnese = db.query(models.Anamnese).filter(models.Anamnese.id_anamnese == payload.id_anamnese).first()
    if not anamnese:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anamnese com ID '{payload.id_anamnese}' não encontrada."
        )

    # 4. Verifica se a Anamnese informada realmente pertence àquele Cliente
    if anamnese.id_cliente != payload.id_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A anamnese '{payload.id_anamnese}' pertence a outro cliente e não pode ser vinculada ao cliente '{payload.id_cliente}'."
        )

    # Cria e salva o registro no banco
    nova_avaliacao = models.Avaliacao(**payload.model_dump())
    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)
    return nova_avaliacao


@router.get("/", response_model=List[schemas.AvaliacaoResponse])
def listar_avaliacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Avaliacao).offset(skip).limit(limit).all()


@router.get("/{id_avaliacao}", response_model=schemas.AvaliacaoResponse)
def obter_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == id_avaliacao).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Avaliação '{id_avaliacao}' não encontrada."
        )
    return avaliacao


@router.put("/{id_avaliacao}", response_model=schemas.AvaliacaoResponse)
def atualizar_avaliacao(id_avaliacao: str, payload: schemas.AvaliacaoUpdate, db: Session = Depends(get_db)):
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == id_avaliacao).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Avaliação '{id_avaliacao}' não encontrada."
        )

    # Atualiza apenas os campos passados pelo usuário (não nulos)
    dados_atualizar = payload.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizar.items():
        setattr(avaliacao, chave, valor)

    db.commit()
    db.refresh(avaliacao)
    return avaliacao


@router.delete("/{id_avaliacao}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id_avaliacao == id_avaliacao).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Avaliação '{id_avaliacao}' não encontrada."
        )

    db.delete(avaliacao)
    db.commit()
    return None