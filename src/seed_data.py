from database.config import SessionLocal, engine, Base
from database.models import Usuario, Registro, Categoria
from datetime import date
from sqlalchemy import text

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(Usuario).filter(Usuario.cpf == "00000000000").first()
    if not admin:
        print("Seeding Admin...")
        admin = Usuario(cpf="00000000000", nome="Administrador", senha="321", is_admin=True)
        db.add(admin)
    
    # Check if mock users exist
    if not db.query(Usuario).filter(Usuario.cpf == "11111111111").first():
        print("Seeding Mock Data...")
        # Users
        u1 = Usuario(cpf="11111111111", nome="User Mock 1", senha="123")
        u2 = Usuario(cpf="22222222222", nome="User Mock 2") # No pass
        db.add_all([u1, u2])
        db.commit()
        db.refresh(u1)
        db.refresh(u2)

        # Categorias need to exist first (handled by setup_database mostly)
        cat_mensal = db.query(Categoria).filter(Categoria.categoria=="Mensalidade").first()
        if not cat_mensal:
            cat_mensal = Categoria(categoria="Mensalidade", repete=True)
            db.add(cat_mensal)
        
        cat_cantina = db.query(Categoria).filter(Categoria.categoria=="Cantina").first()
        if not cat_cantina:
            cat_cantina = Categoria(categoria="Cantina", repete=False)
            db.add(cat_cantina)
        
        db.commit()

        # Transactions
        t1 = Registro(user_id=u1.id, type_id=0, category_id=cat_mensal.id, valor=100.0, data_debito=date(2023, 10, 10))
        t2 = Registro(user_id=u2.id, type_id=0, category_id=cat_cantina.id, valor=50.0, data_debito=date(2023, 10, 12))
        t3 = Registro(user_id=u1.id, type_id=1, category_id=cat_mensal.id, valor=100.0, data_entrada=date(2023, 10, 20))
        
        db.add_all([t1, t2, t3])
        db.commit()
        print("Seed Complete.")
    else:
        print("Data already exists.")
    
    db.close()

if __name__ == "__main__":
    seed()
