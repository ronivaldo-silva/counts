import flet as ft

def main(page: ft.Page):
    page.title = "Exemplo de uso do CameraControl"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    logo = ft.Column(
            controls = [
                ft.Container(
                    bgcolor=ft.Colors.BLUE_200,
                    height=100,
                    width=100,
                ),
            ],
            alignment = ft.MainAxisAlignment.CENTER
    )

    top = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    logo,
                    ft.Divider(height=4, color=ft.Colors.AMBER_400, thickness=2),
                    ft.Text("Login com CPF", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                    ft.Divider(height=4, color=ft.Colors.AMBER_400, thickness=2),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    cpf_input = ft.TextField(
            label="CPF",
            hint_text="Digite seu CPF",
            max_length=11,
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=lambda e: btn_go.on_click(e),
            autofocus=True,
        )

    btn_go = ft.IconButton(
            icon=ft.Icons.DONE,
            bgcolor=ft.Colors.BLUE_400,
            icon_color=ft.Colors.WHITE,
            on_click=lambda e: procurar_usuario(e.data),
        )

    pw_input = ft.TextField(
            label="SENHA",
            hint_text="Digite sua SENHA",
            max_length=11,
            width=300,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            on_submit=lambda e: btn_pw_go.on_click(e),
            autofocus=False,
            disabled=True
        )

    btn_pw_go = ft.IconButton(
        icon=ft.Icons.DONE,
        bgcolor=ft.Colors.BLUE_400,
        icon_color=ft.Colors.WHITE,
        on_click=lambda e: salvar_senha(e.data),
        disabled=True
    )

    start_form = ft.Row([    
        cpf_input,
        btn_go
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=-10
    )

    senha_form = ft.Row([    
        pw_input,
        btn_pw_go
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=-10
    )

    def procurar_usuario(data):
        usuario = {'id':1, 'nome':'Teste','senha': data or None}
        if data:
            pw_input.disabled = False
            btn_pw_go.disabled = False
            pw_input.focus()
            print(f'Olá {usuario}. Insira sua senha')
            return usuario
        else:
            print('nada')
            return None
    
    def salvar_senha(data):
        if data:
            print(f'senha {data.get('nome')} salva' )
            return data
        else:
            print('nada')
            return None

    page.add(top,start_form, senha_form)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8400)
