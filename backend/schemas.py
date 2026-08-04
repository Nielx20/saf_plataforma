
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

class ClienteAtualizar(BaseModel):
    nome_completo: Optional[str] = None
    nome_exibicao: Optional[str] = None
    pronomes: Optional[str] = None
    identidade_genero: Optional[str] = None
    autodescricao: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class AnamneseCriar(BaseModel):
    id_cliente: str = Field(...,max_length=6, description="ID do cliente (ex: CL0001)")
    data_anamnese: date
    pratica_atividade_fisica: bool = False
    historico_lesoes: Optional[str] = None
    medicamentos_uso_continuo: Optional[str] = None
    restricoes_medicas: Optional[str] = None
    observacoes_gerais: Optional[str] = None

class AnamneseResposta(AnamneseCriar):
    id_anamnese: int

    model_config = {"from_attributes": True}

class AnamneseBase(BaseModel):
    id_cliente: str
    data_anamnese: date
    tipo_anamnese: str = "Inicial"
    id_anamnese_anterior: Optional[str] = None
    respondente: str = "Cliente"
    profissional_responsavel: str
    
    # Núcleo Universal
    instrumento_aplicado: str = "Não"
    nome_instrumento: Optional[str] = None
    objetivo_relatado: str
    expectativa_relatada: Optional[str] = None
    experiencia_previa_af: Optional[str] = None
    atividade_fisica_atual: str = "Não pratica atualmente"
    frequencia_relatada: Optional[str] = None
    duracao_sessao_min: Optional[int] = None
    observacoes_rotina: Optional[str] = None

    # Saúde Relatada
    condicao_saude: str = "Não"
    detalhe_condicoes: Optional[str] = None
    uso_medicamentos: str = "Não"
    detalhe_medicamentos: Optional[str] = None
    lesao_cirurgia: str = "Não"
    detalhe_lesao: Optional[str] = None
    dor_atual: str = "Não"
    local_dor: Optional[str] = None
    intensidade_dor: Optional[int] = Field(default=None, ge=0, le=10)
    restricao_recomendacao: str = "Não"
    detalhe_restricao: Optional[str] = None
    documento_apresentado: str = "Não"

    # Estilo de Vida
    tabagismo: str = "Nunca fumou"
    consumo_alcool: str = "Não consome"
    horas_sono_noite: Optional[float] = Field(default=None, ge=0.5, le=24.0)
    qualidade_sono: Optional[str] = None
    estresse_percebido: Optional[int] = Field(default=None, ge=0, le=10)

    # Módulos Condicionais
    modulo_crianca_adolescente: str = "Não"
    detalhe_crianca_adolescente: Optional[str] = None
    modulo_autonomia_funcional: str = "Não"
    detalhe_autonomia: Optional[str] = None
    modulo_gestacao: str = "Não"
    detalhe_gestacao: Optional[str] = None
    modulo_acessibilidade: str = "Não"
    detalhe_acessibilidade: Optional[str] = None
    modulo_performance: str = "Não"
    detalhe_performance: Optional[str] = None
    modulo_retorno_afastamento: str = "Não"
    detalhe_retorno: Optional[str] = None

    # Decisão Profissional
    encaminhamento: str = "Não identificado no momento"
    motivo_encaminhamento: Optional[str] = None
    conduta_inicial: str = "Prosseguir"
    detalhe_conduta: Optional[str] = None
    adaptacoes_previstas: Optional[str] = None
    status_anamnese: str = "Incompleta"
    data_arquivamento: Optional[date] = None
    auditoria_realizada: str = "Não"
    observacoes_auditoria: Optional[str] = None


class AnamneseCriar(AnamneseBase):
    id_anamnese: str = Field(..., pattern=r"^AN\d{4}$", description="ID único no formato AN0001")


class AnamneseAtualizar(BaseModel):
    tipo_anamnese: Optional[str] = None
    respondente: Optional[str] = None
    profissional_responsavel: Optional[str] = None
    objetivo_relatado: Optional[str] = None
    expectativa_relatada: Optional[str] = None
    atividade_fisica_atual: Optional[str] = None
    frequencia_relatada: Optional[str] = None
    duracao_sessao_min: Optional[int] = None
    condicao_saude: Optional[str] = None
    detalhe_condicoes: Optional[str] = None
    uso_medicamentos: Optional[str] = None
    detalhe_medicamentos: Optional[str] = None
    lesao_cirurgia: Optional[str] = None
    detalhe_lesao: Optional[str] = None
    dor_atual: Optional[str] = None
    local_dor: Optional[str] = None
    intensidade_dor: Optional[int] = Field(default=None, ge=0, le=10)
    tabagismo: Optional[str] = None
    consumo_alcool: Optional[str] = None
    horas_sono_noite: Optional[float] = Field(default=None, ge=0.5, le=24.0)
    qualidade_sono: Optional[str] = None
    estresse_percebido: Optional[int] = Field(default=None, ge=0, le=10)
    encaminhamento: Optional[str] = None
    motivo_encaminhamento: Optional[str] = None
    conduta_inicial: Optional[str] = None
    detalhe_conduta: Optional[str] = None
    adaptacoes_previstas: Optional[str] = None
    status_anamnese: Optional[str] = None
    auditoria_realizada: Optional[str] = None
    observacoes_auditoria: Optional[str] = None


class AnamneseResposta(AnamneseBase):
    id_anamnese: str

    class Config:
        from_attributes = True