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
    
    # Optional FK for classification to enforce integrity, or just integer if not strict?
    # User asked for a table 'classificacao', so we should likely link to it.
    # But user didn't explicitly say 'registros' has 'classificacao_id', they said:
    # "classificacoes: id, classificacao. Vamos preencher essa tabela com previsões... para registros"
    # And for 'registros': "id, user_id, type_id, category_id, valor, data_debito, data_entrada, creado_em"
    # Wait, the user prompt for 'registros' schema DOES NOT include 'classificacao_id'.
    # However, it says "previsões de indicadores para registros". This implies a link.
    # Given the strict schema provided: "registros: id, user_id, type_id = 0 ou 1, category_id, valor, data_debito, data_entrada, creado_em"
    # It seems classification might be computed or joined differently, OR I should add it.
    # I will stick STRICTLY to the fields requested for 'registros' first. 
    # BUT, where does 'classificacao' fit? Maybe it's a lookup text? 
    # Or maybe I should add 'classificacao_id' as a foreign key if appropriate?
    # The user listed fields for 'registros' and did NOT list 'classificacao_id'. 
    # I will NOT add 'classificacao_id' to 'registros' to follow instructions precisely, 
    # but I'll create the 'classificacao' table as requested.
    # Perhaps it's for future use or UI dropdowns.
    
    valor = Column(Float, nullable=False)
    data_debito = Column(Date, nullable=True) # "data_debito"
    data_entrada = Column(Date, nullable=True) # "data_entrada" - maybe payment date?
    data_prevista = Column(Date, nullable=True)
    creado_em = Column(DateTime, default=datetime.utcnow)
    #classificacao_id = Column(int, default=3)

    # Relationships
    usuario = relationship("Usuario", back_populates="registros")
    categoria_rel = relationship("Categoria", back_populates="registros")
    
    # Since I'm not adding foreign key for classificacao, no relationship here yet unless I deviate.
    # I'll stick to the requested fields.

    def __repr__(self):
        return f"<Registro(id={self.id}, valor={self.valor}, categoria={self.categoria_rel.categoria}, type_id={self.type_id})>"

        