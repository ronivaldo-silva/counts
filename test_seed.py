"""
Script de teste para verificar se o seed de dados básicos está funcionando
"""
import sys
sys.path.insert(0, 'src')

from database.config import engine, Base, seed_basic_data
from database.models import Usuario, Categoria, Classificacao
from database.config import SessionLocal

# Create tables
print("Criando tabelas...")
Base.metadata.create_all(bind=engine)

# Run seed
print("\nExecutando seed...")
seed_basic_data()

# Verify
print("\n" + "="*50)
print("VERIFICANDO DADOS POPULADOS:")
print("="*50)

db = SessionLocal()
try:
    # Check categories
    cats = db.query(Categoria).all()
    print(f"\n✅ Categorias ({len(cats)}):")
    for cat in cats:
        print(f"   - {cat.categoria} (repete: {cat.repete})")
    
    # Check classifications
    classifs = db.query(Classificacao).all()
    print(f"\n✅ Classificações ({len(classifs)}):")
    for cl in classifs:
        print(f"   - {cl.classificacao}")
    
    # Check admin
    admin = db.query(Usuario).filter(Usuario.cpf == "00000000000").first()
    if admin:
        print(f"\n✅ Admin User:")
        print(f"   - CPF: {admin.cpf}")
        print(f"   - Nome: {admin.nome}")
        print(f"   - Is Admin: {admin.is_admin}")
    else:
        print("\n❌ Admin não encontrado!")
        
finally:
    db.close()

print("\n" + "="*50)
print("TESTE CONCLUÍDO!")
print("="*50)
