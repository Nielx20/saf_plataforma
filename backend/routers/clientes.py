from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import ClienteCriar, ClienteResposta, ClienteAtualizar

router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["Banco de Clientes (tbClientes)"]
)

@router.get("", response_model=list[ClienteResposta])
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

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


@router.put("/{id_cliente}", response_model=ClienteResposta)
def atualizar_cliente(id_cliente: str, dados_atualizacao: ClienteAtualizar, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.id_cliente == id_cliente
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="ID Cliente não encontrado para atualização")

    dados_dict = dados_atualizacao.model_dump(exclude_unset=True, exclude_none=True)


# -> RAIO-X PARA DEBUG NO TERMINAL:
    print(f"\n[DEBUG PUT] ID: {id_cliente} | Dados recebidos para trocar: {dados_dict}\n")

    for campo,valor in dados_dict.items():
        print(f" -> Atualizando '{campo}': de '{getattr(cliente, campo)}' para '{valor}'")
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{id_cliente}", status_code=204)
def deletar_cliente(id_cliente: str, db:session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
            models.Cliente.id_cliente == id_cliente
        ).first()

    if not cliente: 
        raise HTTPException(status_code=404, detail="ID Cliente não encontrado para remoção")

    db.delete(cliente)
    db.commit()
    return None