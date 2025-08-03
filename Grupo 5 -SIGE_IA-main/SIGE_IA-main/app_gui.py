import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring
from gestor_datos import cargar_estudiantes, guardar_estudiantes
from motor_reglas import generar_recomendaciones
from boletin_pdf import generar_boletin
from predictor import predecir_estado, entrenar_modelo
from estado_emocional import evaluar_emocional
from simulador import simular_mejora
from exportar_pdf import exportar_pdf
from exportar_txt import exportar_estado_final
from patrones_fracaso import analizar_fracaso
from leer_imagen_notas import leer_imagen
from registro_ocr import registrar_estudiante_con_ocr
import webbrowser

def configurar_estilo():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f5faff")
    style.configure("TButton", background="#4e2d37", foreground="white", font=("Segoe UI", 10, "bold"))
    style.configure("TLabel", background="#f5faff", font=("Segoe UI", 10))
    style.configure("TNotebook", background="#f5faff")
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"))

def login_usuario():
    global usuario_actual
    usuario = askstring("Inicio de sesión", "Ingresa tu nombre si eres estudiante o escribe 'profesor':")
    if usuario is None:
        root.destroy()
    elif usuario.lower() == "profesor":
        return "profesor"
    else:
        estudiantes = cargar_estudiantes()
        nombres = [e["nombre"].lower() for e in estudiantes]
        if usuario.lower() in nombres:
            usuario_actual = usuario
            return "estudiante"
        else:
            messagebox.showerror("Error", "Estudiante no encontrado. Verifica el nombre.")
            return login_usuario()


def registrar_estudiante_manual():
    def guardar():
        nombre = entry_nombre.get()
        promedio = float(entry_promedio.get())
        materias_texto = entry_materias.get("1.0", tk.END).strip()
        materias = {}
        for linea in materias_texto.splitlines():
            if ':' in linea:
                materia, nota = linea.split(':')
                materias[materia.strip()] = float(nota.strip())
        materias_reprobadas = [m for m, n in materias.items() if n < 7]
        estado_final = "Aprobado" if promedio >= 7 and not materias_reprobadas else "Reprobado"
        estudiante = {
            "nombre": nombre,
            "promedio": promedio,
            "materias": materias,
            "materias_reprobadas": materias_reprobadas,
            "estado_final": estado_final,
            "medalla": asignar_medalla({"promedio": promedio, "materias_reprobadas": materias_reprobadas})
        }
        estudiantes = cargar_estudiantes()
        estudiantes.append(estudiante)
        guardar_estudiantes(estudiantes)
        messagebox.showinfo("Éxito", "Estudiante registrado correctamente")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Registrar estudiante")
    top.geometry("400x400")
    ttk.Label(top, text="Nombre:").pack(pady=5)
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack()
    ttk.Label(top, text="Promedio general:").pack(pady=5)
    entry_promedio = ttk.Entry(top)
    entry_promedio.pack()
    ttk.Label(top, text="Materias (ej: Matematicas: 8.5)").pack(pady=5)
    entry_materias = tk.Text(top, height=10)
    entry_materias.pack()
    ttk.Button(top, text="Guardar", command=guardar).pack(pady=10)

def registrar_ocr():
    def subir():
        nombre = entry_nombre.get()
        ruta = filedialog.askopenfilename(title="Selecciona la imagen de notas")
        if ruta:
            registrar_estudiante_con_ocr(nombre, ruta)
            messagebox.showinfo("OCR", "Estudiante registrado con OCR correctamente")
            top.destroy()

    top = tk.Toplevel(root)
    top.title("Registrar desde imagen (OCR)")
    top.geometry("350x150")
    ttk.Label(top, text="Nombre del estudiante:").pack(pady=5)
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack()
    ttk.Button(top, text="Subir imagen y registrar", command=subir).pack(pady=10)

def ver_estudiantes():
    estudiantes = sorted(cargar_estudiantes(), key=lambda e: e['nombre'].lower())
    if not estudiantes:
        messagebox.showinfo("Estudiantes", "No hay estudiantes registrados")
        return
    top = tk.Toplevel(root)
    top.title("Estudiantes")
    lista = tk.Listbox(top)
    lista.pack(fill="both", expand=True)

    for e in estudiantes:
        if rol == "estudiante" and e["nombre"].lower() != usuario_actual.lower():
            continue
        lista.insert(tk.END, e['nombre'])

    def detalle(event):
        idx = lista.curselection()[0]
        estudiante = [e for e in estudiantes if e["nombre"] == lista.get(idx)][0]
        d = tk.Toplevel(top)
        d.title(estudiante["nombre"])
        tk.Label(d, text=f"Promedio: {estudiante['promedio']}").pack()
        tk.Label(d, text=f"Estado: {estudiante['estado_final']}").pack()
        tk.Label(d, text=f"Medalla: {estudiante.get('medalla', '❔')}").pack()
        tk.Label(d, text="Materias:").pack()
        for m, n in estudiante["materias"].items():
            tk.Label(d, text=f"{m}: {n}").pack()
        ttk.Button(d, text="Evaluar emocional", command=lambda: mostrar_emocional_personalizado(d)).pack(pady=5)
        ttk.Button(d, text="Generar PDF", command=lambda: generar_pdf_individual(estudiante['nombre'])).pack(pady=5)
        if rol == "profesor":
            ttk.Button(d, text="Editar", command=lambda: editar_estudiante(estudiante)).pack(pady=5)

    lista.bind("<<ListboxSelect>>", detalle)

