from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    creado_em = Column(DateTime, default=datetime.utcnow)

    # Relationships
    registros = relationship("Registro", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(cpf={self.cpf}, nome={self.nome})>"

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(50), nullable=False, unique=True)
    repete = Column(Boolean, default=False)

    # Relationships
    registros = relationship("Registro", back_populates="categoria_rel")

    def __repr__(self):
        return f"<Categoria(nome={self.categoria})>"

class Classificacao(Base):
    __tablename__ = "classificacoes"

    id = Column(Integer, primary_key=True, index=True)
    classificacao = Column(String(50), nullable=False, unique=True)

    # Relationships - Optional, knowing which records have this classification?
    # For now, we might not need a direct back-ref unless requested, but good practice.
    # registros = relationship("Registro", back_populates="classificacao_rel")

    def __repr__(self):
        return f"<Classificacao(nome={self.classificacao})>"

class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    type_id = Column(Integer, nullable=False) # 0 or 1
    category_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    
    valor = Column(Float, nullable=False)
    data_debito = Column(Date, nullable=True) # "data_debito"
    data_entrada = Column(Date, nullable=True) # "data_entrada" - maybe payment date?
    data_prevista = Column(Date, nullable=True)
    creado_em = Column(DateTime, default=datetime.utcnow)
    
    # New Columns for Debt Abatement
    # Default classificacao_id=1 (Pendente)
    classificacao_id = Column(Integer, ForeignKey("classificacoes.id"), default=1)
    saldo = Column(Float, default=0.0)

    # Relationships
    usuario = relationship("Usuario", back_populates="registros")
    categoria_rel = relationship("Categoria", back_populates="registros")
    # classification relationship
    classificacao_rel = relationship("Classificacao")

    def __repr__(self):
        return f"<Registro(id={self.id}, valor={self.valor}, categoria={self.categoria_rel.categoria}, type_id={self.type_id}, classificacao={self.classificacao_rel.classificacao})>"

        