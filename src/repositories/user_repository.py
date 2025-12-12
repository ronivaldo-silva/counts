from sqlalchemy.orm import Session
from database.models import Usuario
from sqlalchemy import exc

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cpf(self, cpf: str):
        return self.db.query(Usuario).filter(Usuario.cpf == cpf).first()

    def get_all(self):
        return self.db.query(Usuario).all()

    def create(self, cpf: str, nome: str, senha: str = None, is_admin: bool = False):
        db_user = Usuario(cpf=cpf, nome=nome, senha=senha, is_admin=is_admin)
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except exc.IntegrityError:
            self.db.rollback()
            return None # Duplicate CPF

    def update(self, cpf: str, nome: str = None, senha: str = None):
        user = self.get_by_cpf(cpf)
        if user:
            if nome:
                user.nome = nome
            if senha is not None:
                user.senha = senha
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, cpf: str):
        user = self.get_by_cpf(cpf)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