def mostrar_emocional_personalizado(parent):
    preguntas = [
        ("¿Te sientes motivado para estudiar esta semana?", ["Sí, mucho", "Un poco", "No"]),
        ("¿Has cumplido con tus tareas?", ["Sí todas", "Algunas", "Ninguna"]),
        ("¿Duermes bien y te concentras al estudiar?", ["Sí", "A veces", "No"]),
    ]
    respuestas = {}
    def evaluar():
        respuestas_claras = ""
        for i, (preg, _) in enumerate(preguntas):
            seleccion = variables[i].get()
            respuestas[preg] = seleccion
            respuestas_claras += f"{preg}\n→ {seleccion}\n\n"
        messagebox.showinfo("Resultado Emocional", respuestas_claras)
        top.destroy()
    top = tk.Toplevel(parent)
    top.title("Evaluación emocional personalizada")
    variables = []
    for i, (preg, opciones) in enumerate(preguntas):
        ttk.Label(top, text=preg).pack(anchor="w", padx=10, pady=2)
        var = tk.StringVar(value=opciones[0])
        variables.append(var)
        for opcion in opciones:
            ttk.Radiobutton(top, text=opcion, variable=var, value=opcion).pack(anchor="w", padx=20)
    ttk.Button(top, text="Evaluar", command=evaluar).pack(pady=10)

def generar_pdf_individual(nombre):
    generar_boletin(nombre)
    messagebox.showinfo("PDF", f"Boletín PDF generado para {nombre}")

def editar_estudiante(estudiante):
    top = tk.Toplevel(root)
    top.title("Editar")
    ttk.Label(top, text="Promedio:").pack()
    e_prom = ttk.Entry(top)
    e_prom.insert(0, str(estudiante["promedio"]))
    e_prom.pack()
    ttk.Label(top, text="Materias (formato: Mat:Nota)").pack()
    t_mat = tk.Text(top, height=8)
    for m, n in estudiante["materias"].items():
        t_mat.insert(tk.END, f"{m}: {n}\n")
    t_mat.pack()
    def guardar():
        promedio = float(e_prom.get())
        materias = {}
        for linea in t_mat.get("1.0", tk.END).strip().split("\n"):
            if ":" in linea:
                m, n = linea.split(":")
                materias[m.strip()] = float(n.strip())
        estudiante["promedio"] = promedio
        estudiante["materias"] = materias
        estudiante["materias_reprobadas"] = [m for m, n in materias.items() if n < 7]
        estudiante["estado_final"] = "Aprobado" if promedio >= 7 and not estudiante["materias_reprobadas"] else "Reprobado"
        estudiante["medalla"] = asignar_medalla(estudiante)
        estudiantes = cargar_estudiantes()
        for i, e in enumerate(estudiantes):
            if e["nombre"] == estudiante["nombre"]:
                estudiantes[i] = estudiante
        guardar_estudiantes(estudiantes)
        messagebox.showinfo("Guardado", "Estudiante actualizado.")
        top.destroy()
    ttk.Button(top, text="Guardar cambios", command=guardar).pack(pady=10)

def asignar_medalla(est):
    prom = est["promedio"]
    reprobadas = len(est["materias_reprobadas"])
    if prom >= 9:
        return "🥇 Excelencia"
    elif prom >= 8 and reprobadas == 0:
        return "🥈 Avance"
    elif prom >= 7 and reprobadas == 1:
        return "🥉 Esfuerzo"
    else:
        return " Sin medalla"

