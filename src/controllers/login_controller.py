from time import sleep
from models.dto_form_dados import DTO_FormDados
from database.config import SessionLocal
from repositories.user_repository import UsuarioRepository


class LoginController:
    """
    Controller for the Login View.
    Handles CPF validation, user lookup, and password verification using PostgreSQL.
    """

    def __init__(self, page):
        self.page = page
        self.view = None  # Will be set after view initialization
        self.model = DTO_FormDados()
        self.db = SessionLocal()
        self.user_repo = UsuarioRepository(self.db)

    def set_view(self, view):
        """Sets the reference to the View."""
        self.view = view

    # ==========================
    # Event Handlers
    # ==========================

    def handle_cpf_submit(self, e):
        """
        Handles the submission of the CPF field.
        Checks if the ID exists and routes to Password entry or Password Creation.
        """
        cpf = self.view.cpf_input.value
        if not cpf:
            return

        self.model.cpf = cpf

        # Real DB Lookup
        user = self.user_repo.get_by_cpf(cpf)

        if not user:
            # Case 1: CPF does not exist in DB
            # For this app flow, we might want to AUTO-REGISTER new users implicitly via flow?
            # Or show error? The requirement implied "Add User" is done inside Gestao.
            # But "Scenario 3" in old code implied "User not found".
            self.view.show_message(
                "CPF não cadastrado.", "red"
            )  # Using string "red" or import colors if needed.
            return

        self.model.id = user.id
        self.model.nome = user.nome

        if user.senha:
            # Case 2: CPF exists AND has password
            self.model.senha = (
                user.senha
            )  # Store hashed pass (or plain for now) to compare
            self.view.show_message(f"Olá {self.model.nome}. Insira sua senha", "green")
            self.view.enable_password_field()
        else:
            # Case 3: CPF exists but NO password set (e.g. created by Admin)
            self.view.show_cadastro_dialog(
                "Cadastro de Senha", self.model.nome, self.model.cpf
            )

    def handle_cpf_change(self, e):
        # Placeholder for real-time validation if needed
        pass

    def handle_password_submit(self, e):
        """
        Handles the submission of the Password field.
        Verifies credentials and navigates to the appropriate screen.
        """
        senha = self.view.pw_input.value

        # Validation
        if senha:
            # Check if password matches
            # In real production: bcrypt.checkpw(senha.encode(), self.model.senha.encode())
            if self.model.senha and senha != self.model.senha:
                self.view.show_message("Senha incorreta", "red")
                return

            self.model.senha = senha  # Update model with accepted pass
            self.view.show_message(
                f"Login realizado com sucesso! Bem-vindo {self.model.nome}", "green"
            )
            sleep(1)

            self._navigate_after_login()
        else:
            self.view.show_message("Senha inválida", "red")

    def handle_cadastro_submit(self, senha):
        """Handles the creation of a new password for a user without one."""
        if senha:
            # Update DB
            self.user_repo.update(self.model.cpf, senha=senha)
            self.model.senha = senha

            self.view.show_message(
                f"Senha cadastrada com sucesso para {self.model.nome}", "green"
            )
            self.view.enable_password_field()
        else:
            self.view.show_message("A senha não pode ser vazia", "red")

    # ==========================
    # Logic / Helpers
    # ==========================

    def _navigate_after_login(self):
        """Determines where to navigate based on user role."""
        # Check for Admin
        if self.model.cpf == "00000000000":
            from views.gestao_view import GestaoView
            from controllers.gestao_controller import GestaoController

            self.page.clean()
            # Pass session to next controller? Or let it create its own.
            # Usually better to pass or have dependency injection.
            # For simplicity, GestaoController creates its own session.
            gestao_controller = GestaoController(self.page)
            gestao_view = GestaoView(gestao_controller)
            gestao_controller.set_view(gestao_view)
            self.page.add(gestao_view)
            self.page.update()
            self.db.close()
            return

        # Navigate to Dashboard (User)
        from views.dashboard_view import DashboardView
        from controllers.dashboard_controller import DashboardController

        self.page.clean()

        # Init Dashboard Controller
        dashboard_controller = DashboardController(self.page)

        # Init Dashboard View
        dashboard_view = DashboardView(
            self.page, dashboard_controller, self.model.nome, self.model.id
        )

        dashboard_controller.set_view(dashboard_view)

        self.page.add(dashboard_view)
        self.page.update()
        self.db.close()
