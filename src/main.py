import flet as ft
import uvicorn
import os
from fastapi import FastAPI, Response
from views.login_view import LoginView
from controllers.login_controller import LoginController
from controllers.geral_controller import gerar_pdf_bytes
from database.config import engine, Base, seed_basic_data

# Initialize FastAPI for backend endpoints (e.g. PDF Download)
app = FastAPI()


@app.get("/download/recibo")
def download_recibo(
    nome: str, cpf: str, valor: str, categoria: str = "Associação", data: str = None
):
    """
    Endpoint to generate and download the receipt PDF.
    Args received from query parameters.

    Query params:
        nome: Nome do cliente
        cpf: CPF do cliente
        valor: Valor formatado (ex: R$ 120,00)
        categoria: Categoria da transação (opcional, padrão: Associação)
        data: Data da transação (opcional, padrão: data atual)
    """
    try:
        pdf_bytes = gerar_pdf_bytes(nome, cpf, valor, categoria, data)
        headers = {"Content-Disposition": 'attachment; filename="recibo.pdf"'}
        return Response(
            content=bytes(pdf_bytes), headers=headers, media_type="application/pdf"
        )
    except Exception as e:
        return Response(content=f"Error generating PDF: {str(e)}", status_code=500)


def main(page: ft.Page):
    """
    Main entry point for the Flet application.
    Initializes the LoginView and Controller.
    """
    # Create Tables (if they don't exist)
    Base.metadata.create_all(bind=engine)

    # Seed basic data (categories, classifications, admin user)
    seed_basic_data()

    page.title = "Sistema Counts2"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Initialize Controller
    controller = LoginController(page)

    # Initialize View with Controller
    view = LoginView(page, controller)

    # Link View back to Controller
    controller.set_view(view)

    # Add View to Page
    page.add(view)


# Mount the Flet App on the FastAPI instance
# assets_dir="assets" is assuming src/assets exists relative to this file
app.mount("/", ft.app(main, export_asgi_app=True, assets_dir="assets"))

if __name__ == "__main__":
    # No Render/Cloud Run, usar a porta fornecida pela variável PORT
    # Em desenvolvimento local, usar 8500 como padrão
    port = int(os.environ.get("PORT", 8400))
    host = (
        "0.0.0.0"  # permite aceitar conexões de qualquer origem (necessário no Render)
    )

    uvicorn.run(app, host=host, port=port)
