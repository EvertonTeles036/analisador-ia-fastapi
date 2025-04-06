from fpdf import FPDF
import textwrap

def generate_report(transcription, analysis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Relatório de Atendimento com IA", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Transcrição:\n{textwrap.fill(transcription, 100)}")
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Análise:")
    for k, v in analysis.items():
        if isinstance(v, list):
            pdf.multi_cell(0, 10, f"{k.capitalize()}: {', '.join(v)}")
        else:
            pdf.multi_cell(0, 10, f"{k.capitalize()}: {v}")
    output_path = "/mnt/data/relatorio_atendimento.pdf"
    pdf.output(output_path)
    return output_path