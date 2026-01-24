import flet as ft
import os
from dotenv import load_dotenv
from views.login_view import LoginView
from controllers.login_controller import LoginController
from database.config import engine, Base, seed_basic_data


def main(page: ft.Page):
    """
    Main entry point for the Flet application.
    Initializes the LoginView and Controller.
    """
    # Create Tables (if they don't exist)
    Base.metadata.create_all(bind=engine)

    # Seed basic data (categories, classifications, admin user)
    seed_basic_data()

    page.title = "Tesouraria Counts2"
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
    # No Render, usar a porta fornecida pela variável PORT
    load_dotenv()
    port = int(os.getenv("PORT", 8400))

    print(f"Starting Flet App on port {port}...")

    # In Flet 0.21+, ft.app blocks.
    # assets_dir="assets" serves files relative to this script directory (src/assets)
    ft.run(
        main=main,
        view=ft.AppView.WEB_BROWSER,
        port=port,
        host="0.0.0.0",
        assets_dir="assets",
    )
