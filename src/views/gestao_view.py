import flet as ft
from datetime import datetime
from controllers.gestao_controller import GestaoController

class GestaoView(ft.Column):
    """
    View for the Management Dashboard.
    Contains Tabs for Users, Debts, Entradas, and Reports.
    Handles UI logic for CRUD operations via Dialogs.
    """
    def __init__(self, page: ft.Page, controller: GestaoController):
        super().__init__()
        self.page = page
        self.controller = controller
        self.expand = True
        
        # UI Setup
        self._build_ui()
        
        # Shared Components (e.g., DatePicker)
        self.date_picker = ft.DatePicker(
            on_change=self._on_date_change,
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
        )
        self.page.overlay.append(self.date_picker)

    # ==========================
    # Helpers
    # ==========================

    def show_message(self, message: str, color: str = ft.Colors.RED):
        """Displays a SnackBar message."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def _close_dialog(self):
        """Closes the currently open dialog."""
        self.page.close(self.dialog)

    def _on_date_change(self, e):
        """Handles DatePicker selection updates."""
        # Updates nu_data or et_data depending on context/active field
        # Ideally we should know which field triggered it.
        # For now, simplistic update if field exists
        if hasattr(self, 'nu_data'):
            self.nu_data.value = self.date_picker.value.strftime("%Y-%m-%d")
        if hasattr(self, 'et_data'):
            self.et_data.value = self.date_picker.value.strftime("%Y-%m-%d")
        self.page.update()

    # ==========================
    # Tab Builders
    # ==========================

    def _build_usuarios_tab(self):
        """Builds the User Management Tab."""
        # Top Action Bar
        self.search_field = ft.TextField(
            hint_text="Pesquisa CPF ou Nome",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            bgcolor=ft.Colors.GREY_200,
            border_width=0,
            height=40,
            content_padding=10,
            expand=True,
            on_change=lambda e: self.update_usuarios_table() # Live search
        )
        
        bt_new_user = ft.Row(
            [
                ft.ElevatedButton(
                    "Novo",
                    icon=ft.Icons.PERSON_ADD,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                    width=100,
                    on_click=lambda e: self._show_action_dialog("novo", None)
                ),
                ft.Container(width=20),
                ft.Container(content=self.search_field, width=350, border_radius=20)
            ],
            alignment=ft.MainAxisAlignment.START
        )

        # Table
        self.users_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CPF", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Pendente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Pagos", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Maior Pago", weight=ft.FontWeight.BOLD)),
                #ft.DataColumn(ft.Text("Divida mais antiga", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", weight=ft.FontWeight.BOLD)), # Actions
            ],
            rows=[],
            heading_row_color=ft.Colors.WHITE,
            data_row_color=ft.Colors.WHITE,
        )
        
        # Initial Load
        self.update_usuarios_table()

        return ft.Container(
            content=ft.Column([
                bt_new_user,
                ft.Container(height=20),
                ft.Column([self.users_table], scroll=ft.ScrollMode.AUTO, expand=True)
            ]),
            padding=20

        )

    def _build_dividas_tab(self):
        """Builds the Debts (Dívidas) Tab."""
        self.search_dividas = ft.TextField(
            hint_text="Pesquisa CPF, Nome ou Categoria",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            bgcolor=ft.Colors.GREY_200,
            border_width=0,
            height=40,
            content_padding=10,
            on_change=lambda e: self.update_dividas_table(),
            expand=True
        )
        
        bt_new_divida = ft.Row(
            [
                ft.ElevatedButton(
                    "Novo",
                    icon=ft.Icons.ADD,
                    bgcolor=ft.Colors.ORANGE,
                    width=100,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: self._show_action_dialog("nova_divida_tab", None)
                ),
                ft.Container(width=20),
                ft.Container(content=self.search_dividas, width=350, border_radius=20)
            ],
            alignment=ft.MainAxisAlignment.START
        )

        self.dividas_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CPF", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data Dívida", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data Prevista", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            heading_row_color=ft.Colors.WHITE,
            data_row_color=ft.Colors.WHITE,
        )
        
        self.update_dividas_table()

        return ft.Container(
            content=ft.Column([
                bt_new_divida,
                ft.Container(height=20),
                ft.Column([self.dividas_table], scroll=ft.ScrollMode.AUTO, expand=True)
            ]),
            padding=20
        )

    def _build_entradas_tab(self):
        """Builds the Payments (Entradas) Tab."""
        self.search_entradas = ft.TextField(
            hint_text="Pesquisa CPF, Nome ou Categoria",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            bgcolor=ft.Colors.GREY_200,
            border_width=0,
            height=40,
            content_padding=10,
            on_change=lambda e: self.update_entradas_table(),
            expand=True
        )
        
        bt_new_entrada = ft.Row(
            [
                ft.ElevatedButton(
                    "Novo",
                    icon=ft.Icons.ADD,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: self._show_action_dialog("nova_entrada_tab", None)
                ),
                ft.Container(width=20),
                ft.Container(content=self.search_entradas, width=350, border_radius=20)
            ],
            alignment=ft.MainAxisAlignment.START
        )

        self.entradas_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CPF", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            heading_row_color=ft.Colors.WHITE,
            data_row_color=ft.Colors.WHITE,
        )
        
        self.update_entradas_table()

        return ft.Container(
            content=ft.Column([
                bt_new_entrada,
                ft.Container(height=20),
                ft.Column([self.entradas_table], scroll=ft.ScrollMode.AUTO, expand=True)
            ]),
            padding=20
        )

    def _build_relatorios_tab(self):
        """Builds the Reports Tab with Filters."""
        # Filtros
        users = self.controller.get_usuarios()
        user_opts = [ft.dropdown.Option(key="", text="Todos")] + [
            ft.dropdown.Option(key=u['cpf'], text=f"{u['nome']} ({u['cpf']})") for u in users
        ]
        
        self.filter_user = ft.Dropdown(
            label="Usuário",
            width=300,
            options=user_opts,
            value="",
            enable_filter=True,
            leading_icon=ft.Icons.PERSON
        )
        
        categorias = self.controller.get_categorias()
        cat_opts = [ft.dropdown.Option(key="", text="Todas")] + [
            ft.dropdown.Option(key=c['categoria'], text=c['categoria']) for c in categorias
        ]
        
        self.filter_categoria = ft.Dropdown(
            label="Categoria",
            width=250,
            options=cat_opts,
            value=""
        )
        
        self.filter_tipo = ft.Dropdown(
            label="Tipo",
            width=200,
            options=[
                ft.dropdown.Option(key="", text="Todos"),
                ft.dropdown.Option(key="DEBT", text="Dívidas"),
                ft.dropdown.Option(key="PAYMENT", text="Entradas"),
            ],
            value=""
        )
        
        # Date Pickers para filtros
        self.filter_data_inicial = ft.TextField(
            label="Data Inicial",
            width=200,
            read_only=True,
            value="",
            hint_text="Selecione",
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.filter_date_picker_inicial)
            )
        )
        
        self.filter_data_final = ft.TextField(
            label="Data Final",
            width=200,
            read_only=True,
            value="",
            hint_text="Selecione",
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.filter_date_picker_final)
            )
        )
        
        # Criar DatePickers se não existirem
        if not hasattr(self, 'filter_date_picker_inicial'):
            self.filter_date_picker_inicial = ft.DatePicker(
                on_change=lambda e: self._on_filter_date_inicial_change(e),
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31)
            )
            self.page.overlay.append(self.filter_date_picker_inicial)
        
        if not hasattr(self, 'filter_date_picker_final'):
            self.filter_date_picker_final = ft.DatePicker(
                on_change=lambda e: self._on_filter_date_final_change(e),
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31)
            )
            self.page.overlay.append(self.filter_date_picker_final)
        
        # Linha de Filtros
        filters_row = ft.Container(
            content=ft.Column([
                ft.Text("Filtros", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.filter_user,
                    self.filter_categoria,
                    self.filter_tipo,
                ], wrap=True, spacing=10),
                ft.Row([
                    self.filter_data_inicial,
                    self.filter_data_final,
                    ft.ElevatedButton(
                        "Aplicar Filtros",
                        icon=ft.Icons.FILTER_ALT,
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self.update_reports()
                    ),
                    ft.ElevatedButton(
                        "Limpar Filtros",
                        icon=ft.Icons.CLEAR,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self._clear_filters()
                    ),
                ], wrap=True, spacing=10),
            ]),
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
        
        self.report_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("CPF")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Valor"), numeric=True),
                ft.DataColumn(ft.Text("Data")),
            ],
            rows=[],
        )
        
        self.metrics_container = ft.Row(wrap=True, spacing=20)
        
        # Initial load
        self.update_reports()

        return ft.Container(
            content=ft.Column([
                filters_row,
                ft.Divider(),
                ft.Text("Métricas", size=20, weight=ft.FontWeight.BOLD),
                self.metrics_container,
                ft.Divider(),
                ft.Text("Histórico Geral", size=20, weight=ft.FontWeight.BOLD),
                ft.Column([self.report_table], scroll=ft.ScrollMode.AUTO, height=400)
            ], scroll=ft.ScrollMode.AUTO),
            padding=20
        )
        
    def _build_metric_card(self, title, value, color):
        """Helper to create a metric card."""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, color=ft.Colors.WHITE),
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ]),
            bgcolor=color,
            padding=15,
            border_radius=10,
            width=150,
            height=100
        )

    # ==========================
    # Data Updaters
    # ==========================

    def update_usuarios_table(self):
        """Refreshes the User Management table from controller data."""
        users = self.controller.get_usuarios()
        # Filter if search is active (optional, could implement here or in controller)
        # Assuming controller returns all and we filter view-side or controller handles it.
        # Impl: controller.get_usuarios() returns raw list.
        # Let's adding simple search filtering view-side for Users tab since controller.get_usuarios() doesn't take args yet
        search = self.search_field.value.lower() if hasattr(self, 'search_field') and self.search_field.value else ""
        
        rows = []
        for u in users:
            if search and (search not in u['cpf'].lower() and search not in u['nome'].lower()):
                continue

            if u['is_admin']:
                bt_del_atributos = {
                    'inativo': True,
                    'cor': ft.Colors.BLACK12,
                    'tooltip': 'Não pode ser excluído'
                }
            else:
                bt_del_atributos = {
                    'inativo': False,
                    'cor': ft.Colors.RED,
                    'tooltip': 'Excluir Cadastro'
                }

            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(u['cpf'])),
                ft.DataCell(ft.Text(u['nome'])),
                ft.DataCell(ft.Text(f"R$ {u['pendente']:.2f}")),
                ft.DataCell(ft.Text(f"R$ {u['pagos']:.2f}")),
                ft.DataCell(ft.Text(f"R$ {u['maior_pago']:.2f}")),
                # ft.DataCell(ft.Text(u['is_admin'])),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, tooltip="Editar Cadastro", on_click=lambda e, u=u: self._show_action_dialog("editar", u)),
                    ft.IconButton(ft.Icons.ATTACH_MONEY, icon_color=ft.Colors.ORANGE, tooltip="Adicionar Dívida", on_click=lambda e, u=u: self._show_action_dialog("divida", u)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=bt_del_atributos['cor'], tooltip=bt_del_atributos['tooltip'], on_click=lambda e, u=u: self._show_action_dialog("deletar usuario", u), disabled=bt_del_atributos['inativo']),
                ])),
            ]))
        self.users_table.rows = rows
        self.page.update()

    def update_dividas_table(self):
        """Refreshes the Debts table."""
        data = self.controller.get_dividas(self.search_dividas.value if hasattr(self, 'search_dividas') else "")
        rows = []
        for d in data:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(d['cpf'])),
                ft.DataCell(ft.Text(d['nome'])),
                ft.DataCell(ft.Text(d['categoria'])),
                ft.DataCell(ft.Text(f"R$ {d['valor']:.2f}")),
                ft.DataCell(ft.Text(d.get('data_divida', ''))),
                ft.DataCell(ft.Text(d.get('data_prevista', ''))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, tooltip="Editar", on_click=lambda e, d=d: self._show_action_dialog("editar_transacao", d, "divida")),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, tooltip="Deletar", on_click=lambda e, d=d: self._show_action_dialog("deletar transacao", d, "divida"))
                ])),
            ]))
        self.dividas_table.rows = rows
        self.page.update()

    def update_entradas_table(self):
        """Refreshes the Payments table."""
        data = self.controller.get_entradas(self.search_entradas.value if hasattr(self, 'search_entradas') else "")
        rows = []
        for d in data:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(d['cpf'])),
                ft.DataCell(ft.Text(d['nome'])),
                ft.DataCell(ft.Text(d['categoria'])),
                ft.DataCell(ft.Text(f"R$ {d['valor']:.2f}")),
                ft.DataCell(ft.Text(d['data'])),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, tooltip="Editar", on_click=lambda e, d=d: self._show_action_dialog("editar_transacao", d, "entrada")),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, tooltip="Deletar", on_click=lambda e, d=d: self._show_action_dialog("deletar transacao", d, "entrada"))
                ])),
            ])) 
        self.entradas_table.rows = rows
        self.page.update()

    def update_reports(self):
        """Refreshes Metrics and Report Table with applied filters."""
        from datetime import datetime as dt
        
        # Coletar valores dos filtros
        user_cpf = None
        data_inicial = None
        data_final = None
        categoria = None
        tipo = None
        
        if hasattr(self, 'filter_user') and self.filter_user.value:
            user_cpf = self.filter_user.value if self.filter_user.value != "" else None
        
        if hasattr(self, 'filter_categoria') and self.filter_categoria.value:
            categoria = self.filter_categoria.value if self.filter_categoria.value != "" else None
        
        if hasattr(self, 'filter_tipo') and self.filter_tipo.value:
            tipo = self.filter_tipo.value if self.filter_tipo.value != "" else None
        
        if hasattr(self, 'filter_data_inicial') and self.filter_data_inicial.value:
            try:
                data_inicial = dt.strptime(self.filter_data_inicial.value, "%Y-%m-%d").date() if self.filter_data_inicial.value else None
            except ValueError:
                data_inicial = None
        
        if hasattr(self, 'filter_data_final') and self.filter_data_final.value:
            try:
                data_final = dt.strptime(self.filter_data_final.value, "%Y-%m-%d").date() if self.filter_data_final.value else None
            except ValueError:
                data_final = None
        
        # Atualizar métricas com filtros
        metrics = self.controller.get_metrics(
            user_cpf=user_cpf,
            data_inicial=data_inicial,
            data_final=data_final,
            categoria=categoria,
            tipo=tipo
        )
        
        self.metrics_container.controls = [
            self._build_metric_card("Total Dívidas", f"R$ {metrics['total_dividas']:.2f}", ft.Colors.RED_400),
            self._build_metric_card("Total Entradas", f"R$ {metrics['total_entradas']:.2f}", ft.Colors.GREEN_400),
            self._build_metric_card("Maior Dívida", f"R$ {metrics['maior_divida']:.2f}", ft.Colors.ORANGE_400),
            self._build_metric_card("Maior Entrada", f"R$ {metrics['maior_entrada']:.2f}", ft.Colors.BLUE_400),
        ]

        # Atualizar tabela com transações filtradas
        transactions = self.controller.get_filtered_transactions(
            user_cpf=user_cpf,
            data_inicial=data_inicial,
            data_final=data_final,
            categoria=categoria,
            tipo=tipo
        )
        
        rows = []
        for t in transactions:
            # Determinar cor e tipo baseado no type
            if t['type'] == 'DEBT':
                tipo_text = ft.Text("Dívida", color=ft.Colors.RED)
                data_display = t['data_divida']
            else:
                tipo_text = ft.Text("Entrada", color=ft.Colors.GREEN)
                data_display = t['data_entrada']
            
            rows.append(ft.DataRow(cells=[
                ft.DataCell(tipo_text),
                ft.DataCell(ft.Text(t['cpf'])),
                ft.DataCell(ft.Text(t['nome'])),
                ft.DataCell(ft.Text(t['categoria'])),
                ft.DataCell(ft.Text(f"R$ {t['valor']:.2f}")),
                ft.DataCell(ft.Text(data_display)),
            ]))
        
        self.report_table.rows = rows
        self.page.update()

    # ==========================
    # Dialog Builders & Actions
    # ==========================

    def _show_action_dialog(self, action, user_data, transaction_type=None):
        """
        Main dispatcher for opening dialogs based on action type.
        """
        title = ""
        content = None
        actions = []

        if action == "novo":
            self._build_new_user_dialog_content()
            return
        elif action == "nova_divida_tab":
             self._build_new_user_dialog_content(transaction_type="divida")
             return
        elif action == "nova_entrada_tab":
             self._build_new_user_dialog_content(transaction_type="entrada")
             return
        elif action == "editar":
            self._build_edit_user_dialog_content(user_data)
            return
        elif action == "divida":
            self._build_new_user_dialog_content(user_data)
            return
        elif action == "deletar usuario":
            title = "Confirmar Exclusão"
            content = ft.Text(f"Tem certeza que deseja excluir {user_data['nome']}?")
            actions = [
                ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog()),
                ft.ElevatedButton("Excluir", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: self._confirm_delete_user(user_data['cpf']))
            ]
        elif action == "deletar transacao":
            title = "Confirmar Exclusão"
            content = ft.Text(f"Tem certeza que deseja excluir o registro de:\n {user_data['nome']}\n {user_data['categoria']}\n {user_data['valor']}\n {user_data['data']}?")
            actions = [
                ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog()),
                ft.ElevatedButton("Excluir", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: self._confirm_delete_transaction(user_data['id']))
            ]
        elif action == "editar_transacao":
             self._build_edit_transaction_dialog(user_data, transaction_type)
             return
             
        self.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=content,
            actions=actions,
            modal=True
        )
        self.page.open(self.dialog)
        self.page.update()

    def _build_new_user_dialog_content(self, user_data=None, transaction_type=None):
        """Builds content for New User or New Transaction dialog."""
        self.is_adding_transaction = False
        self.nu_original_user_data = user_data
        
        # Determine mode
        is_transaction_mode = (transaction_type is not None) or (user_data is not None)

        if user_data:
            self.is_adding_transaction = True
            title_text = "Nova Transação"
        elif transaction_type:
            self.is_adding_transaction = True
            title_text = "Nova Dívida" if transaction_type == "divida" else "Nova Entrada"
        else:
            self.is_adding_transaction = False
            title_text = "Novo Usuário"

        # User Locator (Dropdown) for Translations
        self.nu_user_dropout = ft.Dropdown(
            label="Selecione o Usuário",
            width=500,
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            options=[],
            enable_filter=True,
            visible=False
        )

        # Standard Fields (for New User or Read-only display)
        self.nu_cpf = ft.TextField(label="CPF", width=250, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""), max_length=11)
        self.nu_nome = ft.TextField(label="Nome", expand=True)

        categorias = self.controller.get_categorias()
        cat_opts = [ft.dropdown.Option(text=c['categoria']) for c in categorias]

        self.nu_categoria = ft.Dropdown(
            label="Categoria",
            width=250,
            options=cat_opts
        )

        self.nu_valor = ft.TextField(label="Valor R$", width=250, prefix_text="R$ ", keyboard_type=ft.KeyboardType.NUMBER)
       
        # Logic to populate fields
        if is_transaction_mode:
            users = self.controller.get_usuarios()
            opts = [ft.dropdown.Option(key=u['cpf'], text=f"{u['nome']} ({u['cpf']})") for u in users]
            self.nu_user_dropout.options = opts
            
            if user_data:
                # Pre-select user if known
                self.nu_user_dropout.value = user_data['cpf']
                self.nu_user_dropout.disabled = True
                self.nu_user_dropout.visible = True
                self.nu_cpf.visible = False
                self.nu_nome.visible = False
            elif transaction_type:
                 # Generic add from Tab
                 self.nu_user_dropout.visible = True
                 self.nu_cpf.visible = False
                 self.nu_nome.visible = False
        else:
            # New User Mode
            self.nu_user_dropout.visible = False
            self.nu_cpf.visible = True
            self.nu_nome.visible = True
            self.nu_categoria.value = "Mensalidade"
            self.nu_valor.value = "100"
             
        # Toggle
        self.nu_is_pago = ft.Switch(value=False, on_change=self._on_nu_toggle_change)
        
        if transaction_type == "divida":
             self.nu_is_pago.value = False
             self.nu_is_pago.disabled = True
        elif transaction_type == "entrada":
             self.nu_is_pago.value = True
             self.nu_is_pago.disabled = True
             
        self.nu_data_label = ft.Text("Data Dívida", size=16) 
        self.nu_data = ft.TextField(
            label="Data Dívida",
            width=250,
            value=datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.date_picker)
            )
        )

        # New Field: Data Prevista
        self.nu_data_prevista = ft.TextField(
            label="Data Prevista",
            width=250,
            value=datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            visible=False, # Hidden by default, shown if Debt
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.date_picker_prevista)
            )
        )
        
        if not hasattr(self, 'date_picker_prevista'):
             self.date_picker_prevista = ft.DatePicker(
                on_change=lambda e: setattr(self.nu_data_prevista, 'value', e.control.value.strftime("%Y-%m-%d")) or self.page.update(),
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31)
            )
             self.page.overlay.append(self.date_picker_prevista)

        toggle_row = ft.Row([
            ft.Icon(ft.Icons.MONEY_OFF, color=ft.Colors.ORANGE_300),
            self.nu_is_pago,
            ft.Icon(ft.Icons.ATTACH_MONEY, color=ft.Colors.GREEN_300),
        ], alignment=ft.MainAxisAlignment.START)

        # Form Layout
        content = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.PERSON_ADD, size=30, color=ft.Colors.BLUE), ft.Text(title_text, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)]),
                ft.Divider(),
                # User Selection Area
                self.nu_user_dropout,
                ft.Row([self.nu_cpf, self.nu_nome]),
                
                ft.Row([self.nu_categoria, self.nu_valor]),
                ft.Row([toggle_row]),
                ft.Row([self.nu_data, self.nu_data_prevista], alignment=ft.MainAxisAlignment.START, spacing=50),
            ], tight=True, width=600),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10
        )

        # Triggers visibility check
        self._on_nu_toggle_change(None)

        bt_salvar = ft.ElevatedButton("Salvar", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, on_click=self._save_new_user)
        bt_limpar = ft.ElevatedButton("Limpar", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, on_click=self._clear_new_user_form)
        bt_cancelar = ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog())

        actions = [
            bt_salvar,
            bt_limpar,
            bt_cancelar
        ]

        self.dialog = ft.AlertDialog(
            content=content,
            actions=actions,
            modal=True,
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.open(self.dialog)

    def _build_edit_user_dialog_content(self, user_data):
        """Builds content for Editing a User."""
        self.eu_original_data = user_data
        self.eu_cpf = ft.TextField(label="CPF", value=user_data['cpf'], read_only=True, bgcolor=ft.Colors.GREY_100)
        self.eu_nome = ft.TextField(label="Nome", value=user_data['nome'], expand=True)
        self.eu_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True)

        content = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.EDIT, size=30, color=ft.Colors.BLUE), ft.Text("Edição de Usuário", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)]),
                ft.Divider(),
                ft.Row([self.eu_cpf, self.eu_nome]),
                self.eu_senha,
            ], tight=True, width=600),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10
        )

        actions = [
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, on_click=self._save_edit_user),
            ft.ElevatedButton("Limpar", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, on_click=self._clear_edit_user_form),
            ft.ElevatedButton("Cancelar", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE, on_click=lambda e: self._close_dialog())
        ]

        self.dialog = ft.AlertDialog(
            content=content,
            actions=actions,
            modal=True,
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.open(self.dialog)

    def _build_edit_transaction_dialog(self, data, transaction_type):
        """Builds content for Editing a Transaction with Dropdown."""
        self.et_original_data = data
        self.et_type = transaction_type
        
        # User Selector (Dropdown)
        users = self.controller.get_usuarios()
        opts = [ft.dropdown.Option(key=u['cpf'], text=f"{u['nome']} ({u['cpf']})") for u in users]
        
        self.et_user_dropdown = ft.Dropdown(
            label="Usuário",
            width=400,
            options=opts,
            value=data.get('cpf'),
            enable_filter=True,
            leading_icon=ft.Icons.SEARCH
        )
        self.et_selected_cpf = data.get('cpf') # Fallback if not changed

        categorias = self.controller.get_categorias()
        cat_opts = [ft.dropdown.Option(text=c['categoria']) for c in categorias]

        # Category Selector (Dropdown)
        self.et_categoria = ft.Dropdown(
            label="Categoria",
            width=300,
            value=data.get('categoria'),
            options=cat_opts
        )

        # Value Input (TextField)
        self.et_valor = ft.TextField(label="Valor", width=300, prefix_text="R$ ", value=str(data.get('valor')), keyboard_type=ft.KeyboardType.NUMBER)
        
        # Date Logic
        # Determines which date field to pre-fill based on type
        # For DEBT: 'data_divida' should be present.
        # For PAYMENT: 'data' or 'data_entrada' should be present.
        
        initial_date = data.get('data_divida') if transaction_type == "divida" else data.get('data')
        if not initial_date:
             initial_date = datetime.now().strftime("%Y-%m-%d")

        self.et_data_label = ft.Text("Data Dívida" if transaction_type == "divida" else "Data Pagamento", size=16)
        self.et_data = ft.TextField(
            label="Data Dívida" if transaction_type == "divida" else "Data Pagamento",
            width=300,
            value=initial_date,
            read_only=True,
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.et_date_picker)
            )
        )
        
        # Data Prevista (Only for Debt)
        initial_prevista = data.get('data_prevista')
        if not initial_prevista:
             initial_prevista = datetime.now().strftime("%Y-%m-%d")

        self.et_data_prevista = ft.TextField(
            label="Data Prevista",
            width=300,
            value=initial_prevista,
            read_only=True,
            visible=(transaction_type == "divida"),
            suffix=ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: self.page.open(self.et_date_picker_prevista)
            )
        )
        
        # Pickers for Edit Mode (Need distinct instances or shared)
        # Creating distinct to avoid conflicts with "New" mode dialogs if any overlap (unlikely but safe)
        self.et_date_picker = ft.DatePicker(
            on_change=lambda e: setattr(self.et_data, 'value', e.control.value.strftime("%Y-%m-%d")) or self.page.update(),
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31)
        )
        self.page.overlay.append(self.et_date_picker)
        
        self.et_date_picker_prevista = ft.DatePicker(
            on_change=lambda e: setattr(self.et_data_prevista, 'value', e.control.value.strftime("%Y-%m-%d")) or self.page.update(),
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31)
        )
        self.page.overlay.append(self.et_date_picker_prevista)
        
        title_text = "Editar Transação"
 
        # Content
        content = ft.Container(
             content=ft.Column([
                ft.Text(title_text, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ft.Divider(),
                self.et_user_dropdown, 
                self.et_categoria,
                self.et_valor,
                ft.Row([self.et_data, self.et_data_prevista], alignment=ft.MainAxisAlignment.START)
            ], tight=True, width=600),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10
        )
        
        actions = [
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, on_click=self._save_edit_transaction),
            ft.ElevatedButton("Cancelar", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE, on_click=lambda e: self._close_dialog())
        ]
        
        self.dialog = ft.AlertDialog(
            content=content,
            actions=actions,
            modal=True,
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.open(self.dialog)

    # ==========================
    # Logic / Events
    # ==========================

    def _run_action(self, e):
        # Placeholder if generic action needed
        pass

    def _on_nu_toggle_change(self, e):
        if self.nu_is_pago.value:
            self.nu_data.label = "Data Pagamento"
            self.nu_data_label.value = "Data Pagamento"
            self.nu_data_prevista.visible = False
        else:
            self.nu_data.label = "Data Dívida"
            self.nu_data_label.value = "Data Dívida"
            self.nu_data_prevista.visible = True
        self.page.update()

    def _clear_new_user_form(self, e):
        if self.is_adding_transaction and hasattr(self, 'nu_original_user_data') and self.nu_original_user_data:
            # Contextual add, don't clear user
            pass
        elif self.nu_user_dropout.visible:
            self.nu_user_dropout.value = None
        else:
            self.nu_cpf.value = ""
            self.nu_nome.value = ""
            
        self.nu_categoria.value = None
        self.nu_valor.value = ""
        self.nu_is_pago.value = False
        self.nu_data.value = datetime.now().strftime("%Y-%m-%d")
        self.nu_data_prevista.value = datetime.now().strftime("%Y-%m-%d")
        self._on_nu_toggle_change(None)
        self.page.update()

    def _save_new_user(self, e):
        # Determine Data Source
        cpf = None
        nome = None
        
        if self.nu_user_dropout.visible:
            # Transaction Mode
            if not self.nu_user_dropout.value:
                 self.show_message("Selecione um usuário", ft.Colors.RED)
                 return
            cpf = self.nu_user_dropout.value
            nome = "Transaction User" # Placeholder, controller should handle or lookup
        else:
            # New User Mode
            if not self.nu_cpf.value or not self.nu_nome.value:
                self.show_message("Preencha CPF e Nome", ft.Colors.RED)
                return
            cpf = self.nu_cpf.value
            nome = self.nu_nome.value

        if not all([self.nu_categoria.value, self.nu_valor.value]):
            self.show_message("Preencha todos os campos financeiros", ft.Colors.RED)
            return

        data = {
            "cpf": cpf,
            "nome": nome,
            "categoria": self.nu_categoria.value,
            "valor": self.nu_valor.value,
            "is_pago": self.nu_is_pago.value,
            "data": self.nu_data.value,
            "data_prevista": self.nu_data_prevista.value if (not self.nu_is_pago.value) else None
        }
        
        if self.is_adding_transaction:
            self.controller.add_transaction(data)
        else:
            self.controller.add_usuario(data)
            
        self._close_dialog()

    def _clear_edit_user_form(self, e):
        self.eu_nome.value = self.eu_original_data['nome']
        self.eu_senha.value = ""
        self.page.update()

    def _save_edit_user(self, e):
        if not self.eu_nome.value:
            self.show_message("Nome é obrigatório", ft.Colors.RED)
            return

        data = {
            "cpf": self.eu_cpf.value,
            "nome": self.eu_nome.value,
            "senha": self.eu_senha.value
        }
        self.controller.update_usuario(data)
        self._close_dialog()

    def _save_edit_transaction(self, e):
         
         # Validation
         if not self.et_valor.value:
              self.show_message("Valor é obrigatório", ft.Colors.RED)
              return
              
         data = {
             "id": self.et_original_data['id'],
             "cpf": self.et_user_dropdown.value if self.et_user_dropdown.value else self.et_original_data['cpf'],
             "categoria": self.et_categoria.value,
             "valor": self.et_valor.value,
             "data": self.et_data.value,
             # Also need to pass data_prevista if editing
             "data_prevista": self.et_data_prevista.value if hasattr(self, 'et_data_prevista') and self.et_data_prevista.visible else None
         }
         self.controller.update_transaction(data, self.et_type)
         self._close_dialog()

    def _confirm_delete_user(self, cpf):
        self.controller.delete_usuario(cpf)
        self._close_dialog()

    def _confirm_delete_transaction(self, id):
        self.controller.delete_transaction(id)
        self._close_dialog()
    
    def _close_dialog(self):
        """Fecha o diálogo aberto e atualiza as tabelas."""
        if hasattr(self, 'dialog') and self.dialog:
            self.page.close(self.dialog)
            self.dialog = None
        self.update_usuarios_table()
        self.update_dividas_table()
        self.update_entradas_table()
        self.update_reports()
        self.page.update()
    
    # ==========================
    # Filter Methods
    # ==========================
    
    def _on_filter_date_inicial_change(self, e):
        """Handler para quando a data inicial do filtro é selecionada."""
        if e.control.value:
            self.filter_data_inicial.value = e.control.value.strftime("%Y-%m-%d")
            self.page.update()
    
    def _on_filter_date_final_change(self, e):
        """Handler para quando a data final do filtro é selecionada."""
        if e.control.value:
            self.filter_data_final.value = e.control.value.strftime("%Y-%m-%d")
            self.page.update()
    
    def _clear_filters(self):
        """Limpa todos os filtros e atualiza os relatórios."""
        if hasattr(self, 'filter_user'):
            self.filter_user.value = ""
        if hasattr(self, 'filter_categoria'):
            self.filter_categoria.value = ""
        if hasattr(self, 'filter_tipo'):
            self.filter_tipo.value = ""
        if hasattr(self, 'filter_data_inicial'):
            self.filter_data_inicial.value = ""
        if hasattr(self, 'filter_data_final'):
            self.filter_data_final.value = ""
        
        self.update_reports()
        self.show_message("Filtros limpos", ft.Colors.BLUE)


    # ==========================
    # Main Layout (Bottom)
    # ==========================

    def _build_ui(self):
        """Assembles the main application layout."""
        # Header
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=40, color=ft.Colors.BLUE_600),
                    ft.Text("Painel de Gestão", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(ft.Icons.LOGOUT, tooltip="Sair", on_click=lambda e: self.controller.logout())
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )

        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            indicator_color=ft.Colors.ORANGE,
            label_color=ft.Colors.BLUE,
            unselected_label_color=ft.Colors.BLUE_200,
            divider_color=ft.Colors.TRANSPARENT,
            tabs=[
                ft.Tab(
                    text="Usuários",
                    icon=ft.Icons.PEOPLE,
                    content=self._build_usuarios_tab(),
                ),
                ft.Tab(
                    text="Dívidas",
                    icon=ft.Icons.MONEY_OFF,
                    content=self._build_dividas_tab(),
                ),
                ft.Tab(
                    text="Entradas",
                    icon=ft.Icons.ATTACH_MONEY,
                    content=self._build_entradas_tab(),
                ),
                ft.Tab(
                    text="Relatórios",
                    icon=ft.Icons.ANALYTICS,
                    content=self._build_relatorios_tab(),
                ),
            ],
            expand=True,
        )

        self.controls = [
            header,
            self.tabs
        ]
