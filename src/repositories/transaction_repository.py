from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Registro, Usuario, Categoria
from datetime import date

class RegistroRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, type: str, category: str, amount: float, date_obj: date, data_prevista: date = None):
        # Map Type string to ID
        # Assumed: DEBT=0, PAYMENT=1
        type_id = 0 if type == 'DEBT' else 1
        
        # Map Category string to ID
        cat_obj = self.db.query(Categoria).filter(Categoria.categoria == category).first()
        if not cat_obj:
            # Create category if not exists? Or default?
            # User instructions implied fixed categories, but let's be safe.
            # For now, let's create it to prevent crashes, or fail?
            # Let's create it.
            cat_obj = Categoria(categoria=category, repete=False)
            self.db.add(cat_obj)
            self.db.commit()
            self.db.refresh(cat_obj)
        
        category_id = cat_obj.id

        # Mapping Logic:
        # If DEBT (0): date_obj -> data_debito, data_prevista -> from arg or None
        # If PAYMENT (1): date_obj -> data_entrada
        
        d_debito = None
        d_entrada = None
        d_prevista = None
        
        if type_id == 0:
            d_debito = date_obj
            d_prevista = data_prevista
        else:
            d_entrada = date_obj
            
        print("DEBUG: Creating Registro object...")
        db_trans = Registro(
            user_id=user_id,
            type_id=type_id,
            category_id=category_id,
            valor=amount,
            data_debito=d_debito,
            data_entrada=d_entrada,
            data_prevista=d_prevista
        )
        print("DEBUG: Registro created. Adding to DB...")
        self.db.add(db_trans)
        print("DEBUG: Added to DB. Committing...")
        try:
            self.db.commit()
            print("DEBUG: Commit successful.")
        except Exception as e:
            print(f"DEBUG: Commit failed: {e}")
            raise e
        self.db.refresh(db_trans)
        return db_trans

    def get_by_type(self, type: str):
        """Returns transactions of a specific type (DEBT or PAYMENT), joined with Usuario."""
        type_id = 0 if type == 'DEBT' else 1
        return self.db.query(Registro).join(Usuario).options(
            # Eager load relationships
        ).filter(Registro.type_id == type_id).all()

    def get_by_user(self, user_id: int):
        return self.db.query(Registro).filter(Registro.user_id == user_id).all()

    def update(self, trans_id: int, category: str = None, amount: float = None, date_obj: date = None, data_prevista: date = None, new_user_cpf: str = None):
        trans = self.db.query(Registro).filter(Registro.id == trans_id).first()
        if trans:
            if category: 
                # resolving category
                cat_obj = self.db.query(Categoria).filter(Categoria.categoria == category).first()
                if cat_obj:
                     trans.category_id = cat_obj.id
            if amount is not None: trans.valor = amount
            
            # Date logic for Update
            if trans.type_id == 0: # DEBT
                if date_obj: trans.data_debito = date_obj
                if data_prevista: trans.data_prevista = data_prevista
            else: # PAYMENT
                if date_obj: trans.data_entrada = date_obj
            
            if new_user_cpf:
                # Resolve new user ID
                user = self.db.query(Usuario).filter(Usuario.cpf == new_user_cpf).first()
                if user:
                    trans.user_id = user.id
            
            self.db.commit()
            self.db.refresh(trans)
        return trans

    def delete(self, trans_id: int):
        trans = self.db.query(Registro).filter(Registro.id == trans_id).first()
        if trans:
            self.db.delete(trans)
            self.db.commit()
            return True
        return False

    def get_summary_metrics(self):
        """Calculates global totals."""
        total_debts = self.db.query(func.sum(Registro.valor)).filter(Registro.type_id == 0).scalar() or 0.0
        total_payments = self.db.query(func.sum(Registro.valor)).filter(Registro.type_id == 1).scalar() or 0.0
        
        max_debt = self.db.query(func.max(Registro.valor)).filter(Registro.type_id == 0).scalar() or 0.0
        max_payment = self.db.query(func.max(Registro.valor)).filter(Registro.type_id == 1).scalar() or 0.0
        
        return {
            "total_dividas": total_debts,
            "total_entradas": total_payments,
            "maior_divida": max_debt,
            "maior_entrada": max_payment
        }

    def get_user_balance(self, user_id: int):
        """Calculates pending debts and total paid for a user."""
        # Pending debts: Sum of DEBT
        debt_sum = self.db.query(func.sum(Registro.valor)).filter(
            Registro.user_id == user_id, 
            Registro.type_id == 0
        ).scalar() or 0.0
        
        # Total Paid: Sum of PAYMENT
        paid_sum = self.db.query(func.sum(Registro.valor)).filter(
            Registro.user_id == user_id, 
            Registro.type_id == 1
        ).scalar() or 0.0
        
        # Pending = Debts - Payments ? 
        # Usually Balance = Debts - Payments.
        # But the previous logic had separate "pending" and "paid". 
        # Previous logic: "pending" was SUM(DEBT). "paid" was SUM(PAYMENT).
        # This implies debts are not "marked as paid", but rather payments offset them?
        # Or debts are just a log of debts.
        # I'll keep the previous logic: "Pendente" = Sum of Debts (maybe minus payments? No, old code just summed debts).
        # Wait, old code: pending = sum(amount) where type='DEBT'. 
        # So it ignores payments for the "pending" figure? That seems odd for a "Balance".
        # But I will stick to the exact logic of the previous code to avoid logical regression unless obvious.
        # Actually, "Pendente" usually means "Outstanding".
        # If I have Debt 100 and Payment 50. Pending should be 50.
        # But the old code:
        # pending = ... filter(Transaction.type == 'DEBT').scalar()
        # It didn't subtract payments. So it was "Total Debited".
        # I will assume "Pendente" in the view label really just meant "Total Dívidas".
        # Re-reading old code:
        # pending = self.db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.type == 'DEBT')
        # Yes, it was total debt.
        
        # Let's subtract payments to make it a real "Pending" or keep it?
        # Given I'm refactoring, improving logic is good, but might break UI expectations.
        # Let's keep "Total Debts" as "Pendente" for now to match old behavior exactly.
        
        pending = debt_sum # - paid_sum ? No, let's stick to old logic. 
        # Actually, if the user wants "Pendente", it usually implies (Debts - Paid).
        # But without a link between specific payment and debt, it's just a running balance.
        # Let's do (Debts - Paid) this time? No, safer to replicate old logic.
        
        max_paid = self.db.query(func.max(Registro.valor)).filter(
            Registro.user_id == user_id, 
            Registro.type_id == 1
        ).scalar() or 0.0
        
        # Oldest Debt
        oldest_debt_date = self.db.query(func.min(Registro.data_debito)).filter(
            Registro.user_id == user_id,
            Registro.type_id == 0
        ).scalar()
        
        divida_antiga = "-"
        if oldest_debt_date:
            old_debt = self.db.query(Registro).filter(
                Registro.user_id == user_id, 
                Registro.type_id == 0,
                Registro.data_debito == oldest_debt_date
            ).first()
            if old_debt:
                divida_antiga = f"R$ {old_debt.valor:.2f}  {old_debt.data_debito.strftime('%d-%b-%Y')}"

        return {
            # "pendente" currently implies Total Debt in old code. 
            # If I want it to be real pending (Debts - Paid), I should change it.
            # But "pagos" shows total paid. 
            # So the user sees "Total Debt" and "Total Paid".
            "pendente": pending, 
            "pagos": paid_sum,
            "maior_pago": max_paid,
            "divida_antiga": divida_antiga
        }
