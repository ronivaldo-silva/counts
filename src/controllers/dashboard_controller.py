import flet as ft

class DashboardController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = None

    def set_view(self, view):
        self.view = view

    def get_finance_data(self, user_id):
        # Mock data simulation
        return {
            "total_contribuicoes": 1250.00,
            "dividas": {
                "Mensalidade": 300.00,
                "Cantina": 45.50,
                "Dízimo": 0.00,
                "Big Loja": 120.00,
                "Cota Preparo": 30.00,
                "Cotas": 100.00
            },
            "detalhes_dividas": [
                {"data": "2023-10-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Outubro/2023"},
                {"data": "2023-09-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Setembro/2023"},
                {"data": "2023-08-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Agosto/2023"},
                {"data": "2023-10-15", "categoria": "Big Loja", "valor": 120.00, "desc": "Compra de Uniforme"},
                {"data": "2023-10-20", "categoria": "Cantina", "valor": 45.50, "desc": "Lanches"},
            ]
        }

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
