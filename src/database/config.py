import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Default to Counts Postgres DB
# For Postgres, use: postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://userapp:Li0nt0g3ro!@localhost:5432/Counts")

# Fix for Render/Heroku typically using 'postgres://' which SQLAlchemy doesn't like anymore
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True
)
# Note: check_same_thread=False is needed for SQLite + Multithreading (Flet often runs in threads)
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_basic_data():
    """
    Popula dados básicos essenciais no banco de dados se não existirem.
    - Categorias padrão
    - Classificações padrão
    - Usuário Admin
    
    Esta função é chamada automaticamente no startup da aplicação.
    """
    # Import here to avoid circular dependency
    from database.models import Usuario, Categoria, Classificacao
    
    db = SessionLocal()
    try:
        # Seed Categorias
        if db.query(Categoria).count() == 0:
            print("🌱 Seeding Categorias...")
            cats = [
                Categoria(categoria="Mensalidade", repete=True),
                Categoria(categoria="Cantina", repete=False),
                Categoria(categoria="Dízimo", repete=False),
                Categoria(categoria="Big Loja", repete=False),
                Categoria(categoria="Cota Preparo", repete=False),
                Categoria(categoria="Cotas Diversas", repete=False),
                Categoria(categoria="Doação", repete=False),
                Categoria(categoria="Prosperar", repete=False),
                Categoria(categoria="Novo Encanto", repete=False),
                Categoria(categoria="Outros", repete=False)
            ]
            db.add_all(cats)
            db.commit()
            print("✅ Categorias criadas com sucesso!")
        else:
            print("ℹ️  Categorias já existem no banco.")

        # Seed Classificacao
        if db.query(Classificacao).count() == 0:
            print("🌱 Seeding Classificações...")
            classifications = [
                Classificacao(classificacao="Pendente"),
                Classificacao(classificacao="Vencido"),
                Classificacao(classificacao="Pago"),
                Classificacao(classificacao="Parcial")
            ]
            db.add_all(classifications)
            db.commit()
            print("✅ Classificações criadas com sucesso!")
        else:
            print("ℹ️  Classificações já existem no banco.")

        # Seed Admin User
        if not db.query(Usuario).filter(Usuario.cpf == "00000000000").first():
            print("🌱 Criando usuário Admin...")
            admin = Usuario(
                cpf="00000000000", 
                nome="Administrador", 
                senha="321",  # Em produção, considere usar hash
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário Admin criado! (CPF: 00000000000, Senha: 321)")
        else:
            print("ℹ️  Usuário Admin já existe.")
            
        print("🎉 Seed de dados básicos concluído!")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados básicos: {e}")
        db.rollback()
    finally:
        db.close()
