from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey, Integer
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


class Anamnese(Base):
    __tablename__ = "tbAnamneses"

    id_anamnese = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(String(6), ForeignKey("tbClientes.id_cliente"), nullable=False, index=True)
    
    data_anamnese = Column(Date, nullable=False)
    pratica_atividade_fisica = Column(Boolean, default=False)
    historico_lesoes = Column(Text, nullable=True)
    medicamentos_uso_continuo = Column(Text, nullable=True)
    restricoes_medicas = Column(Text, nullable=True)
    observacoes_gerais = Column(Text, nullable=True)

    cliente = relationship("Cliente", back_populates="anamneses")