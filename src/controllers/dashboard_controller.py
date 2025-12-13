import flet as ft
from database.config import SessionLocal
from repositories.transaction_repository import RegistroRepository

class DashboardController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = None
        self.db = SessionLocal()
        self.trans_repo = RegistroRepository(self.db)

    def set_view(self, view):
        self.view = view

    def get_finance_data(self, user_id):
        ### Mock data simulation
        registros = self.trans_repo.get_by_user(user_id)

        # Agrupar registros por categoria com soma de valores
        grouped_data = {}
        for registro in registros:
            categoria = registro.categoria
            valor = registro.valor
            if categoria in grouped_data:
                grouped_data[categoria] += valor
            else:
                grouped_data[categoria] = valor
        
        return {
            "total_contribuicoes": 1250.00,
            "dividas": grouped_data,
            "detalhes_dividas": [
                {"data": "2023-10-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Outubro/2023"},
                {"data": "2023-09-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Setembro/2023"},
                {"data": "2023-08-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Agosto/2023"},
                {"data": "2023-10-15", "categoria": "Big Loja", "valor": 120.00, "desc": "Compra de Uniforme"},
                {"data": "2023-10-20", "categoria": "Cantina", "valor": 45.50, "desc": "Lanches"},
            ]
        }
    ### Tocar a lógica do código, criar DTO object

    def logout(self):
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        
        self.page.clean()
        
        # Re-init login
        login_controller = LoginController(self.page)
        login_view = LoginView(self.page, login_controller)
        login_controller.set_view(login_view)
        
        self.page.add(login_view)
        self.page.update()
