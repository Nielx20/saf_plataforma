
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class SolicitacaoIMC(BaseModel):
    # Field garante as regras de validação antes mesmo do cálculo acontecer
    peso: float = Field(..., ge=20, le=300, description="Peso do cliente em kg")
    altura: float = Field(..., gt=0, le=3.0, description="Altura do cliente em metros")

class RespostaIMC(BaseModel):
    imc: float

class ClienteCriar(BaseModel):
    id_cliente: str = Field(..., max_length = 6, description = "Formato fixo e único, ex: CL0001")
    nome_completo: str
    nome_exibicao: Optional[str] = None
    pronomes: Optional[str] = None
    identidade_genero: Optional[str] = None
    autodescricao: Optional[str] = None
    sexo_equacao: str = Field(..., description="Variável metodológica: Masculino, Feminino, etc")
    data_nascimento: date
    telefone: Optional[str] = None
    email: Optional[str] = None
    status: str = "Ativo"

class ClienteResposta(ClienteCriar):
    model_config = {"from_attributes": True}
