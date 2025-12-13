import flet as ft
from datetime import datetime, date
from database.config import SessionLocal
from repositories.user_repository import UsuarioRepository
from repositories.transaction_repository import RegistroRepository, CategoriasRepository

class GestaoController:
    """
    Controller for the Management Dashboard (Gestão View).
    Manages Users, Debts, Payments (Entradas), and calculating Reports/Metrics using PostgreSQL.
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = None
        
        self.db = SessionLocal()
        self.user_repo = UsuarioRepository(self.db)
        self.trans_repo = RegistroRepository(self.db)
        self.cat_repo = CategoriasRepository(self.db)

    def set_view(self, view):
        """Sets the reference to the View."""
        self.view = view

    # ==========================
    # Transformers (Model -> Dict)
    # ==========================
    def _user_to_dict(self, user):
        """Converts User DB object to dictionary for View compatibility."""
        if not user: return {}
        
        # Calculate balance dynamically
        balance = self.trans_repo.get_user_balance(user.id)
        
        return {
            "id": user.id,
            "cpf": user.cpf,
            "nome": user.nome,
            "pendente": balance['pendente'],
            "pagos": balance['pagos'],
            "maior_pago": balance['maior_pago'],
            "divida_antiga": balance['divida_antiga'],
            "is_admin": user.is_admin,
            "senha": user.senha
        }

    def _trans_to_dict(self, trans):
        """Converts Transaction DB object to dictionary."""
        if not trans: return {}
        
        # Determine type string from ID (0=DEBT, 1=PAYMENT)
        type_str = 'DEBT' if trans.type_id == 0 else 'PAYMENT'
        
        # Handle Relationships (Usuario and Categoria)
        user_name = trans.usuario.nome if trans.usuario else "Desconhecido"
        user_cpf = trans.usuario.cpf if trans.usuario else ""
        category_name = trans.categoria_rel.categoria if trans.categoria_rel else "Sem Categoria"

        # Safe date formatting
        data_divida_str = trans.data_debito.strftime("%Y-%m-%d") if trans.data_debito else ""
        data_prevista_str = trans.data_prevista.strftime("%Y-%m-%d") if trans.data_prevista else ""
        data_entrada_str = trans.data_entrada.strftime("%Y-%m-%d") if trans.data_entrada else ""
        
        # If DEBT, we show 'data_divida' as primary 'data', but maybe view needs explicit fields
        # Previously we mashed into 'data'. Now we serve explicit keys.
        
        return {
            "id": trans.id,
            "cpf": user_cpf,
            "nome": user_name,
            "categoria": category_name,
            "categoria_id": trans.category_id,  # ID da categoria para uso em dropdowns
            "valor": trans.valor, 
            "data_divida": data_divida_str,
            "data_prevista": data_prevista_str,
            "data_entrada": data_entrada_str,
            "data": data_divida_str if type_str == 'DEBT' else data_entrada_str, # Legacy/Compat field?
            "type": type_str
        }
    def _update_view_gests(self):
        self.view.update_usuarios_table()
        self.view.update_dividas_table()
        self.view.update_entradas_table()

    # ==========================
    # User Management
    # ==========================

    def get_usuarios(self):
        """Returns the list of users as dicts."""
        users = self.user_repo.get_all()
        return [self._user_to_dict(u) for u in users]

    def add_usuario(self, data):
        """
        Adds a new user to the DB.
        Also handles the initial transaction (debt or payment) if provided.
        """
        # Create User
        new_user = self.user_repo.create(data['cpf'], data['nome'])
        
        if not new_user:
            self.view.show_message("Erro: CPF já cadastrado!", ft.Colors.RED)
            return

        # Add Initial Transaction
        self._add_debt_or_payment(data)

        self._update_view_gests()
        self.view.show_message("Usuário adicionado com sucesso!", ft.Colors.GREEN)

    def update_usuario(self, data):
        """Updates user details (Name, Password)."""
        senha = data.get('senha')
        # Only update password if provided and not empty
        senha_arg = senha if senha else None
        
        self.user_repo.update(data['cpf'], nome=data['nome'], senha=senha_arg)
        self._update_view_gests()
        self.view.show_message("Usuário atualizado com sucesso!", ft.Colors.GREEN)

    def delete_usuario(self, cpf):
        """Removes a user from the DB."""
        if self.user_repo.delete(cpf):
            self._update_view_gests()
            self.view.show_message("Usuário removido com sucesso!", ft.Colors.GREEN)
        else:
            self.view.show_message("Erro ao remover usuário.", ft.Colors.RED)

    # ==========================
    # Transaction Management (Dividas/Entradas)
    # ==========================

    def get_dividas(self, search_term=""):
        """Returns a filtered list of debts."""
        all_debts = self.trans_repo.get_by_type('DEBT')
        # Convert to dicts
        results = [self._trans_to_dict(d) for d in all_debts]
        
        if not search_term:
            return results
                
        search = search_term.lower()
        return [d for d in results if 
                search in d['cpf'].lower() or 
                search in d['nome'].lower() or 
                search in d['categoria'].lower()]

    def get_entradas(self, search_term=""):
        """Returns a filtered list of payments."""
        all_payments = self.trans_repo.get_by_type('PAYMENT')
        # Convert to dicts
        results = [self._trans_to_dict(p) for p in all_payments]
        
        if not search_term:
            return results
            
        search = search_term.lower()
        return [p for p in results if 
                search in p['cpf'].lower() or 
                search in p['nome'].lower() or 
                search in p['categoria'].lower()]

    def add_transaction(self, data):
        """Adds a debt or payment to an existing user."""
        self._add_debt_or_payment(data)
        self._update_view_gests()
        self.view.show_message("Transação adicionada com sucesso!", ft.Colors.GREEN)

    def _add_debt_or_payment(self, data):
        """Helper to process a generic transaction data dict."""
        valor = float(str(data['valor']).replace(',', '.')) if data['valor'] else 0.0
        
        # Find User ID
        user = self.user_repo.get_by_cpf(data['cpf'])
        if not user:
            return # Should handle error

        transaction_type = 'PAYMENT' if data.get('is_pago') else 'DEBT'
        
        # Parse Dates
        # data['data'] is treated as "Data Dívida" for Debts, "Data Pagamento" for Payments
        try:
            date_obj = datetime.strptime(data['data'], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            date_obj = datetime.now().date() # Default to today if missing/invalid

        # Parse Data Prevista (only for Debts)
        data_prevista = None
        if transaction_type == 'DEBT':
            try:
                if data.get('data_prevista'):
                    data_prevista = datetime.strptime(data['data_prevista'], "%Y-%m-%d").date()
            except ValueError:
                pass # Ignore invalid format

        self.trans_repo.create(
            user_id=user.id,
            type=transaction_type,
            category=data['categoria'],
            amount=valor,
            date_obj=date_obj,
            data_prevista=data_prevista
        )
        self.view.update_reports()
        self._update_view_gests()

    def update_transaction(self, data, transaction_type):
        """Updates an existing transaction."""
        val = float(str(data['valor']).replace(',', '.'))
        
        try:
            date_obj = datetime.strptime(data['data'], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            date_obj = datetime.now().date()

        data_prevista = None
        if transaction_type == "divida":
             try:
                if data.get('data_prevista'):
                    data_prevista = datetime.strptime(data['data_prevista'], "%Y-%m-%d").date()
             except ValueError:
                pass

        self.trans_repo.update(
            trans_id=data['id'],
            category=data['categoria'],
            amount=val,
            date_obj=date_obj,
            data_prevista=data_prevista,
            new_user_cpf=data['cpf']
        )
        
        if transaction_type == "divida":
            self.view.update_dividas_table()
        else:
            self.view.update_entradas_table()
            
        self.view.update_usuarios_table() # Update stats
        self.view.show_message("Transação atualizada com sucesso!", ft.Colors.GREEN)

    def add_divida(self, cpf, categoria, valor, data):
        """Internal/Direct: Adds debt record."""
        # Use helper
        payload = {
            'cpf': cpf, 'categoria': categoria, 'valor': valor, 'data': data, 'is_pago': False
        }
        self._add_debt_or_payment(payload)
        self.view.show_message("Dívida adicionada com sucesso!", ft.Colors.GREEN)

    def add_entrada(self, cpf, categoria, valor, data):
        """Internal/Direct: Adds payment record."""
        # Use helper
        payload = {
            'cpf': cpf, 'categoria': categoria, 'valor': valor, 'data': data, 'is_pago': True
        }
        self._add_debt_or_payment(payload)
        self.view.show_message("Entrada adicionada com sucesso!", ft.Colors.GREEN)

    def delete_transaction(self, trans_id):
        """Deletes a transaction."""
        if self.trans_repo.delete(trans_id):
            self._update_view_gests()
            self.view.show_message("Transação removida com sucesso!", ft.Colors.GREEN)
        else:
            self.view.show_message("Erro ao remover transação.", ft.Colors.RED)

    def get_categorias(self):
        """Returns the list of categories as dicts."""
        categories = self.cat_repo.get_all()
        return [{"id": u.id, "categoria": u.categoria} for u in categories]

    # ==========================
    # Reports / Metrics
    # ==========================

    def get_metrics(self, user_cpf=None, data_inicial=None, data_final=None, categoria=None, tipo=None):
        """
        Calcula métricas globais para o dashboard com filtros opcionais.
        
        Args:
            user_cpf (str, optional): CPF do usuário
            data_inicial (date, optional): Data inicial do intervalo
            data_final (date, optional): Data final do intervalo
            categoria (str, optional): Nome da categoria
            tipo (str, optional): Tipo da transação ('DEBT', 'PAYMENT', ou None para todos)
        """
        return self.trans_repo.get_summary_metrics(
            user_cpf=user_cpf,
            data_inicial=data_inicial,
            data_final=data_final,
            categoria=categoria,
            tipo=tipo
        )
    
    def get_filtered_transactions(self, user_cpf=None, data_inicial=None, data_final=None, categoria=None, tipo=None):
        """
        Retorna transações filtradas por múltiplos critérios em formato de dicionário.
        
        Args:
            user_cpf (str, optional): CPF do usuário
            data_inicial (date, optional): Data inicial do intervalo
            data_final (date, optional): Data final do intervalo
            categoria (str, optional): Nome da categoria
            tipo (str, optional): Tipo da transação ('DEBT', 'PAYMENT', ou None para todos)
        
        Returns:
            list: Lista de dicionários com transações filtradas
        """
        transactions = self.trans_repo.get_with_filters(
            user_cpf=user_cpf,
            data_inicial=data_inicial,
            data_final=data_final,
            categoria=categoria,
            tipo=tipo
        )
        return [self._trans_to_dict(t) for t in transactions]

    # ==========================
    # Authentication
    # ==========================

    def logout(self):
        """Handles user logout and navigation back to login."""
        self.db.close() # Close connection
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        
        self.page.clean()
        
        # Re-init login
        login_controller = LoginController(self.page)
        login_view = LoginView(self.page, login_controller)
        login_controller.set_view(login_view)
        
        self.page.add(login_view)
        self.page.update()
