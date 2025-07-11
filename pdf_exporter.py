# pdf_exporter.py
from fpdf import FPDF
from flask import send_file
import io

def processed_text(text):
    subscript_dict = {
        '₀': '0', '₁': '1', '₂': '2', '₃': '3',
        '₄': '4', '₅': '5', '₆': '6', '₇': '7',
        '₈': '8', '₉': '9'
    }
    for sub, normal in subscript_dict.items():
        text = text.replace(sub, normal)
    return text.encode('ascii', 'ignore').decode()# converted into ascii, non-ascii are ignored and then converted again to string

def export_to_pdf(data):
    summary = processed_text(data.get("summary", ""))
    questions = processed_text(data.get("questions", ""))
    concepts = processed_text(data.get("concepts", ""))
    filename = processed_text(data.get("filename", "StudyGuide"))

    pdf = FPDF()
    pdf.add_page()

    # for heading
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, "Study Guide", ln=True)

    # summary
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf.ln(5)

    # key concepts
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Key Concepts:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, concepts)
    pdf.ln(5)

    # practice questions
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Practice Questions:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, questions)

    pdf_data = pdf.output(dest='S').encode('latin-1') # file is coverted into string then in bytes

    return send_file(
        io.BytesIO(pdf_data),
        as_attachment=True, # file can be downloaded
        download_name=f"{filename}.pdf",
        mimetype="application/pdf"
    )
