
# backend/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import ClienteCriar, ClienteResposta

router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["Banco de Clientes (tbClientes)"]
)

# Como o prefixo já é /api/v1/clientes, usamos apenas "/" ou "/{id_cliente}"
@router.post("", response_model=ClienteResposta)
def criar_cliente(cliente: ClienteCriar, db: Session = Depends(get_db)):
    cliente_existente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == cliente.id_cliente
    ).first()
    
    if cliente_existente:
        raise HTTPException(
            status_code=400, 
            detail="ID Cliente já cadastrado. IDs são únicos e não reutilizados."
        )
    
    novo_cliente = models.Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get("/{id_cliente}", response_model=ClienteResposta)
def consultar_cliente(id_cliente: str, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == id_cliente
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="ID não encontrado")
    
    return cliente