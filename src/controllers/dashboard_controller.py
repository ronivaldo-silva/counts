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
            categoria = registro.categoria_rel.categoria
            valor = registro.valor
            if categoria in grouped_data:
                grouped_data[categoria] += valor # Soma o valor se a categoria já existir
            else:
                grouped_data[categoria] = valor # Adiciona o valor se ainda não existir

        total_contribuicoes = sum(registro.valor for registro in registros if registro.type_id == 0)

        total_dividas = sum(registro.valor for registro in registros if registro.type_id == 1)
        return {
            "total_contribuicoes": total_contribuicoes,
            "dividas": grouped_data,
            "detalhes_dividas": [
                {"data": "2023-10-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Outubro/2023"},
                {"data": "2023-09-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Setembro/2023"},
                {"data": "2023-08-10", "categoria": "Mensalidade", "valor": 100.00, "desc": "Agosto/2023"},
                {"data": "2023-10-15", "categoria": "Big Loja", "valor": 120.00, "desc": "Compra de Uniforme"},
                {"data": "2023-10-20", "categoria": "Cantina", "valor": 45.50, "desc": "Lanches"},
            ]
        }

    def get_dividas_data(self, user_id):
        registros = self.trans_repo.get_divi_by_user(user_id)
        
        # Dictionary to hold aggregated data
        # Structure: { 'CategoryName': {'total': float, 'latest_date': datetime} }
        aggregated_data = {}

        for registro in registros:
            categoria = registro.categoria_rel.categoria
            valor = registro.valor
            data = registro.creado_em # Changed from data_debito to creado_em

            if categoria not in aggregated_data:
                aggregated_data[categoria] = {
                    'total': 0.0,
                    'latest_date': data
                }
            
            aggregated_data[categoria]['total'] += valor
            # Update latest date if current record is more recent
            if data > aggregated_data[categoria]['latest_date']:
                aggregated_data[categoria]['latest_date'] = data

        # Convert to list for the view
        dividas_summary = []
        total_pendente = 0.0
        
        for cat, data in aggregated_data.items():
            dividas_summary.append({
                "categoria": cat,
                "total": data['total'],
                "data_atualizacao": data['latest_date'].strftime("%d-%m-%Y")
            })
            total_pendente += data['total']

        return {
            "total_dividas": total_pendente,
            "dividas_agrupadas": dividas_summary
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
