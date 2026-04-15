from fpdf import FPDF

class Certificate(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CERTIFICADO DE PARTICIPAÇÃO', 0, 1, 'C')
        self.ln(5)

pdf = Certificate()
pdf.add_page()
pdf.set_font("Arial", size=12)

# --- Cabeçalho e Identificação ---
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "ContentFlow: Planejador de Redes Sociais", 0, 1, 'C')
pdf.ln(10)

pdf.set_font("Arial", size=12)
text = (
    "Certificamos que Inguerson Pereira da Silva Gomes participou com êxito do treinamento "
    "estratégico de marketing e planejamento de conteúdo, utilizando a metodologia ContentFlow, "
    "concluído em 26 de janeiro de 2026."
)
pdf.multi_cell(0, 10, text, align='C')
pdf.ln(10)

# --- Critérios de Validação ---
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Critérios de Validação e Conteúdo Programático:", 0, 1, 'L')
pdf.set_font("Arial", size=11)
pdf.cell(0, 8, "- Estratégia de Mix de Conteúdo (Promoção, Conexão e Educação)", 0, 1, 'L')
pdf.cell(0, 8, "- Aplicação de Gatilhos Mentais e Modelos de Engajamento", 0, 1, 'L')
pdf.cell(0, 8, "- Criação de Autoridade através de Conteúdo Educativo", 0, 1, 'L')
pdf.cell(0, 8, "- Carga Horária Total: 20 Horas", 0, 1, 'L')
pdf.cell(0, 8, f"- ID de Autenticidade: 43081769472299", 0, 1, 'L')
pdf.ln(20)

# --- Rodapé / Assinatura ---
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.set_font("Arial", 'I', 10)
pdf.cell(0, 10, "Assinatura da Coordenação ContentFlow", 0, 1, 'C')

pdf.output("Certificado_ContentFlow_Inguerson.pdf")
