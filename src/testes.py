import flet as ft
import base64
import os
from fpdf import FPDF

def main(page: ft.Page):
    """
    Ambiente de teste local para desenvolvimento de componentes.
    """
    page.title = "Ambiente de Teste - Components"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_200 

    def gerar_pdf_bytes(nome: str, cpf: str, valor: str) -> bytes:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        
        # Absolute path to assets to ensure fpdf finds them
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, "assets")
        
        # Margins & Setup
        pdf.set_margins(20, 20, 20)
        
        # --- Header ---
        # Logo
        logo_path = os.path.join(assets_dir, "udv_logo.png")
        try:
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=20, y=20, w=60)
            else:
                 print(f"Aviso: Logo não encontrado em {logo_path}")
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            pass 
            
        # Company Info
        pdf.set_xy(90, 20)
        pdf.set_font("Helvetica", size=8)
        pdf.cell(0, 5, "CEBUDV - N. MESTRE VICENTE MARQUES", ln=True)
        pdf.set_x(90)
        pdf.cell(0, 5, "CNPJ/CPF: 02.069.705/0001-90 IE: ISENTO", ln=True)
        pdf.set_x(90)
        pdf.cell(0, 5, "MARAPATA, 3801, Manaus - AM", ln=True)
        pdf.set_x(90)
        pdf.cell(0, 5, "CEP: 69088-068", ln=True)
        
        pdf.ln(10)
        
        # Line
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)
        
        # --- Title & Value ---
        pdf.set_font("Helvetica", 'B', 24)
        pdf.cell(100, 10, "Recibo", border=0)
        
        pdf.set_font("Helvetica", '', 24)
        pdf.cell(0, 10, valor, border=0, align='R', ln=True)
        
        pdf.ln(5)
        
        # Dashed Line (Simulated)
        pdf.set_font("Courier", '', 10)
        pdf.cell(0, 4, "- - " * 35, align='C', ln=True)
        pdf.ln(10)
        
        # --- Body ---
        cliente_nome = nome
        cliente_doc = cpf
        texto_valor_extenso = "Cento e Vinte Reais"
        referente_a = "pagamento total da parcela 'Associação (Mensalidade R$ 60,00 e Joia R$ 60,00)'."
        
        texto_corpo = f"Recebi de {cliente_nome}, CNPJ/CPF: {cliente_doc}, a importância de {texto_valor_extenso} referente ao {referente_a}"
        
        pdf.set_font("Helvetica", '', 12)
        pdf.multi_cell(0, 6, texto_corpo, align='J')
        
        pdf.ln(5)
        texto_legal = "Para confirmar a veracidade deste documento e da quantia paga, assino neste documento firmando o presente recibo nesta data."
        pdf.multi_cell(0, 6, texto_legal, align='J')
        
        pdf.ln(20)
        
        # --- Footer & Signature ---
        data_local = "Manaus (AM), 05 de janeiro de 2026"
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 5, data_local, align='C', ln=True)
        
        pdf.ln(5)
        
        # Signature Image
        # Save X, Y to overlapping
        sig_x = (210 - 50) / 2 # Center ~ 50mm width image
        sig_y = pdf.get_y()
        
        ass_path = os.path.join(assets_dir, "recibo_assinatura.png")
        try:
             if os.path.exists(ass_path):
                pdf.image(ass_path, x=sig_x, y=sig_y, w=50)
             else:
                 print(f"Aviso: Assinatura não encontrada em {ass_path}")

        except Exception as e:
             print(f"Erro ao carregar assinatura: {e}")
             pass
        
        pdf.ln(15) # Space for signature image
        
        # Signature Line
        pdf.set_line_width(0.2)
        pdf.line(60, pdf.get_y(), 150, pdf.get_y()) # Centered line
        pdf.ln(2)
        
        # Signature Name
        assinatura_nome = "CEBUDV - N. MESTRE VICENTE MARQUES"
        assinatura_doc = "CNPJ/CPF: 02.069.705/0001-90"
        
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 5, assinatura_nome, align='C', ln=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(0, 5, assinatura_doc, align='C', ln=True)
        
        return pdf.output() # Returns bytearray

    def criar_recibo(nome: str, cpf: str, valor: str):
        # ... (Existing Flet Receipt Code Omitted for Brevity - Keeping Logic) ...
        # (Assuming the user wants to KEEP the visual preview, I will just re-instantiate it essentially or keep the old function structure if I can. 
        # But wait, replace_file_content replaces the whole block. 
        # I must include the existing `criar_recibo` logic OR import it if I moved it.
        # But currently `testes.py` HAS the logic inline. Moving it was only for `controles.py`.
        # So I will retain `criar_recibo` implementation here for the preview.)
        
        # --- 1. Variáveis de Valores ---
        empresa_nome = "CEBUDV - N. MESTRE VICENTE MARQUES"
        # ... (Redundant variables, but keeping for standalone nature of testes.py)
        # To save tokens/complexity, I will just copy the body of creating the Flet control 
        # effectively or if I can import it? 
        # The user's request context implies `testes.py` is independent.
        # I will paste the `criar_recibo` body back.

        # --- RE-PASTING CRIAR_RECIBO BODY ---
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
        
        logo_icon = ft.Row([ft.Image("udv_logo.png", width=300, height=100)], spacing=0, alignment=ft.MainAxisAlignment.START)
        header_info = ft.Column([ft.Text(empresa_nome, size=10, color=ft.Colors.GREY_800), ft.Text(empresa_cnpj, size=10, color=ft.Colors.GREY_800), ft.Text(empresa_end, size=10, color=ft.Colors.GREY_800), ft.Text(empresa_cep, size=10, color=ft.Colors.GREY_800)], spacing=2)
        header_row = ft.Row([ft.Container(logo_icon, padding=ft.padding.only(right=20)), header_info], alignment=ft.MainAxisAlignment.START)
        divisor_solido = ft.Divider(color=ft.Colors.BLACK, thickness=2)
        titulo_ctrl = ft.Text(titulo_doc, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        valor_ctrl = ft.Text(valor_total, size=28, weight=ft.FontWeight.W_300, color=ft.Colors.GREY_700)
        titulo_row = ft.Row([titulo_ctrl, valor_ctrl], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        divisor_tracejado = ft.Container(content=ft.Text("- - " * 40, size=10, color=ft.Colors.GREY_400, max_lines=1, overflow=ft.TextOverflow.CLIP), padding=ft.padding.symmetric(vertical=10))
        corpo_ctrl = ft.Text(texto_corpo, size=12, text_align=ft.TextAlign.JUSTIFY, color=ft.Colors.BLACK)
        legal_ctrl = ft.Text(texto_legal, size=12, text_align=ft.TextAlign.JUSTIFY, color=ft.Colors.BLACK)
        data_ctrl = ft.Text(data_local, size=12, color=ft.Colors.BLACK)
        assinatura_img = ft.Image(src="recibo_assinatura.png", width=250)
        assinatura_linha = ft.Container(height=1, bgcolor=ft.Colors.BLACK, width=300)
        ass_nome_ctrl = ft.Text(assinatura_nome, size=10, weight=ft.FontWeight.BOLD)
        ass_doc_ctrl = ft.Text(assinatura_doc, size=10)
        assinatura_col = ft.Column([data_ctrl, ft.Container(height=20), assinatura_linha, ass_nome_ctrl, ass_doc_ctrl], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        
        recibo_container = ft.Container(content=ft.Column([header_row, ft.Container(height=10), divisor_solido, ft.Container(height=10), titulo_row, divisor_tracejado, ft.Container(height=10), corpo_ctrl, ft.Container(height=10), legal_ctrl, ft.Container(height=40), ft.Stack([ft.Column([assinatura_img], alignment=ft.MainAxisAlignment.CENTER, bottom=60), assinatura_col], alignment=ft.alignment.center, height=150)], spacing=5), width=700, bgcolor=ft.Colors.WHITE, padding=40, border_radius=10, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLUE_GREY_100, offset=ft.Offset(0, 5)))
        return recibo_container

    # --- Button Handler ---
    def download_pdf(e):
        nome = "ANTONIA IVANILCE CASTRO DA SILVA"
        cpf = "624.121.322-91"
        valor = "R$ 120,00"
        
        pdf_bytes = gerar_pdf_bytes(nome, cpf, valor)
        b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        page.launch_url(f"data:application/pdf;base64,{b64_pdf}")

    # Criando o recibo visual
    recibo = criar_recibo("ANTONIA IVANILCE CASTRO DA SILVA", "624.121.322-91", "R$ 120,00")

    # Botão de Download
    bt_download = ft.ElevatedButton("Baixar PDF (Economiza Storage)", icon=ft.Icons.DOWNLOAD, on_click=download_pdf, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)

    # Adicionando à página com scroll se necessário
    page.add(
        ft.Column(
            [
                ft.Text("Visualização de Recibo", size=20, weight=ft.FontWeight.BOLD),
                bt_download,
                recibo
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
