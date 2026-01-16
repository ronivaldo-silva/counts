import flet as ft

def criar_recibo(nome: str, cpf: str, valor: str):
    """
    Gera um container Flet com o layout gráfico do recibo.
    """
    # --- 1. Variáveis de Valores ---
    empresa_nome = "CEBUDV - N. MESTRE VICENTE MARQUES"
    empresa_cnpj = "CNPJ/CPF: 02.069.705/0001-90 IE: ISENTO"
    empresa_end = "MARAPATA, 3801, Manaus - AM"
    empresa_cep = "CEP: 69088-068"
    
    titulo_doc = "Recibo"
    valor_total = valor
    
    cliente_nome = nome
    cliente_doc = cpf
    texto_valor_extenso = "Cento e Vinte Reais"
    referente_a = "pagamento total da parcela 'Associação (Mensalidade R$ 60,00 e Joia R$ 60,00)'."
    
    texto_corpo = f"Recebi de {cliente_nome}, CNPJ/CPF: {cliente_doc}, a importância de {texto_valor_extenso} referente ao {referente_a}"
    texto_legal = "Para confirmar a veracidade deste documento e da quantia paga, assino neste documento firmando o presente recibo nesta data."
    
    data_local = "Manaus (AM), 05 de janeiro de 2026"
    assinatura_nome = "CEBUDV - N. MESTRE VICENTE MARQUES"
    assinatura_doc = "CNPJ/CPF: 02.069.705/0001-90"

    logo_file = "udv_logo.png"
    assinatura_file = "recibo_assinatura.png"

    # --- 2. Variáveis de Elementos ---
    # Header
    logo_icon = ft.Row(
        [
            ft.Image(logo_file, width=300, height=100)
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )
    
    header_info = ft.Column(
        [
            ft.Text(empresa_nome, size=10, color=ft.Colors.GREY_800),
            ft.Text(empresa_cnpj, size=10, color=ft.Colors.GREY_800),
            ft.Text(empresa_end, size=10, color=ft.Colors.GREY_800),
            ft.Text(empresa_cep, size=10, color=ft.Colors.GREY_800),
        ],
        spacing=2,
    )
    
    header_row = ft.Row(
        [
            ft.Container(logo_icon, padding=ft.padding.only(right=20)),
            header_info
        ],
        alignment=ft.MainAxisAlignment.START
    )

    divisor_solido = ft.Divider(color=ft.Colors.BLACK, thickness=2)

    # Título e Valor
    titulo_ctrl = ft.Text(titulo_doc, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
    valor_ctrl = ft.Text(valor_total, size=28, weight=ft.FontWeight.W_300, color=ft.Colors.GREY_700)
    
    titulo_row = ft.Row(
        [titulo_ctrl, valor_ctrl],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Divisor tracejado
    divisor_tracejado = ft.Container(
        content=ft.Text("- - " * 40, size=10, color=ft.Colors.GREY_400, max_lines=1, overflow=ft.TextOverflow.CLIP),
        padding=ft.padding.symmetric(vertical=10)
    )

    # Corpo
    corpo_ctrl = ft.Text(texto_corpo, size=12, text_align=ft.TextAlign.JUSTIFY, color=ft.Colors.BLACK)
    legal_ctrl = ft.Text(texto_legal, size=12, text_align=ft.TextAlign.JUSTIFY, color=ft.Colors.BLACK)

    # Assinatura
    data_ctrl = ft.Text(data_local, size=12, color=ft.Colors.BLACK)
    
    # Imagem de assinatura
    assinatura_img = ft.Image(src=assinatura_file, width=250)

    assinatura_linha = ft.Container(
        height=1,
        bgcolor=ft.Colors.BLACK,
        width=300,
    )
    
    ass_nome_ctrl = ft.Text(assinatura_nome, size=10, weight=ft.FontWeight.BOLD)
    ass_doc_ctrl = ft.Text(assinatura_doc, size=10)

    assinatura_col = ft.Column(
        [
            data_ctrl,
            ft.Container(height=20), # Espaço antes da assinatura
            assinatura_linha,
            ass_nome_ctrl,
            ass_doc_ctrl
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2, 
        alignment=ft.MainAxisAlignment.CENTER
    )

    # --- 3. Layout ---
    recibo_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(height=10),
                divisor_solido,
                ft.Container(height=10),
                titulo_row,
                divisor_tracejado,
                ft.Container(height=10),
                corpo_ctrl,
                ft.Container(height=10),
                legal_ctrl,
                ft.Container(height=40),
                ft.Stack(
                    [
                        ft.Column([assinatura_img], alignment=ft.MainAxisAlignment.CENTER, bottom=60),
                        assinatura_col,
                    ],
                    alignment=ft.alignment.center,
                    height=150
                )
            ],
            spacing=5,
        ),
        width=700,
        bgcolor=ft.Colors.WHITE,
        padding=40,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLUE_GREY_100,
            offset=ft.Offset(0, 5),
        )
    )

    return recibo_container
