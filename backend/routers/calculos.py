from fastapi import APIRouter
from schemas import SolicitacaoIMC, RespostaIMC
from services import calcular_imc

router = APIRouter(
    prefix="/api/v1/calculos",
    tags=["Cálculos e Motores Matemáticos"]
)

@router.post("/imc", response_model=RespostaIMC)
def endpoint_calcular_imc(dados: SolicitacaoIMC):
    resultado = calcular_imc(peso=dados.peso, altura=dados.altura)
    return RespostaIMC(imc=resultado)
