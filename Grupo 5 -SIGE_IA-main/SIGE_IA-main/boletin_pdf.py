from fpdf import FPDF
from gestor_datos import cargar_estudiantes
from tkinter import filedialog

def generar_boletin(nombre_estudiante):
    estudiantes = cargar_estudiantes()
    estudiante = next((e for e in estudiantes if e["nombre"].lower() == nombre_estudiante.lower()), None)
    
    if not estudiante:
        print("Estudiante no encontrado.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Boletín Académico", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nombre: {estudiante['nombre']}", ln=True)
    pdf.cell(200, 10, txt=f"Promedio: {estudiante['promedio']}", ln=True)
    pdf.cell(200, 10, txt=f"Estado final: {estudiante['estado_final']}", ln=True)
    pdf.cell(200, 10, txt=f"Medalla: {estudiante.get('medalla', '❔')}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Notas por materia:", ln=True)
    pdf.set_font("Arial", size=11)

    for materia, nota in estudiante["materias"].items():
        pdf.cell(200, 8, txt=f"{materia}: {nota}", ln=True)

    ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if ruta:
        pdf.output(ruta)
        print(f"✅ PDF guardado en {ruta}")

