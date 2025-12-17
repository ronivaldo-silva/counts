from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.config import DATABASE_URL, Base
from database.models import Usuario, Categoria, Classificacao, Registro
import os

# Admin credentials for initial setup
# Try to get root password from env, else default to empty or 'root'
# In many local setups (XAMPP/WAMP), root has no password.
ROOT_PASS = os.getenv("DB_ROOT_PASSWORD", "")
ADMIN_DB_URL = f"mysql+pymysql://root:{ROOT_PASS}@localhost:3306/mysql"

TARGET_DB_NAME = "Counts"
APP_USER = "userapp"
APP_PASS = "Li0nt0g3ro!"             

def create_database_and_user():
    print(f"Connecting to database server to setup DB and User...")
    try:
        engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Check if user exists
            # MySQL stores users in mysql.user table
            result = conn.execute(text(f"SELECT 1 FROM mysql.user WHERE User = '{APP_USER}'"))
            if not result.scalar():
                print(f"Creating user {APP_USER}...")
                conn.execute(text(f"CREATE USER '{APP_USER}'@'localhost' IDENTIFIED BY '{APP_PASS}'"))
                # Also allow remote access if needed? For now localhost
                conn.execute(text(f"CREATE USER '{APP_USER}'@'%' IDENTIFIED BY '{APP_PASS}'")) 
            else:
                print(f"User {APP_USER} already exists.")

            # Check if DB exists
            result = conn.execute(text(f"SELECT 1 FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{TARGET_DB_NAME}'"))
            if not result.scalar():
                print(f"Creating database {TARGET_DB_NAME}...")
                conn.execute(text(f"CREATE DATABASE `{TARGET_DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            else:
                print(f"Database {TARGET_DB_NAME} already exists.")

            # Grant privileges
            print(f"Granting privileges on database {TARGET_DB_NAME} to {APP_USER}...")
            conn.execute(text(f"GRANT ALL PRIVILEGES ON `{TARGET_DB_NAME}`.* TO '{APP_USER}'@'localhost'"))
            conn.execute(text(f"GRANT ALL PRIVILEGES ON `{TARGET_DB_NAME}`.* TO '{APP_USER}'@'%'"))
            conn.execute(text("FLUSH PRIVILEGES"))
            
        engine.dispose()
        print("Database and User setup complete.")
        
    except Exception as e:
        print(f"Error during database/user creation: {e}")
        print("Tip: Check if MariaDB is running on port 3306 and if root password is correct.")
        raise e

def create_tables_and_seed():
    print("Connecting to Counts database to create tables and seed data...")
    
    # We use the engine from config which points to the new DB
    from database.config import engine as app_engine, SessionLocal
    
    # Create tables
    print("Creating tables...")
    try:
        Base.metadata.create_all(bind=app_engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        return

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
                Categoria(categoria="Cotas Diversas", repete=False),
                Categoria(categoria="Doação", repete=False),
                Categoria(categoria="Outros", repete=False)
            ]
            db.add_all(cats)
            db.commit()
            print("✅ Categorias criadas!")
        else:
            print("Categorias already exist.")

        # Seed Classificacao
        if db.query(Classificacao).count() == 0:
            print("Seeding Classificacao...")
            classifications = [
                Classificacao(classificacao="Pendente"),
                Classificacao(classificacao="Vencido"),
                Classificacao(classificacao="Pago"),
                Classificacao(classificacao="Parcial")
            ]
            db.add_all(classifications)
            db.commit()
            print("✅ Classificações criadas!")
        else:
            print("Classificacao already exists.")

        # Seed Admin User
        if not db.query(Usuario).filter(Usuario.cpf == "00000000000").first():
            print("Seeding Admin User...")
            admin = Usuario(
                cpf="00000000000", 
                nome="Administrador", 
                senha="321", 
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário Admin criado!")
        else:
            print("Admin user already exists.")
            
        print("🎉 Setup completed successfully!")
        
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
        print(f"Setup failed: {e}")
