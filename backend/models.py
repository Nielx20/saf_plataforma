from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "tbClientes"

    id_cliente = Column(String(6), primary_key=True, index=True) 
    nome_completo = Column(String, nullable=False)
    nome_exibicao = Column(String)
    pronomes = Column(String)
    identidade_genero = Column(String) 
    autodescricao = Column(String)
    sexo_equacao = Column(String, nullable=False) 
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(String, default="Ativo")
    # Relacionamento: 1 Clientes pode ter N anamneses
    anamneses = relationship("Anamnese", back_populates="cliente", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")

class Anamnese(Base):
    __tablename__ = "tbAnamneses"

    # ==========================================
    # IDENTIFICAÇÃO E VERSIONAMENTO (A:G)
    # ==========================================
    id_anamnese = Column(String, primary_key=True, index=True)  # AN0001
    id_cliente = Column(String, ForeignKey("tbClientes.id_cliente"), nullable=False, index=True)
    data_anamnese = Column(Date, nullable=False)
    tipo_anamnese = Column(String, nullable=False)  # Inicial, Atualização periódica, etc.
    id_anamnese_anterior = Column(String, nullable=True)
    respondente = Column(String, nullable=False)  # Cliente, Responsável legal, etc.
    profissional_responsavel = Column(String, nullable=False)

    # ==========================================
    # INSTRUMENTO E NÚCLEO UNIVERSAL
    # ==========================================
    instrumento_aplicado = Column(String, default="Não")  # Sim / Não
    nome_instrumento = Column(String, nullable=True)
    objetivo_relatado = Column(String, nullable=False)
    expectativa_relatada = Column(String, nullable=True)
    experiencia_previa_af = Column(String, nullable=True)
    atividade_fisica_atual = Column(String, nullable=False)
    frequencia_relatada = Column(String, nullable=True)
    duracao_sessao_min = Column(Integer, nullable=True)
    observacoes_rotina = Column(Text, nullable=True)

    # ==========================================
    # SAÚDE RELATADA E DOCUMENTOS
    # ==========================================
    condicao_saude = Column(String, default="Não")  # Sim, Não, Não sabe...
    detalhe_condicoes = Column(Text, nullable=True)
    uso_medicamentos = Column(String, default="Não")
    detalhe_medicamentos = Column(Text, nullable=True)
    lesao_cirurgia = Column(String, default="Não")
    detalhe_lesao = Column(Text, nullable=True)
    dor_atual = Column(String, default="Não")
    local_dor = Column(String, nullable=True)
    intensidade_dor = Column(Integer, nullable=True)  # 0 a 10
    restricao_recomendacao = Column(String, default="Não")
    detalhe_restricao = Column(Text, nullable=True)
    documento_apresentado = Column(String, default="Não")

    # ==========================================
    # ESTILO DE VIDA E PERCEPÇÕES
    # ==========================================
    tabagismo = Column(String, default="Nunca fumou")
    consumo_alcool = Column(String, default="Não consome")
    horas_sono_noite = Column(Float, nullable=True)
    qualidade_sono = Column(String, nullable=True)
    estresse_percebido = Column(Integer, nullable=True)  # 0 a 10

    # ==========================================
    # MÓDULOS CONDICIONAIS (Sim/Não Operacional)
    # ==========================================
    modulo_crianca_adolescente = Column(String, default="Não")
    detalhe_crianca_adolescente = Column(Text, nullable=True)
    modulo_autonomia_funcional = Column(String, default="Não")
    detalhe_autonomia = Column(Text, nullable=True)
    modulo_gestacao = Column(String, default="Não")
    detalhe_gestacao = Column(Text, nullable=True)
    modulo_acessibilidade = Column(String, default="Não")
    detalhe_acessibilidade = Column(Text, nullable=True)
    modulo_performance = Column(String, default="Não")
    detalhe_performance = Column(Text, nullable=True)
    modulo_retorno_afastamento = Column(String, default="Não")
    detalhe_retorno = Column(Text, nullable=True)

    # ==========================================
    # DECISÃO PROFISSIONAL E AUDITORIA
    # ==========================================
    encaminhamento = Column(String, default="Não identificado")
    motivo_encaminhamento = Column(Text, nullable=True)
    conduta_inicial = Column(String, default="Prosseguir")
    detalhe_conduta = Column(Text, nullable=True)
    adaptacoes_previstas = Column(Text, nullable=True)
    status_anamnese = Column(String, default="Incompleta")  # Completa, Incompleta, Revisão necessária
    data_arquivamento = Column(Date, nullable=True)
    auditoria_realizada = Column(String, default="Não")
    observacoes_auditoria = Column(Text, nullable=True)

    # Relacionamento de volta com a tabela de Clientes
    cliente = relationship("Cliente", back_populates="anamneses")
    avaliacoes = relationship("Avaliacao", back_populates="anamnese")


class Avaliacao(Base):
    """
    Cabeçalho de uma sessão de Avaliação Física (tbAvaliacoes).
    Vincula um cliente e sua anamnese vigente aos protocolos e medidas coletadas.
    """
    __tablename__ = "tbAvaliacoes"

    # Chaves e Identificadores
    id_avaliacao = Column(String(10), primary_key=True, index=True)  # Ex: "AV0001"
    id_cliente = Column(String(10), ForeignKey("tbClientes.id_cliente", ondelete="CASCADE"), nullable=False)
    id_anamnese = Column(String(10), ForeignKey("tbAnamneses.id_anamnese"), nullable=False)

    # Metadados da Sessão
    data_avaliacao = Column(Date, nullable=False)
    profissional_responsavel = Column(String(100), nullable=False)
    status_avaliacao = Column(String(30), default="Em Andamento")  # Ex: "Em Andamento", "Concluida", "Revisada"
    observacoes_gerais = Column(Text, nullable=True)

    # Navegação do SQLAlchemy ORM
    cliente = relationship("Cliente", back_populates="avaliacoes")
    anamnese = relationship("Anamnese", back_populates="avaliacoes")

    # Futuros relacionamentos com protocolos aplicados e medidas longas:
    # protocolos_aplicados = relationship("ProtocoloAplicado", back_populates="avaliacao", cascade="all, delete-orphan")
    # medidas = relationship("Medida", back_populates="avaliacao", cascade="all, delete-orphan")