def abrir_chat():
    def responder():
        p = entrada.get()
        if not p.strip(): return
        historial.insert(tk.END, f"👤 Tú: {p}\n")
        entrada.delete(0, tk.END)
        if "recomiendas" in p.lower():
            r = " Te recomiendo Khan Academy y Python: https://www.w3schools.com/python/"
        elif "me siento mal" in p.lower():
            r = " Intenta pausas activas o visita: https://www.psicologiaymente.com/clinica/consejos-superar-desmotivacion"
        elif "aprender ia" in p.lower():
            r = " Mira este curso gratuito: https://developers.google.com/machine-learning/crash-course"
        else:
            r = "Puedes preguntarme sobre IA, motivación, recursos educativos..."
        historial.insert(tk.END, f" Tutor IA: {r}\n\n")
        historial.see(tk.END)

    chat = tk.Toplevel(root)
    chat.title("Tutor Educativo IA")
    historial = tk.Text(chat)
    historial.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    frame = ttk.Frame(chat)
    frame.pack(fill=tk.X)
    entrada = ttk.Entry(frame, width=70)
    entrada.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Button(frame, text="Enviar", command=responder).pack(side=tk.RIGHT)
    historial.insert(tk.END, " Hola, soy tu tutor inteligente. Pregúntame lo que necesites.\n")

def mostrar_estado_final():
    estudiantes = cargar_estudiantes()
    texto = "\n".join(f"{e['nombre']}: {e['estado_final']}" for e in estudiantes)
    messagebox.showinfo("Estado Final", texto)

def exportar_estado():
    exportar_estado_final()
    messagebox.showinfo("TXT Exportado", "Estado final exportado correctamente")

def predecir():
    def calcular():
        try:
            promedio = float(entry.get())
            estado = predecir_estado(promedio)
            messagebox.showinfo("Predicción", f"Probabilidad de aprobar: {estado}")
        except:
            messagebox.showerror("Error", "Ingrese un promedio válido")
    top = tk.Toplevel(root)
    top.title("Predicción de aprobación")
    ttk.Label(top, text="Ingrese promedio estimado:").pack(pady=5)
    entry = ttk.Entry(top)
    entry.pack()
    ttk.Button(top, text="Predecir", command=calcular).pack(pady=10)

def generar_boletin_gui():
    def crear():
        nombre = entry_nombre.get()
        generar_boletin(nombre)
        messagebox.showinfo("Boletín", f"Boletín generado para {nombre}")
        top.destroy()
    top = tk.Toplevel(root)
    top.title("Generar boletín")
    ttk.Label(top, text="Nombre del estudiante:").pack(pady=5)
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack()
    ttk.Button(top, text="Generar", command=crear).pack(pady=10)

def reentrenar_modelo_gui():
    entrenar_modelo()
    messagebox.showinfo("Entrenamiento", " El modelo ha sido reentrenado correctamente.")

# Inicialización
root = tk.Tk()
root.title("SIGE-IA - Sistema Inteligente de Gestión Estudiantil")
root.geometry("750x500")
configurar_estilo()
rol = login_usuario()
entrenar_modelo()
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)
frame_registro = ttk.Frame(notebook)
frame_analisis = ttk.Frame(notebook)
frame_simulador = ttk.Frame(notebook)
frame_docente = ttk.Frame(notebook)
frame_exportar = ttk.Frame(notebook)
frame_tutor = ttk.Frame(notebook)
notebook.add(frame_registro, text=" Registro")
notebook.add(frame_analisis, text=" Análisis")
notebook.add(frame_simulador, text="Simulador")
notebook.add(frame_docente, text=" Docente")
notebook.add(frame_exportar, text=" Exportar")
notebook.add(frame_tutor, text=" Tutor IA")

# Botones por pestaña
ttk.Button(frame_registro, text="Registrar Manualmente", command=registrar_estudiante_manual).pack(pady=10)
ttk.Button(frame_registro, text="Registrar desde Imagen (OCR)", command=registrar_ocr).pack(pady=10)
ttk.Button(frame_registro, text="Ver Estudiantes", command=ver_estudiantes).pack(pady=10)
ttk.Button(frame_analisis, text="Ver Estado Final", command=mostrar_estado_final).pack(pady=10)
ttk.Button(frame_analisis, text="Generar Boletín PDF", command=generar_boletin_gui).pack(pady=10)
ttk.Button(frame_analisis, text="Predecir Aprobación IA", command=predecir).pack(pady=10)
ttk.Button(frame_analisis, text="Analizar Fracaso (IA)", command=analizar_fracaso).pack(pady=10)
ttk.Button(frame_tutor, text="Chat IA Educativo", command=abrir_chat).pack(pady=20)

if rol == "profesor":
    ttk.Button(frame_simulador, text="Simular Mejora y Plan", command=simular_mejora).pack(pady=20)
    ttk.Button(frame_docente, text="Exportar Estado Final (TXT)", command=exportar_estado).pack(pady=10)
    ttk.Button(frame_docente, text="Exportar Recomendaciones (PDF)", command=exportar_pdf).pack(pady=10)
    ttk.Button(frame_docente, text=" Reentrenar Modelo IA", command=reentrenar_modelo_gui).pack(pady=10)
else:
    ttk.Label(frame_simulador, text="(Acceso solo para profesores)").pack(pady=30)
    ttk.Label(frame_docente, text="(Acceso solo para profesores)").pack(pady=30)

root.mainloop()

