from sqlalchemy import Column, String, Date
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
    