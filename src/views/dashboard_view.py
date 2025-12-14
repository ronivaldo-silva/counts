from flet.core.padding import Padding
import flet as ft
from controllers.dashboard_controller import DashboardController

class DashboardView(ft.Column):
    def __init__(self, page: ft.Page, controller: DashboardController, user_name: str, user_id: int):
        super().__init__()
        self.page = page
        self.controller = controller
        self.user_name = user_name
        self.user_id = user_id
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        
        # Fetch Data
        self.data = self.controller.get_dividas_data(self.user_id)
        
        self._build_ui()

    # Cabeçalho 
    def _build_ui(self):
        # Header
        header = ft.Container(
            content=ft.Row(
                [
                    #ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.BLUE_600),
                    ft.Container(
                        content=ft.Image(src="splash_android.png", width=80, height=70, fit=ft.ImageFit.CONTAIN),
                        padding=2,
                        width=80,
                        height=70
                    ),
                    ft.Column(
                        [
                            ft.Text(f"Olá, {self.user_name}", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Bem-vindo ao seu painel financeiro", size=14, color=ft.Colors.GREY_600),
                        ],
                        spacing=2
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(ft.Icons.LOGOUT, tooltip="Sair", on_click=lambda e: self.controller.logout())
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )

        # Summary Cards
        total_divida = sum(self.data['dividas'].values())
        
        summary_row = ft.ResponsiveRow(
            [
                #self._build_summary_card("Contribuições", f"R$ {self.data['total_contribuicoes']:.2f}", ft.Icons.SAVINGS, ft.Colors.GREEN_500),
                self._build_summary_card("Total Pendente", f"R$ {total_divida:.2f}", ft.Icons.MONEY_OFF, ft.Colors.RED_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # Debts Categories
        dividas_controls = []
        for cat, val in self.data['dividas'].items():
            if val > 0:
                dividas_controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LABEL_IMPORTANT_OUTLINE, color=ft.Colors.ORANGE_400),
                        title=ft.Text(cat, weight=ft.FontWeight.W_500),
                        trailing=ft.Text(f"R$ {val:.2f}", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400)
                    )
                )
        
        if not dividas_controls:
            dividas_controls.append(ft.Text("Nenhuma pendência!", color=ft.Colors.GREEN))

        debts_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Pendências por Categoria", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column(dividas_controls)
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
            width=400
        )

        # Recent History (Oldest Debts/Details)
        history_rows = []
        for item in self.data['detalhes_dividas']:
             history_rows.append(
                 ft.DataRow(
                     cells=[
                         ft.DataCell(ft.Text(item['data'])),
                         ft.DataCell(ft.Text(item['categoria'])),
                         ft.DataCell(ft.Text(f"R$ {item['valor']:.2f}", color=ft.Colors.RED_400)),
                     ]
                 )
             )

        history_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Detalhamento de Pendências", size=18, weight=ft.FontWeight.BOLD),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Data")),
                            ft.DataColumn(ft.Text("Categoria")),
                            ft.DataColumn(ft.Text("Valor"), numeric=True),
                        ],
                        rows=history_rows,
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
            expand=True
        )

        self.controls = [
            header,
            ft.Container(height=20),
            summary_row,
            ft.Container(height=20),
            ft.Row([debts_card, history_card], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START, wrap=True, spacing=20)
        ]

    def _build_summary_card(self, title, value, icon, color):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=40, color=ft.Colors.WHITE),
                    ft.Column(
                        [
                            ft.Text(title, color=ft.Colors.WHITE70, size=14),
                            ft.Text(value, color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=2
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=300,
            height=70,
            bgcolor=color,
            border_radius=10,
            padding=10,
            shadow=ft.BoxShadow(blur_radius=5, color=color)
        )

    def _build_defice_card(self, data):
        return ft.Container(
            ft.Row(
                controls=[ft.Text(value=data, size=14, weight=ft.FontWeight.NORMAL) ]
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
            expand=True
        )

    def logout(self, e):
        # Deprecated, using controller
        pass
