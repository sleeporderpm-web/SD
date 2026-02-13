from typing import Dict
from fpdf import FPDF
from datetime import datetime


def build_report(data: Dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Sleep Analysis Report", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ln=1)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Patient Details", ln=1)
    pdf.set_font("Arial", size=12)
    for k in ["user_email", "phone", "age", "gender", "occupation", "bmi_category"]:
        v = str(data.get(k, ""))
        pdf.cell(0, 8, f"{k.replace('_', ' ').title()}: {v}", ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Vitals", ln=1)
    pdf.set_font("Arial", size=12)
    for k in ["blood_pressure", "heart_rate", "sleep_duration", "stress", "snoring_frequency", "working_hours"]:
        v = str(data.get(k, ""))
        pdf.cell(0, 8, f"{k.replace('_', ' ').title()}: {v}", ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Diagnosis", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, str(data.get("diagnosis", "")))
    pdf.ln(4)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 6, "This report is for informational purposes only and does not constitute medical advice. Consult a qualified healthcare professional for diagnosis and treatment.")
    return pdf.output(dest="S").encode("latin1")
