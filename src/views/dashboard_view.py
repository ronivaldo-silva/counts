import flet as ft
from controllers.dashboard_controller import DashboardController

class DashboardView(ft.Column):
    def __init__(self, page: ft.Page, controller: DashboardController, user_name: str, user_id: int):
        super().__init__()
        self.page = page
        self.controller = controller
        self.user_name = user_name
        self.user_id = user_id
        # self.page.window_height = 1080 # Removed to avoid overriding global settings if not needed, or keep if strict requirements
        self.page.bgcolor = ft.Colors.WHITE
        self.scroll = ft.ScrollMode.AUTO
        
        # Fetch Data
        self.data = self.controller.get_dividas_data(self.user_id)
        
        self._build_ui()

    def _build_ui(self):
        # --- Header ---
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Image(src="splash_android.png", width=60, height=60, fit=ft.ImageFit.CONTAIN), # Reduced size slightly
                        padding=2,
                    ),
                    ft.Column(
                        [
                            ft.Text(f"Olá, {self.user_name}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text("Bem-vindo ao seu painel financeiro", size=14, color=ft.Colors.GREY_600),
                        ],
                        spacing=2
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(ft.Icons.LOGOUT, tooltip="Sair", on_click=lambda e: self.controller.logout(), icon_color=ft.Colors.BLUE_900)
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
            margin=ft.margin.only(bottom=20)
        )

        # --- Total Pendente Card ---
        total_pendente = self.data["total_dividas"]
        total_card = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.MONEY_OFF, color=ft.Colors.WHITE, size=40),
                    ft.Column(
                        [
                            ft.Text("Total Pendente", color=ft.Colors.WHITE70, size=14),
                            ft.Text(f"R$ {total_pendente:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), color=ft.Colors.WHITE, size=24, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=0
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=ft.Colors.RED_400, # Matches the red/salmon color
            border_radius=15,
            padding=20,
            width=350, # Fixed width for the card style
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, ft.Colors.RED_400))
        )

        # --- Debts List ---
        debt_items = []
        for item in self.data["dividas_agrupadas"]:
            debt_items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.MONEY_OFF_CSRED_OUTLINED, color=ft.Colors.RED_400, size=30), # Icon style
                                    ft.Column(
                                        [
                                            ft.Text(item["categoria"], size=14, color=ft.Colors.BLACK87),
                                            ft.Text(f"R$ {item['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                        ],
                                        spacing=0
                                    ),
                                ]
                            ),
                            ft.Column(
                                [
                                    ft.Text("Atualizado", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.RIGHT),
                                    ft.Text(item["data_atualizacao"], size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_500, text_align=ft.TextAlign.RIGHT),
                                ],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.END
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=15,
                    border=ft.border.all(1, ft.Colors.RED_200),
                    border_radius=15,
                    bgcolor=ft.Colors.WHITE,
                    margin=ft.margin.only(bottom=10)
                )
            )

        if not debt_items:
             debt_items.append(ft.Text("Nenhuma pendência encontrada!", color=ft.Colors.GREEN))

        debts_column = ft.Column(
            controls=debt_items,
            spacing=10
        )

        # --- QR Code Section ---
        pix_key = "tes.mestrevicentemarques@udv.org.br"
        qr_section = ft.Column(
            [
                ft.Image(src="qrpix.png", width=250, height=250, fit=ft.ImageFit.CONTAIN),
                ft.Text(pix_key, size=16, color=ft.Colors.BLACK87, text_align=ft.TextAlign.CENTER),
                ft.IconButton(
                    icon=ft.Icons.COPY, 
                    icon_color=ft.Colors.BLUE_500, 
                    tooltip="Copiar chave Pix",
                    on_click=lambda e: (self.page.set_clipboard(pix_key), self.page.open(ft.SnackBar(ft.Text("Chave Pix copiada!"))))
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START
        )

        # --- Main Layout (Responsive) ---
        # Left side: Total Card + Debts List
        left_content = ft.Column(
            [
                total_card,
                ft.Container(height=20),
                debts_column
            ],
            scroll=ft.ScrollMode.ADAPTIVE
        )

        # Responsive Row
        # Col parameter: dictionaries defining column span for different breakpoints (xs, sm, md, lg, xl, xxl)
        # 12 columns total
        self.controls = [
            header,
            ft.ResponsiveRow(
                [
                    ft.Column(col={"sm": 12, "md": 7}, controls=[left_content]),
                    ft.Column(col={"sm": 12, "md": 5}, controls=[qr_section], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=30
            )
        ]

