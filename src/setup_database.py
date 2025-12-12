from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.config import DATABASE_URL, Base
from database.models import Usuario, Categoria, Classificacao, Registro
import os

# Admin credentials for initial setup
ADMIN_DB_URL = "postgresql://postgres:Li0nt0g3ro!@localhost:5432/postgres"
TARGET_DB_NAME = "Counts"
APP_USER = "userapp"
APP_PASS = "Li0nt0g3ro!"

def create_database_and_user():
    print(f"Connecting to {ADMIN_DB_URL} to setup DB and User...")
    engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        # Check if user exists
        result = conn.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname='{APP_USER}'"))
        if not result.scalar():
            print(f"Creating user {APP_USER}...")
            conn.execute(text(f"CREATE USER {APP_USER} WITH PASSWORD '{APP_PASS}'"))
            # Grant privilege to create database if validation needed? No, just grant on target DB later.
            # But usually userapp doesn't need to be superuser.
        else:
            print(f"User {APP_USER} already exists.")

        # Check if DB exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{TARGET_DB_NAME}'"))
        if not result.scalar():
            print(f"Creating database {TARGET_DB_NAME}...")
            conn.execute(text(f"CREATE DATABASE \"{TARGET_DB_NAME}\" OWNER {APP_USER}"))
        else:
            print(f"Database {TARGET_DB_NAME} already exists.")

        # Grant privileges
        print(f"Granting privileges on database {TARGET_DB_NAME} to {APP_USER}...")
        conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE \"{TARGET_DB_NAME}\" TO {APP_USER}"))
        # Also grant schema usage usually needed for public schema in PG 15+
        # But we need to connect to the DB to grant schema privileges usually.
    
    engine.dispose()

def create_tables_and_seed():
    # Connect using the app user and the specific database
    # Note: config.py should already have the correct URL now, but we'll be explicit to be safe or use what's in config
    print("Connecting to Counts database to create tables and seed data...")
    
    # We use the engine from config which points to the new DB
    from database.config import engine as app_engine, SessionLocal
    
    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(bind=app_engine)
    
    db = SessionLocal()
    try:
        # Seed Categorias
        if db.query(Categoria).count() == 0:
            print("Seeding Categorias...")
            cats = [
                Categoria(categoria="Mensalidade", repete=True),
                Categoria(categoria="Cantina", repete=False),
                Categoria(categoria="Dízimo", repete=False),
                Categoria(categoria="Big Loja", repete=False),
                Categoria(categoria="Cota Preparo", repete=False),
                Categoria(categoria="Cotas", repete=False),
                Categoria(categoria="Outros", repete=False)
            ]
            db.add_all(cats)
            db.commit()
        else:
            print("Categorias already exist.")

        # Seed Classificacao
        if db.query(Classificacao).count() == 0:
            print("Seeding Classificacao...")
            classifications = [
                Classificacao(classificacao="Vencido"),
                Classificacao(classificacao="Pago"),
                Classificacao(classificacao="Pendente"),
                Classificacao(classificacao="Parcial")
            ]
            db.add_all(classifications)
            db.commit()
        else:
            print("Classificacao already exists.")

        # Seed Admin User
        if not db.query(Usuario).filter(Usuario.cpf == "00000000000").first():
            print("Seeding Admin User...")
            admin = Usuario(
                cpf="00000000000", 
                nome="Administrador", 
                senha="321", # In production, hash this!
                is_admin=True
            )
            db.add(admin)
            db.commit()
        else:
            print("Admin user already exists.")
            
        print("Setup completed successfully!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    try:
        create_database_and_user()
        create_tables_and_seed()
    except Exception as e:
        print(f"An error occurred: {e}")
