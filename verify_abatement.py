
import os
import sys

# Override ENV to use local SQLite for verification
os.environ["DATABASE_URL"] = "sqlite:///verify.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from database.models import Base, Usuario, Categoria, Classificacao, Registro
from repositories.transaction_repository import RegistroRepository

def verify():
    # Setup DB
    engine = create_engine("sqlite:///verify.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    repo = RegistroRepository(db)
    
    print("--- Setting up Data ---")
    # Create User
    user = Usuario(cpf="123", nome="TestUser")
    db.add(user)
    
    # Create Categories
    cat = Categoria(categoria="TestCat", repete=False)
    db.add(cat)
    
    # Create Classifications
    # 1=Pendente, 3=Pago, 4=Parcial
    c1 = Classificacao(id=1, classificacao="Pendente")
    c3 = Classificacao(id=3, classificacao="Pago")
    c4 = Classificacao(id=4, classificacao="Parcial")
    db.add_all([c1, c3, c4])
    
    db.commit()
    user_id = user.id
    cat_name = cat.categoria
    
    print("--- Test 1: Create Debt ---")
    debt1 = repo.create(user_id, 'DEBT', cat_name, 100.0, date(2025, 1, 1))
    print(f"Debt1 Created: ID={debt1.id}, Val={debt1.valor}, Saldo={debt1.saldo}, Status={debt1.classificacao_id}")
    assert debt1.saldo == 100.0
    assert debt1.classificacao_id == 1
    
    print("--- Test 2: Partial Payment (60.00) ---")
    pay1 = repo.create(user_id, 'PAYMENT', cat_name, 60.0, date(2025, 1, 5))
    
    # Refresh debt1
    db.refresh(debt1)
    print(f"Debt1 After Payment: Saldo={debt1.saldo}, Status={debt1.classificacao_id}")
    assert debt1.saldo == 40.0
    assert debt1.classificacao_id == 4 # Parcial
    
    print("--- Test 3: Create Second Debt (50.00) ---")
    debt2 = repo.create(user_id, 'DEBT', cat_name, 50.0, date(2025, 1, 10))
    print(f"Debt2 Created: ID={debt2.id}, Val={debt2.valor}, Saldo={debt2.saldo}, Status={debt2.classificacao_id}")
    
    print("--- Test 4: Full Payment of Remainder + Part of Debt2 (Total 60.00) ---")
    # Pay 60. 40 goes to Debt1 (Finalizing it), 20 goes to Debt2.
    pay2 = repo.create(user_id, 'PAYMENT', cat_name, 60.0, date(2025, 1, 15))
    
    db.refresh(debt1)
    db.refresh(debt2)
    
    print(f"Debt1 Final: Saldo={debt1.saldo}, Status={debt1.classificacao_id}")
    print(f"Debt2 Final: Saldo={debt2.saldo}, Status={debt2.classificacao_id}")
    
    assert debt1.saldo == 0.0
    assert debt1.classificacao_id == 3 # Pago
    assert debt2.saldo == 30.0 # 50 - 20
    assert debt2.classificacao_id == 4 # Parcial

    print("--- Test 5: Verify Dashboard Logic (Get Pending) ---")
    # Should only return Debt2 with saldo
    debts = repo.get_divi_by_user(user_id)
    print(f"Pending Debts Found: {len(debts)}")
    for d in debts:
        print(f" - ID={d.id}, Saldo={d.saldo}")
        
    assert len(debts) == 1
    assert debts[0].id == debt2.id
    assert debts[0].saldo == 30.0

    print("SUCCESS: Abatement Logic Verified!")

if __name__ == "__main__":
    verify()
