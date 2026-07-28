# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import SolicitacaoIMC, RespostaIMC, ClienteCriar, ClienteResposta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SAF - Motor Matemático e Banco de Dados")

# O motor matemático isolado
def calcular_imc(peso: float, altura: float) -> float:
    return round(peso / (altura ** 2), 2)

@app.post("/api/v1/calculos/imc", response_model=RespostaIMC)
def endpoint_calcular_imc(dados: SolicitacaoIMC):
    resultado = calcular_imc(peso=dados.peso, altura=dados.altura)
    return RespostaIMC(imc=resultado)


@app.post("/api/v1/clientes", response_model=ClienteResposta)
def criar_cliente(cliente: ClienteCriar, db: Session = Depends(get_db)):
    # 1. Regra de unicidade: Verifica se o ID Cliente já existe no banco
    cliente_existente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente.id_cliente).first()
    
    if cliente_existente:
        # Se existir, bloqueamos a inserção e avisamos o erro (como a validação bloqueando duplicidade)
        raise HTTPException(status_code=400, detail="ID Cliente já cadastrado. IDs são únicos e não reutilizados.")
    
    # 2. Prepara os dados para salvar
    novo_cliente = models.Cliente(**cliente.model_dump())
    
    # 3. Executa a inserção no banco de dados (fonte única de verdade)
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    
    return novo_cliente

@app.get("/api/v1/clientes/{id_cliente}", response_model=ClienteResposta)
def consultar_cliente(id_cliente: str, db: Session = Depends(get_db)):
    # Fazemos a busca no banco filtrando pelo ID passado na URL
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    
    # Se o banco não achar ninguém, retornamos o status que o manual previu: "ID não encontrado"
    if not cliente:
        raise HTTPException(status_code=404, detail="ID não encontrado")
    
    # Retorna os dados do cliente se ele for encontrado
    return cliente