from time import sleep
import flet as ft
from controllers.login_controller import LoginController

class LoginView(ft.Column):
    """
    View for the Login Screen.
    Displays CPF and Password inputs and handles user interaction.
    """
    def __init__(self, page: ft.Page, controller: LoginController):
        super().__init__()
        self.page = page
        self.controller: LoginController = controller
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # UI Components
        self.cpf_input = ft.TextField(
            label="CPF",
            hint_text="Digite seu CPF",
            max_length=11,
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: self.controller.handle_cpf_submit(e),
            on_tap_outside=lambda e: self.controller.handle_cpf_submit(e),
            # on_change=lambda e: self.controller.handle_cpf_change(e),
            autofocus=True,
        )
        
        self.pw_input = ft.TextField(
            label="SENHA",
            hint_text="Digite sua SENHA",
            max_length=20,
            width=300,
            password=True,
            can_reveal_password=True,
            on_submit=lambda e: self.controller.handle_password_submit(e),
            disabled=True,
        )
        
        self.msg_operation = ft.Text(value="", color=ft.Colors.RED_300, size=16, weight=ft.FontWeight.BOLD)

        # Build UI
        self._build_ui()

    # ==========================
    # Action Handlers
    # ==========================

    def login_action(self, e):
        """Triggers the login process based on current input state."""
        # If password field is enabled and has value, try to login
        if not self.pw_input.disabled and self.pw_input.value:
            self.controller.handle_password_submit(e)
        # If only CPF is entered so far, try to find user
        elif self.cpf_input.value:
            self.controller.handle_cpf_submit(e)
        else:
            self.show_message("Digite o CPF", ft.Colors.RED)

    def clear_action(self, e):
        """Resets the login form."""
        self.cpf_input.value = ""
        self.pw_input.value = ""
        self.pw_input.disabled = True
        self.msg_operation.value = ""
        self.cpf_input.focus()
        self.page.update()

    # ==========================
    # UI Helpers
    # ==========================

    def show_message(self, message: str, color: str = ft.Colors.RED):
        """Displays a message to the user."""
        self.msg_operation.value = message
        self.msg_operation.color = color
        self.msg_operation.update()

    def enable_password_field(self):
        """Enables the password input field."""
        self.pw_input.disabled = False
        self.pw_input.update()
        sleep(0.1)
        self.pw_input.focus()

    def show_cadastro_dialog(self, titulo: str, nome: str, cpf: str):
        """Opens a dialog for password creation."""
        new_password_input = ft.TextField(
            label="Nova Senha",
            autofocus=True,
            password=True
        )

        def on_done_click(e):
            self.controller.handle_cadastro_submit(new_password_input.value)
            self.page.close(dialog)

        dialog = ft.AlertDialog(
            title=ft.Text(titulo),
            modal=True,
            content=ft.Column(
                [
                    ft.TextField(label='Nome', value=nome, disabled=True),
                    ft.TextField(label='CPF', value=cpf, keyboard_type=ft.KeyboardType.NUMBER, disabled=True),
                    new_password_input,
                ],
                spacing=10,
                height=200,
            ),
            actions=[
                ft.IconButton(icon=ft.Icons.CANCEL, on_click=lambda e: self.page.close(dialog)),
                ft.IconButton(icon=ft.Icons.DONE, on_click=on_done_click),
            ],
        )
        self.page.open(dialog)
        self.page.update()

    # ==========================
    # Layout Builder
    # ==========================

    def _build_ui(self):
        """Assembles the main layout."""
        logo = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="udv_logo.png",
                        width=400,
                        height=200,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    height=200,
                    width=400,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        top = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        logo,
                        ft.Divider(height=4, color=ft.Colors.AMBER_400, thickness=2),
                        ft.Column(
                            [
                                ft.Text("Login com CPF", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600, text_align=ft.TextAlign.CENTER),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Divider(height=4, color=ft.Colors.AMBER_400, thickness=2),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        start_form = ft.Row(
            [self.cpf_input],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        senha_form = ft.Row(
            [self.pw_input],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        btn_actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.DONE,
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.GREEN_300,
                    hover_color=ft.Colors.GREEN_400,
                    tooltip="Enviar",
                    on_click=lambda e: self.login_action(e),
                ),
                ft.IconButton(
                    icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.ORANGE_300,
                    hover_color=ft.Colors.ORANGE_400,
                    tooltip="Limpar",
                    on_click=lambda e: self.clear_action(e),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        self.controls = [
            top,
            start_form,
            senha_form,
            btn_actions,
            self.msg_operation
        ]
