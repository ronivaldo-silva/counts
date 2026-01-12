import flet as ft

def main(page: ft.Page):
    """
    Ambiente de teste local para desenvolvimento de componentes.
    """
    page.title = "Ambiente de Teste - Components"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def criar_exemplo_card(titulo: str, subtitulo: str, icone: str):
        titulo = ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(icone, size=40),
                    title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(subtitulo),
                )
            ],
        )

        datas = ft.Row(
            [
                ft.Text("Início: 01/01/2020"),
                ft.Text("Fim: 31/12/2020"),
            ],
            alignment=ft.MainAxisAlignment.START,
            wrap=True,
        )

        botoes = ft.Row(
            [
                ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE),
                ft.IconButton(ft.Icons.RECEIPT, icon_color=ft.Colors.YELLOW),
                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED),
            ],
            alignment=ft.MainAxisAlignment.END,
        )
    
        return ft.Card(
            content=ft.Column(
                [
                    ft.Row([titulo, datas], alignment=ft.MainAxisAlignment.START, wrap=True),
                    botoes,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=800, # Largura fixa para visualizar melhor
        )

    # Criando instâncias dos componentes
    card_1 = criar_exemplo_card("Card de Teste 1", "Descrição do componente.", ft.Icons.ALBUM)
    card_2 = criar_exemplo_card("Card de Teste 2", "Outra variação.", ft.Icons.FAVORITE)

    # Componente "Container" wrapper para centralizar e dar destaque
    playground = ft.Column(
        controls=[
            ft.Text("Área de Teste de Componentes", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            card_1,
            ft.Divider(),
            card_2,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Adicionando à página
    page.add(playground)

if __name__ == "__main__":
    # Executa o app como aplicação desktop por padrão para desenvolvimento rápido
    # Se preferir ver no navegador, adicione view=ft.AppView.WEB_BROWSER
    ft.app(target=main)
