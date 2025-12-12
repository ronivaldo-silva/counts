import flet as ft
from views.login_view import LoginView
from controllers.login_controller import LoginController
from database.config import engine, Base, seed_basic_data

def main(page: ft.Page):
    """
    Main entry point for the application.
    Initializes the LoginView and Controller.
    """
    # Create Tables (if they don't exist)
    Base.metadata.create_all(bind=engine)
    
    # Seed basic data (categories, classifications, admin user)
    seed_basic_data()

    page.title = "Sistema de Gestão Financeira"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Initialize Controller
    controller = LoginController(page)
    
    # Initialize View with Controller
    view = LoginView(page, controller)
    
    # Link View back to Controller
    controller.set_view(view)
    
    # Add View to Page
    page.add(view)

if __name__ == "__main__":
    import os
    
    # No Render, usar a porta fornecida pela variável PORT
    # Em desenvolvimento local, usar 8400 como padrão
    port = int(os.getenv("PORT", 8400))
    
    # Para deploy web, usar WEB_APPLICATION ao invés de WEB_BROWSER
    # host="0.0.0.0" permite aceitar conexões de qualquer origem (necessário no Render)
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP_WEB,
        port=port,
        host="0.0.0.0"
    )
