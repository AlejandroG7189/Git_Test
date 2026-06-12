import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os
import subprocess 
import sys

# =============================================================================
# CONTROL DE AUDIO (SFX) Y MULTIMEDIA
# =============================================================================
try:
    import pygame
    pygame.mixer.init()
    AUDIO_HABILITADO = True
except ImportError:
    AUDIO_HABILITADO = False
    print("AVISO: La librería 'pygame' no está instalada. Los efectos de sonido están desactivados.")
    print("Para habilitarlos, ejecuta en tu terminal: pip install pygame")

def resource_path(relative_path):
    """ Gestiona rutas para archivos internos si compilas en un .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def play_sfx(filename):
    """ Reproduce un archivo de audio .ogg en segundo plano """
    if AUDIO_HABILITADO:
        try:
            ruta_audio = resource_path(filename)
            if os.path.exists(ruta_audio):
                sonido = pygame.mixer.Sound(ruta_audio)
                sonido.play()
        except Exception as e:
            print(f"Error reproduciendo {filename}: {e}")

# =============================================================================
# CONTROL DE ACCESO JERÁRQUICO
# =============================================================================
USUARIOS_SISTEMA = {
    "admin": {"password": "1234", "rol": 3, "cargo": "Creador del Proyecto"},
    "supervisor": {"password": "4567", "rol": 2, "cargo": "Supervisor / Editor"},
    "operador": {"password": "7890", "rol": 1, "cargo": "Operador / Consulta"}
}

usuario_actual = None  

# --- IMPORTACIONES PARA REPORTE PDF ---
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def verificar_permiso(nivel_requerido):
    global usuario_actual
    if not usuario_actual:
        return False
    return usuario_actual["rol"] >= nivel_requerido

# =============================================================================
# FUNCIONES PARA VENTANAS EMERGENTES DE INFORMACIÓN (ACERCA DE Y AYUDA)
# =============================================================================
def mostrar_acerca_de(parent):
    play_sfx("major_function.ogg")
    win_about = tk.Toplevel(parent)
    win_about.title("Acerca de - SOLEIL DATABASES")
    win_about.geometry("520x580")
    win_about.configure(bg="white")
    win_about.transient(parent)
    win_about.grab_set()
    win_about.focus_set()
    
    frame_ctrl = tk.Frame(win_about, bg="#0A4E5C", height=35)
    frame_ctrl.pack(fill="x")
    frame_ctrl.pack_propagate(False)
    
    try:
        ruta_logo = resource_path("soleil.png")
        win_about.logo_img = tk.PhotoImage(file=ruta_logo).subsample(3, 3)
        tk.Label(win_about, image=win_about.logo_img, bg="white").pack(pady=(15, 5))
    except:
        tk.Label(win_about, text="☀️", font=("Century Gothic", 26), bg="white", fg="#0A4E5C").pack(pady=10)
        
    tk.Label(win_about, text="SOLEIL DATABASES", font=("Century Gothic", 15, "bold"), fg="#0A4E5C", bg="white").pack()
    tk.Label(win_about, text="Control Avanzado de Inventarios y Auditorías de Áreas Técnicas", font=("Century Gothic", 9, "italic"), fg="#148197", bg="white").pack(pady=(2, 10))
    
    info_texto = (
        "■ DESARROLLADORES:\n"
        "Diseñado e implementado íntegramente como Proyecto Técnico Institucional para la optimización de recursos pedagógicos.\n\n"
        "■ NOMBRE DE MARCA REGISTRADA:\n"
        "Soleil Databases © 2026. Todos los derechos reservados.\n\n"
        "■ LIBRERÍAS Y TECNOLOGÍAS UTILIZADAS (PYTHON):\n"
        "• Tkinter & Ttk: Desarrollo de la arquitectura visual de la interfaz gráfica (GUI).\n"
        "• SQLite3: Motor relacional integrado para persistencia de datos local robusta.\n"
        "• ReportLab: Compilación algorítmica y maquetación estructurada de reportes en PDF.\n"
        "• Pygame: Motor de renderizado asíncrono para efectos de sonido (SFX).\n"
        "• Pillow (PIL): Soporte adaptativo para el renderizado e inclusión de imágenes vectoriales."
    )
    
    txt_box = tk.Text(win_about, font=("Century Gothic", 10), bg="#F4F8F9", fg="#1B4953", relief="solid", bd=1, wrap="word", padx=12, pady=12)
    txt_box.pack(fill="both", expand=True, padx=25, pady=(5, 20))
    txt_box.insert("1.0", info_texto)
    txt_box.config(state="disabled")

def mostrar_ayuda(parent):
    play_sfx("major_function.ogg")
    win_help = tk.Toplevel(parent)
    win_help.title("Manual de Ayuda e Instrucción - SOLEIL DATABASES")
    win_help.geometry("750x660")
    win_help.configure(bg="white")
    win_help.transient(parent)
    win_help.grab_set()
    win_help.focus_set()
    
    frame_ctrl = tk.Frame(win_help, bg="#0A4E5C", height=40)
    frame_ctrl.pack(fill="x")
    frame_ctrl.pack_propagate(False)

    try:
        ruta_logo = resource_path("soleil.png")
        win_help.logo_img = tk.PhotoImage(file=ruta_logo).subsample(4, 4)
        lbl_img = tk.Label(frame_ctrl, image=win_help.logo_img, bg="#0A4E5C")
        lbl_img.pack(side="left", padx=10, pady=2)
    except: pass
        
    tk.Label(frame_ctrl, text="MANUAL DE OPERACIÓN DEL SISTEMA", font=("Century Gothic", 10, "bold"), fg="white", bg="#0A4E5C").pack(side="left", padx=5)
    
    txt_ayuda = tk.Text(win_help, font=("Century Gothic", 10), bg="white", fg="#1B4953", relief="flat", wrap="word", padx=15, pady=15)
    scroll = ttk.Scrollbar(win_help, orient="vertical", command=txt_ayuda.yview)
    txt_ayuda.configure(yscrollcommand=scroll.set)
    
    scroll.pack(side="right", fill="y")
    txt_ayuda.pack(side="left", fill="both", expand=True)
    
    manual_contenido = (
        "¡Bienvenido al Manual Integrado de SOLEIL DATABASES!\n"
        "Este entorno ha sido estructurado para facilitar la gestión técnica escolar. Siga las pautas descritas a continuación:\n\n"
        "1. CONTROL DE ACCESO (ROLES DE SEGURIDAD)\n"
        "El sistema distribuye sus capacidades operativas en tres perfiles jerárquicos diferenciados:\n"
        "• Operador / Consulta: Perfil básico con permisos de solo lectura.\n"
        "• Supervisor / Editor: Perfil intermedio. Habilita ingreso y actualización de datos.\n"
        "• Creador / Administrador: Acceso total y restrictivo.\n\n"
        "2. DESCRIPCIÓN DE VENTANAS PRINCIPALES\n"
        "• Panel General: Contiene pestañas para Especialidades, Personal e Inventario clasificado (Herramientas, Materiales, etc.).\n"
        "• Registro de Actividad: Almacena cronológicamente cada cambio en el sistema y lo traduce a un formato humano.\n\n"
        "3. ACCIONES Y FUNCIONES\n"
        "• RETIRAR PARA USO (ASIGNAR): Presta recursos a los docentes descontando automáticamente del stock.\n"
        "• DEVOLVER A STOCK: Reincorpora elementos devolviéndolos al inventario principal.\n"
        "• GENERAR PDF: Compila reportes técnicos inmediatos."
    )
    
    txt_ayuda.insert("1.0", manual_contenido)
    txt_ayuda.config(state="disabled")

# --- GESTIÓN DE BASE DE DATOS Y AUDITORÍA ---
def query_db(query, parameters=()):
    with sqlite3.connect("sistema_tecnico.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        return cursor.fetchall()

def registrar_evento(evento):
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_db("INSERT INTO logs (evento, fecha_hora) VALUES (?, ?)", (evento, fecha_hora))

def inicializar_db():
    query_db("CREATE TABLE IF NOT EXISTS especialidades (id INTEGER PRIMARY KEY, nombre TEXT)")
    query_db("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, esp_id INTEGER, FOREIGN KEY(esp_id) REFERENCES especialidades(id))")
    
    query_db("CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, item TEXT, cantidad INTEGER, categoria TEXT DEFAULT 'Herramientas')")
    try:
        query_db("ALTER TABLE inventario ADD COLUMN categoria TEXT DEFAULT 'Herramientas'")
    except:
        pass 
    
    query_db("""CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY, 
                inventario_id INTEGER, 
                usuario_id INTEGER, 
                especialidad_id INTEGER,
                fecha TEXT,
                FOREIGN KEY(inventario_id) REFERENCES inventario(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(especialidad_id) REFERENCES especialidades(id))""")
    
    query_db("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, evento TEXT, fecha_hora TEXT)")

    if not query_db("SELECT * FROM especialidades"):
        for esp in ['Telemática', 'Electricidad', 'Electrónica', 'Metalmecánica']:
            query_db("INSERT INTO especialidades (nombre) VALUES (?)", (esp,))


# --- VENTANA DE REGISTRO DE ACTIVIDAD (AUDITORÍA) ---
def abrir_registro_actividad(parent):
    play_sfx("button_click.ogg")
    registrar_evento("Botón presionado: Abrir Registro de Actividad")
    reg_win = tk.Toplevel(parent)
    reg_win.title("SOLEIL DATABASES - REGISTRO DE AUDITORÍA")
    reg_win.geometry("900x700")  
    reg_win.configure(bg="#F4F8F9")
    
    header_reg = tk.Frame(reg_win, bg="#0A4E5C", height=60)
    header_reg.pack(fill="x")
    header_reg.pack_propagate(False)
    
    tk.Label(header_reg, text="📋 HISTORIAL DE ACCIONES Y CAMBIOS DEL SISTEMA", 
             fg="white", bg="#0A4E5C", font=("Century Gothic", 11, "bold")).pack(side="left", padx=20, pady=18)
    
    frame_tabla = tk.Frame(reg_win, bg="#F4F8F9")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    tree_logs = ttk.Treeview(frame_tabla, columns=("ID", "Evento / Acción", "Fecha y Hora"), show="headings")
    tree_logs.heading("ID", text="ID")
    tree_logs.heading("Evento / Acción", text="EVENTO / ACCIÓN DEL USUARIO")
    tree_logs.heading("Fecha y Hora", text="FECHA Y HORA")
    
    tree_logs.column("ID", width=60, anchor="center")
    tree_logs.column("Evento / Acción", width=490, anchor="w")
    tree_logs.column("Fecha y Hora", width=170, anchor="center")
    
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree_logs.yview)
    tree_logs.configure(yscrollcommand=scrollbar.set)
    
    tree_logs.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    frame_detalle = tk.LabelFrame(reg_win, text=" 🔍 DESCRIPCIÓN DEL MOVIMIENTO SELECCIONADO ", 
                                  font=("Century Gothic", 9, "bold"), bg="white", fg="#0A4E5C", bd=1, relief="solid")
    frame_detalle.pack(fill="x", padx=20, pady=(5, 20), ipady=8)

    txt_detalle = tk.Text(frame_detalle, font=("Century Gothic", 10), bg="white", fg="#1B4953", height=4, relief="flat", wrap="word")
    txt_detalle.pack(fill="both", expand=True, padx=15, pady=10)
    txt_detalle.insert("1.0", "Seleccione cualquier fila del registro superior para desglosar narrativamente la actividad ocurrida.")
    txt_detalle.config(state="disabled")

    def traducir_a_narrativa(evento_raw):
        import re
        if "Retiro de" in evento_raw and "asignadas al Docente" in evento_raw:
            match = re.search(r"Retiro de (\d+) unidad\(es\) de '(.*)' asignadas al Docente ([^\[]+) \[(.*)\]", evento_raw)
            if match:
                cant, recurso, docente, mencion = match.groups()
                return f"El profesor {docente.strip()}, adscrito a la mención de {mencion.strip()}, retiró con éxito {cant} unidad(es) del recurso '{recurso.strip()}' para su respectiva utilización en las áreas técnicas asignadas."
        
        elif "Devolución de" in evento_raw and "devueltas por Docente" in evento_raw:
            match = re.search(r"Devolución de (\d+) unidad\(es\) de(?: la herramienta|l recurso) '(.*)' devueltas por Docente (.*)", evento_raw)
            if match:
                cant, recurso, docente = match.groups()
                return f"El profesor {docente.strip()} realizó formalmente la entrega y devolución de {cant} unidad(es) del recurso '{recurso.strip()}', reincorporándolas de forma satisfactoria al stock del inventario."
        
        return None 

    def mostrar_detalle_humano(event):
        sel = tree_logs.selection()
        if not sel: return
        
        valores = tree_logs.item(sel)['values']
        evento_raw = str(valores[1])
        fecha_hora = valores[2]
        
        narrativa = traducir_a_narrativa(evento_raw)
        if not narrativa:
            import re
            if "Creado nuevo registro en tabla" in evento_raw:
                match = re.search(r"Creado nuevo registro en tabla (\w+) \(Valores: (.*)\)", evento_raw)
                if match:
                    tabla, valores_db = match.groups()
                    nom_tabla = {"ESPECIALIDADES": "Menciones/Especialidades", "USUARIOS": "Personal Docente", "INVENTARIO": "Inventario de Recursos"}
                    nombre_amigable = nom_tabla.get(tabla.upper(), tabla)
                    narrativa = f"Se ha registrado una nueva incorporación dentro de la sección de [{nombre_amigable}]. El elemento guardado contiene los siguientes valores de base de datos: {valores_db}."
            elif "LOGIN: Acceso concedido" in evento_raw:
                match = re.search(r"Acceso concedido a '(.*)' como \[(.*)\]", evento_raw)
                if match: narrativa = f"El sistema autorizó el ingreso al entorno de control técnico al usuario '{match.group(1)}', operando bajo el perfil de '{match.group(2)}'."
            elif "ALERTA: Intento de acceso fallido" in evento_raw:
                match = re.search(r"Intento de acceso fallido para el usuario: '(.*)'", evento_raw)
                if match: narrativa = f"Seguridad del Sistema: Se denegó un intento fallido de inicio de sesión. Se intentaron validar credenciales erróneas con el usuario: '{match.group(1)}'."
            
            if not narrativa: narrativa = evento_raw

        txt_detalle.config(state="normal")
        txt_detalle.delete("1.0", tk.END)
        txt_detalle.insert("1.0", f"📅 REGISTRO TEMPORAL: {fecha_hora}\n\n💬 HISTORIA DEL MOVIMIENTO:\n{narrativa}")
        txt_detalle.config(state="disabled")

    tree_logs.bind("<<TreeviewSelect>>", mostrar_detalle_humano)

    def exportar_pdf_narrativa():
        play_sfx("button_click.ogg")
        from reportlab.lib.styles import ParagraphStyle
        global usuario_actual
        
        try:
            if hasattr(sys, '_MEIPASS'): dir_base = os.path.dirname(sys.executable)
            else: dir_base = os.path.dirname(os.path.abspath(__file__))
            
            ruta_carpeta_reportes = os.path.join(dir_base, "Reportes")
            os.makedirs(ruta_carpeta_reportes, exist_ok=True)
            
            filename = f"Reporte_Narrativo_Auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_completa = os.path.join(ruta_carpeta_reportes, filename)
            
            doc = SimpleDocTemplate(ruta_completa, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
            elements = []
            styles = getSampleStyleSheet()
            
            style_titulo = ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0A4E5C'), spaceAfter=8)
            style_sub = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#148197'), alignment=1, spaceAfter=20)
            style_meta = ParagraphStyle('DocMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#6c757d'), spaceAfter=25)
            
            style_th = ParagraphStyle('TableHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)
            style_td_fecha = ParagraphStyle('TableDate', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor('#1B4953'), alignment=1)
            style_td_desc = ParagraphStyle('TableDesc', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#1B4953'))
            
            elements.append(Paragraph("SOLEIL DATABASES - INFORME NARRATIVO", style_titulo))
            elements.append(Paragraph("Historial Estructurado de Préstamos y Devoluciones Generales", style_sub))
            
            nombre_usuario = usuario_actual.get("username", "admin").capitalize() if usuario_actual else "Administrador"
            
            meta_info = f"<b>Fecha de Generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>" \
                        f"<b>Área de Auditoría:</b> Control de Stock e Inventario Técnico Escolar.<br/>" \
                        f"<b>Usuario que generó el PDF:</b> {nombre_usuario}<br/>" \
                        f"<b>Ubicación:</b> /Reportes/{filename}"
            
            elements.append(Paragraph(meta_info, style_meta))
            
            tabla_datos = [[Paragraph("FECHA Y HORA", style_th), Paragraph("HISTORIAL DE MOVIMIENTOS", style_th)]]
            logs_procesados = 0
            
            for item in tree_logs.get_children():
                valores = tree_logs.item(item)['values']
                evento_raw = str(valores[1])
                fecha_hora = valores[2]
                
                narrativa_texto = traducir_a_narrativa(evento_raw)
                if narrativa_texto:
                    logs_procesados += 1
                    tabla_datos.append([Paragraph(fecha_hora, style_td_fecha), Paragraph(narrativa_texto, style_td_desc)])
            
            if logs_procesados > 0:
                tabla_pdf = Table(tabla_datos, colWidths=[134, 370])
                tabla_pdf.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A4E5C')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F8F9')]),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.6, colors.HexColor('#CBE0E3')),
                ]))
                elements.append(tabla_pdf)
            else:
                elements.append(Paragraph("<i>No se localizaron registros vigentes de préstamos o devoluciones en el módulo analizado.</i>", styles['Normal']))
            
            doc.build(elements)
            play_sfx("major_function.ogg")
            if messagebox.askyesno("Éxito", f"Reporte guardado en:\n📁 /Reportes/{filename}\n\n¿Desea abrir la carpeta ahora?", parent=reg_win):
                if sys.platform == "win32": os.startfile(ruta_carpeta_reportes)
                else: subprocess.Popen(["xdg-open", ruta_carpeta_reportes])
                
        except Exception as e:
            play_sfx("error.ogg")
            messagebox.showerror("Error PDF", f"Ocurrió un problema: {e}", parent=reg_win)

    def limpiar_historial():
        play_sfx("button_click.ogg")
        if messagebox.askyesno("Confirmar Eliminación", "¿Desea borrar permanentemente los registros?", parent=reg_win):
            try:
                query_db("DELETE FROM logs")
                registrar_evento("Limpieza de sistema: Historial de auditoría vaciado por el administrador")
                for item in tree_logs.get_children(): tree_logs.delete(item)
                logs_data = query_db("SELECT id, evento, fecha_hora FROM logs ORDER BY id DESC")
                for log in logs_data: tree_logs.insert("", "end", values=log)
                play_sfx("successful_change.ogg")
                messagebox.showinfo("Éxito", "Historial vaciado correctamente.", parent=reg_win)
            except Exception as e:
                play_sfx("error.ogg")
                messagebox.showerror("Error", f"No se pudo vaciar: {e}", parent=reg_win)

    tk.Button(header_reg, text="🗑️ LIMPIAR HISTORIAL", bg="#631E26", fg="white", font=("Century Gothic", 9, "bold"), command=limpiar_historial, relief="flat", padx=12, pady=4, cursor="hand2").pack(side="right", padx=20, pady=15)
    btn_pdf_narrativa = tk.Button(header_reg, text="📄 PDF NARRATIVO", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "bold"), command=exportar_pdf_narrativa, relief="flat", padx=12, pady=4, cursor="hand2")
    btn_pdf_narrativa.pack(side="right", padx=(0, 5), pady=15)
    btn_ayuda_reg = tk.Button(header_reg, text="❓ AYUDA", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "bold"), relief="flat", padx=12, pady=4, cursor="hand2", command=lambda: mostrar_ayuda(reg_win))
    btn_ayuda_reg.pack(side="right", padx=5, pady=15)
    btn_about_reg = tk.Button(header_reg, text="ℹ️ ACERCA DE", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "bold"), relief="flat", padx=12, pady=4, cursor="hand2", command=lambda: mostrar_acerca_de(reg_win))
    btn_about_reg.pack(side="right", padx=5, pady=15)

    try:
        logs_data = query_db("SELECT id, evento, fecha_hora FROM logs ORDER BY id DESC")
        for log in logs_data: tree_logs.insert("", "end", values=log)
    except Exception as e:
        play_sfx("error.ogg")
        messagebox.showerror("Error", f"No se pudieron leer los registros: {e}")


# --- CLASE CRUD PRINCIPAL REESTRUCTURADA ---
class ModuloCRUD(tk.Frame):
    def __init__(self, parent, tabla, columnas, fields, categoria_actual=None, cmd_volver=None):
        super().__init__(parent, bg="#F4F8F9")
        self.tabla = tabla
        self.fields = fields
        self.categoria_actual = categoria_actual
        self.inputs = {}
        self.combos_info = {}
        
        if cmd_volver:
            tk.Button(self, text="⬅ VOLVER AL MENÚ DE INVENTARIO", bg="#631E26", fg="white", font=("Century Gothic", 9, "bold"), command=cmd_volver, cursor="hand2", relief="flat", padx=15, pady=4).pack(anchor="nw", padx=25, pady=(15, 0))

        titulo_seccion = f"  GESTIÓN DE {self.categoria_actual.upper()}  " if self.categoria_actual else f"  GESTIÓN DE {tabla.upper()}  "

        frame_top = tk.LabelFrame(self, text=titulo_seccion, font=("Century Gothic", 10, "bold"), bg="white", fg="#0A4E5C", padx=15, pady=15, bd=1, relief="solid")
        frame_top.pack(fill="x", padx=25, pady=15)

        for idx in range(len(fields) * 2): frame_top.columnconfigure(idx, weight=1)

        for i, (label, tipo) in enumerate(fields.items()):
            texto_visual = "ESPECIALIDAD:" if label == "esp_id" else label.upper() + ":"
            tk.Label(frame_top, text=texto_visual, bg="white", font=("Century Gothic", 9, "bold"), fg="#1B4953").grid(row=0, column=i*2, padx=(10, 2), pady=8, sticky="e")
            
            if tipo == "text" or tipo == "int":
                res = tk.Entry(frame_top, font=("Century Gothic", 10), bd=1, relief="solid", highlightthickness=1, highlightbackground="#CBE0E3", highlightcolor="#148197")
            else: 
                res = ttk.Combobox(frame_top, font=("Century Gothic", 9), state="readonly")
                self.combos_info[label] = tipo
            res.grid(row=0, column=i*2+1, padx=(2, 10), pady=8, sticky="w")
            self.inputs[label] = res
            
        search_frame = tk.Frame(self, bg="#F4F8F9")
        search_frame.pack(fill="x", padx=25, pady=(5, 10))
        
        tk.Label(search_frame, text="🔍 BUSCAR:", bg="#F4F8F9", font=("Century Gothic", 9, "bold"), fg="#0A4E5C").pack(side="left", padx=(0, 5))
        self.ent_search = tk.Entry(search_frame, font=("Century Gothic", 10), bd=1, relief="solid", highlightthickness=1, highlightbackground="#CBE0E3", highlightcolor="#148197")
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5, ipady=2)
        self.ent_search.bind("<KeyRelease>", lambda e: self.read(self.ent_search.get()))

        if tabla != "especialidades":
            texto_boton = "📂 AGRUPAR POR ESPECIALIDAD" if tabla == "usuarios" else "📦 ORDENAR POR STOCK"
            tk.Button(search_frame, text=texto_boton, bg="#2E3F3F", fg="white", font=("Century Gothic", 8, "bold"), command=lambda:[play_sfx("button_click.ogg"), self.ordenar_por_criterio()], relief="flat", cursor="hand2", padx=10, pady=2).pack(side="right", padx=(10, 0))

        if tabla == "inventario":
            loan_frame = tk.Frame(self, bg="#F4F8F9")
            loan_frame.pack(pady=12) 
            
            btn_retirar = tk.Button(loan_frame, text="🚀 RETIRAR PARA USO (ASIGNAR)", bg="#18331A", fg="white", font=("Century Gothic", 10, "bold"), relief="flat", padx=22, pady=8, cursor="hand2", command=self.prestar_herramienta)
            btn_retirar.pack(side="left", padx=12)
            
            btn_devolver = tk.Button(loan_frame, text="📦 DEVOLVER A STOCK (RECEPCIÓN)", bg="#18331A", fg="white", font=("Century Gothic", 10, "bold"), relief="flat", padx=22, pady=8, cursor="hand2", command=self.devolver_herramienta)
            btn_devolver.pack(side="left", padx=12)
            
            btn_pdf = tk.Button(loan_frame, text="📄 GENERAR PDF", bg="#0A4E5C", fg="white", font=("Century Gothic", 10, "bold"), relief="flat", padx=22, pady=8, cursor="hand2", command=self.exportar_pdf)
            btn_pdf.pack(side="left", padx=12)

            for b, col_base, col_hover in [(btn_retirar, "#18331A", "#244D27"), (btn_devolver, "#18331A", "#244D27"), (btn_pdf, "#0A4E5C", "#0F6E82")]:
                b.bind("<Enter>", lambda e, btn=b, h=col_hover: btn.config(bg=h))
                b.bind("<Leave>", lambda e, btn=b, c=col_base: btn.config(bg=c))

        btn_frame = tk.Frame(self, bg="#F4F8F9")
        btn_frame.pack(pady=15)
        
        btns = [("CREAR", "#18331A", "#244D27", self.create), ("ACTUALIZAR", "#0A4E5C", "#0F6E82", self.update), ("BORRAR", "#631E26", "#8A2B35", self.delete)]
        self.botones_crud = {}  
        
        for text, color, h_color, cmd in btns:
            btn = tk.Button(btn_frame, text=text, bg=color, fg="white", width=16, font=("Century Gothic", 10, "bold"), relief="flat", pady=8, cursor="hand2", command=cmd)
            btn.pack(side="left", padx=10)
            self.botones_crud[text] = btn
            btn.bind("<Enter>", lambda e, b=btn, h=h_color: b.config(bg=h) if b['state'] != 'disabled' else None)
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c) if b['state'] != 'disabled' else None)

        style_tree = ttk.Style()
        style_tree.theme_use("default")
        style_tree.configure("TNotebook.Tab", font=("Century Gothic", 11, "bold"), padding=[22, 8], background="#E0ECEF", foreground="#1B4953")
        style_tree.map("TNotebook.Tab", background=[("selected", "#0A4E5C")], foreground=[("selected", "white")])
        style_tree.configure("Treeview.Heading", font=("Century Gothic", 10, "bold"), background="#E0ECEF", foreground="#1B4953", relief="flat")
        style_tree.configure("Treeview", font=("Century Gothic", 10), rowheight=32, gridlinecolor="#D5E4E6", background="white")
        style_tree.map("Treeview", background=[('selected', '#148197')], foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        for col in columnas: 
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=25, pady=(10, 20))
        self.tree.tag_configure('low_stock', background='#FFC0C0', foreground='red')
        
        
        self.tree.bind("<<TreeviewSelect>>", self.cargar_seleccion)
        self.read()
        
        if not verificar_permiso(2):
            for btn in self.botones_crud.values(): btn.configure(state="disabled", bg="#A3C1C6")
        elif not verificar_permiso(3):
            if "BORRAR" in self.botones_crud: self.botones_crud["BORRAR"].configure(state="disabled", bg="#A3C1C6")

    def exportar_pdf(self):
        play_sfx("button_click.ogg")
        try:
            if hasattr(sys, '_MEIPASS'): dir_base = os.path.dirname(sys.executable)
            else: dir_base = os.path.dirname(os.path.abspath(__file__))
            
            ruta_carpeta_reportes = os.path.join(dir_base, "Reportes")
            os.makedirs(ruta_carpeta_reportes, exist_ok=True)
            
            sufijo_cat = f"_{self.categoria_actual}" if self.categoria_actual else ""
            filename = f"Reporte_{self.tabla}{sufijo_cat}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_completa = os.path.join(ruta_carpeta_reportes, filename)

            doc = SimpleDocTemplate(ruta_completa, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            cat_str = f" ({self.categoria_actual.upper()})" if self.categoria_actual else ""
            title = Paragraph(f"<b>SOLEIL DATABASES - REPORTE TÉCNICO{cat_str}</b>", styles['Title'])
            elements.append(title)
            elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            elements.append(Spacer(1, 20))

            elements.append(Paragraph("<b>1. ESTADO ACTUAL DEL INVENTARIO GENERAL (DEPOSITADO)</b>", styles['Heading2']))
            elements.append(Spacer(1, 10))
            
            headers_inv = ["ID", "Recurso / Ítem", "Stock Disponible"]
            data_inv = [headers_inv]
            for child in self.tree.get_children():
                vals = self.tree.item(child)['values']
                data_inv.append([vals[0], vals[1], vals[2]])

            t_inv = Table(data_inv, hAlign='CENTER', colWidths=[60, 240, 150])
            t_inv.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A4E5C")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(t_inv)
            elements.append(Spacer(1, 25))

            elements.append(Paragraph("<b>2. DETALLE DE ASIGNACIONES ACTIVAS (EN USO)</b>", styles['Heading2']))
            elements.append(Spacer(1, 10))

            if self.categoria_actual:
                query_uso = """
                    SELECT i.item, u.nombre, e.nombre, p.fecha 
                    FROM prestamos p
                    JOIN inventario i ON p.inventario_id = i.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    JOIN especialidades e ON p.especialidad_id = e.id
                    WHERE i.categoria = ?
                    ORDER BY p.fecha DESC
                """
                prestamos_activos = query_db(query_uso, (self.categoria_actual,))
            else:
                query_uso = """
                    SELECT i.item, u.nombre, e.nombre, p.fecha 
                    FROM prestamos p
                    JOIN inventario i ON p.inventario_id = i.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    JOIN especialidades e ON p.especialidad_id = e.id
                    ORDER BY p.fecha DESC
                """
                prestamos_activos = query_db(query_uso)

            if prestamos_activos:
                headers_uso = ["Recurso", "Docente Responsable", "Mención/Especialidad", "Fecha Retiro"]
                data_uso = [headers_uso]
                for p in prestamos_activos: data_uso.append(list(p))

                t_uso = Table(data_uso, hAlign='CENTER', colWidths=[120, 130, 110, 110])
                t_uso.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A4E5C")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ]))
                elements.append(t_uso)
            else:
                elements.append(Paragraph("<i>No existen recursos retirados o bajo cargo docente en este momento.</i>", styles['Normal']))

            elements.append(Spacer(1, 50))
            data_firma = [["__________________________", "__________________________"], ["Firma Responsable Técnico", "Sello de Control / Auditoría"]]
            t_firma = Table(data_firma, colWidths=[225, 225])
            t_firma.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))
            elements.append(t_firma)
            
            doc.build(elements)
            play_sfx("major_function.ogg")
            
            if messagebox.askyesno("Éxito", f"Reporte guardado en:\n📁 /Reportes/{filename}\n\n¿Desea abrir la carpeta ahora?", parent=self):
                if sys.platform == "win32": os.startfile(ruta_carpeta_reportes)
                else: subprocess.Popen(["xdg-open", ruta_carpeta_reportes])
        except Exception as e:
            play_sfx("error.ogg")
            messagebox.showerror("Error PDF", f"Error al compilar reporte: {e}", parent=self)

    def ordenar_por_criterio(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        if self.tabla == "inventario":
            query = "SELECT id, item, cantidad FROM inventario WHERE categoria = ? ORDER BY cantidad DESC"
            data = query_db(query, (self.categoria_actual,))
        elif self.tabla == "usuarios":
            query = "SELECT u.id, u.nombre, e.nombre FROM usuarios u LEFT JOIN especialidades e ON u.esp_id = e.id ORDER BY e.nombre ASC"
            data = query_db(query)
        else:
            query = f"SELECT * FROM {self.tabla} ORDER BY id ASC"
            data = query_db(query)
        for fila in data: self.tree.insert("", "end", values=fila)

    def cargar_seleccion(self, event):
        sel = self.tree.selection()
        if not sel: return
        valores = self.tree.item(sel)['values']
        for i, (label, widget) in enumerate(self.inputs.items()):
            val_tabla = str(valores[i+1])
            if isinstance(widget, ttk.Combobox):
                for index, item in enumerate(widget['values']):
                    if val_tabla in item:
                        widget.current(index)
                        break
            else:
                widget.delete(0, tk.END)
                widget.insert(0, val_tabla)

    def update_combos(self):
        for label, tabla_ref in self.combos_info.items():
            datos = query_db(f"SELECT id, nombre FROM {tabla_ref}")
            self.inputs[label]['values'] = [f"{d[1]} (ID:{d[0]})" for d in datos]

    def read(self, filter_text=""):
        if not filter_text: self.update_combos()
        for i in self.tree.get_children(): self.tree.delete(i)
        
        alert_sound_played = False # Bandera para no saturar el sonido
        
        if self.tabla == "inventario":
            query = "SELECT id, item, cantidad FROM inventario WHERE item LIKE ? AND categoria = ?"
            data = query_db(query, ('%' + filter_text + '%', self.categoria_actual))
            
            for fila in data:
                id_fila = self.tree.insert("", "end", values=fila)
                cantidad = fila[2]
                
                # Lógica de Alerta de Bajas Unidades
                if cantidad < 1:
                    self.tree.item(id_fila, tags=('low_stock',))
                    if not alert_sound_played:
                        play_sfx("error.ogg")
                        alert_sound_played = True
                        
        elif self.tabla == "usuarios":
            # ... (tu código original para usuarios)
            query = "SELECT u.id, u.nombre, e.nombre FROM usuarios u LEFT JOIN especialidades e ON u.esp_id = e.id WHERE u.nombre LIKE ?"
            data = query_db(query, ('%' + filter_text + '%',))
            for fila in data: self.tree.insert("", "end", values=fila)
        else:
            # ... (tu código original para otros)
            query = f"SELECT * FROM {self.tabla} WHERE nombre LIKE ?"
            data = query_db(query, ('%' + filter_text + '%',))
            for fila in data: self.tree.insert("", "end", values=fila)

    def prestar_herramienta(self):
        play_sfx("button_click.ogg")
        sel = self.tree.selection()
        if not sel: 
            play_sfx("error.ogg")
            return messagebox.showwarning("Atención", "Seleccione un ítem del inventario")
        
        item_id, item_nombre, cant_actual = self.tree.item(sel)['values']
        if cant_actual <= 0: 
            play_sfx("error.ogg")
            return messagebox.showerror("Error", "No hay stock disponible.")
        
        win_cant = tk.Toplevel(self)
        win_cant.title("Retirar Unidades - Asignación de Cargo")
        win_cant.geometry("400x340")
        win_cant.configure(bg="white")
        win_cant.transient(self)
        win_cant.grab_set()
        win_cant.resizable(False, False)
        
        tk.Label(win_cant, text=f"ÍTEM: {item_nombre.upper()}", bg="white", font=("Century Gothic", 10, "bold"), fg="#1B4953").pack(pady=(15, 5))
        tk.Label(win_cant, text=f"Stock General: {cant_actual} unidades", bg="white", font=("Century Gothic", 9), fg="#148197").pack()
        
        tk.Label(win_cant, text="SELECCIONE MENCIÓN / ÁREA:", bg="white", font=("Century Gothic", 9, "bold"), fg="#1B4953").pack(pady=(10, 2))
        combo_esp = ttk.Combobox(win_cant, font=("Century Gothic", 9), state="readonly", width=35)
        combo_esp.pack(pady=2)
        datos_esp = query_db("SELECT id, nombre FROM especialidades")
        combo_esp['values'] = [f"{d[1]} (ID:{d[0]})" for d in datos_esp]
        
        tk.Label(win_cant, text="SELECCIONE DOCENTE RESPONSABLE:", bg="white", font=("Century Gothic", 9, "bold"), fg="#1B4953").pack(pady=(10, 2))
        combo_doc = ttk.Combobox(win_cant, font=("Century Gothic", 9), state="readonly", width=35)
        combo_doc.pack(pady=2)
        
        def filtrar_docentes(event):
            try:
                esp_id = combo_esp.get().split("ID:")[1].split(")")[0].strip()
                datos_doc = query_db("SELECT id, nombre FROM usuarios WHERE esp_id = ?", (esp_id,))
                combo_doc['values'] = [f"{d[1]} (ID:{d[0]})" for d in datos_doc]
                combo_doc.set('') 
            except: pass
            
        combo_esp.bind("<<ComboboxSelected>>", filtrar_docentes)
        
        tk.Label(win_cant, text="CANTIDAD A ASIGNAR/RETIRAR:", bg="white", font=("Century Gothic", 9, "bold"), fg="#18331A").pack(pady=(10, 2))
        ent_cant = tk.Entry(win_cant, font=("Century Gothic", 10), justify="center", bd=1, relief="solid", width=15)
        ent_cant.pack(ipady=2)
        ent_cant.insert(0, "1")
        
        def ejecutar_retiro():
            if not combo_esp.get(): 
                play_sfx("error.ogg")
                return messagebox.showerror("Error", "Debe seleccionar una mención.", parent=win_cant)
            if not combo_doc.get(): 
                play_sfx("error.ogg")
                return messagebox.showerror("Error", "Debe seleccionar un docente.", parent=win_cant)
            try:
                cantidad = int(ent_cant.get())
                if cantidad <= 0: raise ValueError
                if cantidad > cant_actual:
                    play_sfx("error.ogg")
                    return messagebox.showerror("Error de Stock", f"No puede retirar más unidades de las disponibles ({cant_actual}).", parent=win_cant)
            except ValueError:
                play_sfx("error.ogg")
                return messagebox.showerror("Error de Entrada", "Por favor, introduzca un número entero válido.", parent=win_cant)
            
            esp_id = combo_esp.get().split("ID:")[1].split(")")[0].strip()
            user_id = combo_doc.get().split("ID:")[1].split(")")[0].strip()
            doc_nombre = combo_doc.get().split(" (ID:")[0].strip()
            esp_nombre = combo_esp.get().split(" (ID:")[0].strip()
            
            query_db("UPDATE inventario SET cantidad = cantidad - ? WHERE id = ?", (cantidad, item_id))
            for _ in range(cantidad):
                query_db("INSERT INTO prestamos (inventario_id, usuario_id, especialidad_id, fecha) VALUES (?, ?, ?, datetime('now'))", (item_id, user_id, esp_id))
            
            registrar_evento(f"Cambio en DB: Retiro de {cantidad} unidad(es) de '{item_nombre}' asignadas al Docente {doc_nombre} [{esp_nombre}]")
            play_sfx("inventory_register.ogg")
            win_cant.destroy()
            self.read()
            self._mantener_seleccion(item_id)

        ent_cant.bind("<Return>", lambda e: ejecutar_retiro())
        tk.Button(win_cant, text="CONFIRMAR RETIRO Y ASIGNACIÓN", bg="#18331A", fg="white", font=("Century Gothic", 9, "bold"), relief="flat", cursor="hand2", pady=6, command=lambda:[play_sfx("button_click.ogg"), ejecutar_retiro()]).pack(pady=15)

    def devolver_herramienta(self):
        play_sfx("button_click.ogg")
        sel = self.tree.selection()
        if not sel: 
            play_sfx("error.ogg")
            return messagebox.showwarning("Atención", "Seleccione un ítem del inventario")
        
        item_id, item_nombre, _ = self.tree.item(sel)['values']
        
        query_prestamos = """
            SELECT p.id, u.nombre, e.nombre 
            FROM prestamos p
            JOIN usuarios u ON p.usuario_id = u.id
            JOIN especialidades e ON p.especialidad_id = e.id
            WHERE p.inventario_id = ?
        """
        prestamos_activos = query_db(query_prestamos, (item_id,))
        if not prestamos_activos: 
            play_sfx("error.ogg")
            return messagebox.showwarning("Info", "Este recurso no se encuentra asignado a ningún docente en este momento.")

        win_cant = tk.Toplevel(self)
        win_cant.title("Devolver Unidades - Recepción de Cargo")
        win_cant.geometry("420x260")
        win_cant.configure(bg="white")
        win_cant.transient(self)
        win_cant.grab_set()
        win_cant.resizable(False, False)
        
        tk.Label(win_cant, text=f"ÍTEM: {item_nombre.upper()}", bg="white", font=("Century Gothic", 10, "bold"), fg="#1B4953").pack(pady=(15, 5))
        tk.Label(win_cant, text="SELECCIONE EL DOCENTE QUE DEVOLVERÁ LA UNIDAD:", bg="white", font=("Century Gothic", 9, "bold"), fg="#1B4953").pack(pady=(10, 2))
        
        combo_dev = ttk.Combobox(win_cant, font=("Century Gothic", 9), state="readonly", width=45)
        combo_dev.pack(pady=2)
        combo_dev['values'] = [f"{p[1]} [{p[2]}] (ID Registro:{p[0]})" for p in prestamos_activos]
        
        tk.Label(win_cant, text="CANTIDAD A DEVOLVER A STOCK:", bg="white", font=("Century Gothic", 9, "bold"), fg="#1B4953").pack(pady=(10, 2))
        ent_cant = tk.Entry(win_cant, font=("Century Gothic", 10), justify="center", bd=1, relief="solid", width=15)
        ent_cant.pack(ipady=2)
        ent_cant.insert(0, "1")

        def ejecutar_devolucion():
            if not combo_dev.get(): 
                play_sfx("error.ogg")
                return messagebox.showerror("Error", "Debe elegir el registro de cargo a liberar.", parent=win_cant)
            try:
                cantidad = int(ent_cant.get())
                if cantidad <= 0: raise ValueError
            except ValueError:
                play_sfx("error.ogg")
                return messagebox.showerror("Error de Entrada", "Por favor, introduzca un número entero válido.", parent=win_cant)
            
            info_sel = combo_dev.get()
            id_p_sel = int(info_sel.split("ID Registro:")[1].split(")")[0].strip())
            
            p_base = query_db("SELECT usuario_id, especialidad_id FROM prestamos WHERE id = ?", (id_p_sel,))
            if not p_base: return
            u_id, e_id = p_base[0]
            
            prestamos_del_docente = query_db("SELECT id FROM prestamos WHERE inventario_id = ? AND usuario_id = ? AND especialidad_id = ?", (item_id, u_id, e_id))
            cant_max = len(prestamos_del_docente)
            
            if cantidad > cant_max:
                play_sfx("error.ogg")
                return messagebox.showerror("Error de Retorno", f"Este docente solo posee {cant_max} unidad(es) bajo su responsabilidad.", parent=win_cant)
            
            query_db("UPDATE inventario SET cantidad = cantidad + ? WHERE id = ?", (cantidad, item_id))
            for i in range(cantidad):
                query_db("DELETE FROM prestamos WHERE id = ?", (prestamos_del_docente[i][0],))
                
            doc_nom = info_sel.split(" [")[0]
            registrar_evento(f"Cambio en DB: Devolución de {cantidad} unidad(es) del recurso '{item_nombre}' devueltas por Docente {doc_nom}")
            play_sfx("inventory_register.ogg")
            win_cant.destroy()
            self.read()
            self._mantener_seleccion(item_id)

        ent_cant.bind("<Return>", lambda e: ejecutar_devolucion())
        tk.Button(win_cant, text="CONFIRMAR DEVOLUCIÓN A STOCK", bg="#18331A", fg="white", font=("Century Gothic", 9, "bold"), relief="flat", cursor="hand2", pady=6, command=lambda:[play_sfx("button_click.ogg"), ejecutar_devolucion()]).pack(pady=15)

    def _mantener_seleccion(self, id_objetivo):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == id_objetivo:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def create(self):
        play_sfx("button_click.ogg")
        try:
            vals = []
            for l in self.fields:
                widget = self.inputs[l]
                val = widget.get()
                if isinstance(widget, ttk.Combobox):
                    if "ID:" in val: val = val.split("ID:")[1].split(")")[0].strip()
                    else: 
                        play_sfx("error.ogg")
                        return messagebox.showwarning("Atención", f"Seleccione un valor válido de la lista en {l}")
                if val == "": 
                    play_sfx("error.ogg")
                    return messagebox.showwarning("Atención", f"El campo {l} no puede estar vacío")
                vals.append(val)

            if self.tabla == "inventario":
                columnas = ", ".join(list(self.fields.keys()) + ["categoria"])
                placeholders = ", ".join(["?"] * (len(vals) + 1))
                query_db(f"INSERT INTO {self.tabla} ({columnas}) VALUES ({placeholders})", vals + [self.categoria_actual])
            else:
                columnas = ", ".join(self.fields.keys())
                placeholders = ", ".join(["?"] * len(vals))
                query_db(f"INSERT INTO {self.tabla} ({columnas}) VALUES ({placeholders})", vals)
            
            registrar_evento(f"Cambio en DB: Creado nuevo registro en tabla {self.tabla.upper()} (Valores: {vals})")
            play_sfx("successful_change.ogg")
            self.read()
            for w in self.inputs.values():
                if isinstance(w, ttk.Combobox): w.set('')
                else: w.delete(0, tk.END)
        except Exception as e: 
            play_sfx("error.ogg")
            messagebox.showerror("Error", f"No se pudo crear: {e}")

    def delete(self):
        play_sfx("button_click.ogg")
        sel = self.tree.selection()
        if sel:
            valores_fila = self.tree.item(sel)['values']
            id_reg = valores_fila[0]
            query_db(f"DELETE FROM {self.tabla} WHERE id=?", (id_reg,))
            play_sfx("successful_change.ogg")
            self.read()
        else:
            play_sfx("error.ogg")

    def update(self):
        play_sfx("button_click.ogg")
        sel = self.tree.selection()
        if not sel: 
            play_sfx("error.ogg")
            return messagebox.showwarning("Atención", "Seleccione un registro para actualizar")
        id_reg = self.tree.item(sel)['values'][0]
        try:
            vals = []
            for l in self.fields:
                widget = self.inputs[l]
                val = widget.get()
                if isinstance(widget, ttk.Combobox):
                    if "ID:" in val: val = val.split("ID:")[1].split(")")[0].strip()
                    else: 
                        play_sfx("error.ogg")
                        return messagebox.showwarning("Atención", f"Vuelva a seleccionar la opción en {l}")
                vals.append(val)

            set_str = ", ".join([f"{k}=?" for k in self.fields.keys()])
            query_db(f"UPDATE {self.tabla} SET {set_str} WHERE id=?", vals + [id_reg])
            play_sfx("successful_change.ogg")
            self.read()
            messagebox.showinfo("Éxito", "Registro actualizado")
        except Exception as e: 
            play_sfx("error.ogg")
            messagebox.showerror("Error", f"Verifique los datos: {e}")


# =============================================================================
# MÓDULO CONTENEDOR DE INVENTARIO (MENÚ DE SELECCIÓN)
# =============================================================================
class ModuloInventarioMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F4F8F9")
        self.categorias = ["Herramientas", "Materiales", "Insumos", "Instrumentos", "Equipos"]
        self.frame_menu = tk.Frame(self, bg="#F4F8F9")
        self.frame_menu.pack(fill="both", expand=True)

        tk.Label(self.frame_menu, text="📦 SELECCIONE EL ÁREA DE INVENTARIO", font=("Century Gothic", 16, "bold"), bg="#F4F8F9", fg="#0A4E5C").pack(pady=(60, 30))

        for cat in self.categorias:
            btn = tk.Button(self.frame_menu, text=cat.upper(), bg="#148197", fg="white", font=("Century Gothic", 12, "bold"), width=35, pady=12, cursor="hand2", relief="flat", command=lambda c=cat: self.abrir_categoria(c))
            btn.pack(pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0A4E5C"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#148197"))

        self.frame_crud = None

    def abrir_categoria(self, categoria):
        play_sfx("button_click.ogg")
        self.frame_menu.pack_forget()
        if self.frame_crud: self.frame_crud.destroy()

        self.frame_crud = ModuloCRUD(self, "inventario", ("ID", "Ítem", "Stock Disponible"), {"item": "text", "cantidad": "int"}, categoria_actual=categoria, cmd_volver=self.volver_menu)
        self.frame_crud.pack(fill="both", expand=True)

    def volver_menu(self):
        play_sfx("button_click.ogg")
        if self.frame_crud: self.frame_crud.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)
        
    def read(self):
        if self.frame_crud and self.frame_crud.winfo_ismapped():
            self.frame_crud.read()


# =============================================================================
# MÓDULO EXCLUSIVO DE ESTADÍSTICAS (CON HOVER / TOOLTIPS DETALLADOS)
# =============================================================================
class ModuloEstadisticas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F4F8F9")
        self.tooltip_win = None
        
        frame_top = tk.LabelFrame(self, text="  MÓDULO DE ANALÍTICA Y ESTADÍSTICAS  ", font=("Century Gothic", 10, "bold"), bg="white", fg="#0A4E5C", padx=15, pady=15, bd=1, relief="solid")
        frame_top.pack(fill="both", expand=True, padx=25, pady=20)
        
        lbl_desc = tk.Label(frame_top, text="Volumen de Recursos Distribuidos (Pasa el cursor sobre las variables para ver detalles específicos)", font=("Century Gothic", 10, "italic"), bg="white", fg="#148197")
        lbl_desc.pack(pady=(0, 15))
        
        self.canvas = tk.Canvas(frame_top, bg="white", highlightthickness=1, highlightbackground="#CBE0E3")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.bind("<Unmap>", lambda e: self.ocultar_tooltip())
        
    def mostrar_tooltip(self, event, texto):
        self.ocultar_tooltip()
        self.tooltip_win = tk.Toplevel(self)
        self.tooltip_win.wm_overrideredirect(True)
        self.tooltip_win.configure(bg="#1B4953")
        
        lbl = tk.Label(self.tooltip_win, text=texto, bg="#1B4953", fg="white", font=("Century Gothic", 9, "bold"), justify="left", padx=12, pady=10, relief="solid", bd=1, highlightthickness=0)
        lbl.pack()
        self.mover_tooltip(event)
        
    def mover_tooltip(self, event):
        if self.tooltip_win:
            x = event.x_root + 15
            y = event.y_root + 15
            self.tooltip_win.wm_geometry(f"+{x}+{y}")
            
    def ocultar_tooltip(self):
        if self.tooltip_win:
            self.tooltip_win.destroy()
            self.tooltip_win = None

    def read(self, filter_text=""):
        self.ocultar_tooltip()
        self.canvas.delete("all")
        self.update_idletasks()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 100: canvas_width = 850
        if canvas_height < 100: canvas_height = 420
        
        query = """
            SELECT e.id, e.nombre, COUNT(p.id) 
            FROM especialidades e 
            LEFT JOIN prestamos p ON e.id = p.especialidad_id 
            GROUP BY e.id, e.nombre
        """
        datos = query_db(query)
        
        if not datos:
            self.canvas.create_text(canvas_width/2, canvas_height/2, text="No hay registros suficientes para estructurar métricas.", font=("Century Gothic", 11, "bold"), fill="#631E26")
            return
            
        max_uso = max([d[2] for d in datos]) if datos else 0
        padding_x, padding_y = 80, 60
        graph_width, graph_height = canvas_width - (padding_x * 2), canvas_height - (padding_y * 2)
        
        num_items = len(datos)
        bar_gap = 35
        bar_width = (graph_width - (bar_gap * (num_items - 1))) / num_items
        
        self.canvas.create_line(padding_x - 15, canvas_height - padding_y, canvas_width - padding_x + 15, canvas_height - padding_y, fill="#0A4E5C", width=2)
        
        for idx, (esp_id, mencion, cantidad) in enumerate(datos):
            x0 = padding_x + idx * (bar_width + bar_gap)
            x1 = x0 + bar_width
            
            y0 = canvas_height - padding_y - (graph_height * (cantidad / max_uso)) if max_uso > 0 else canvas_height - padding_y
            y1 = canvas_height - padding_y
            color_barra = "#148197" if idx % 2 == 0 else "#0A4E5C"
            
            query_herramientas = """
                SELECT i.item, COUNT(p.id)
                FROM prestamos p
                JOIN inventario i ON p.inventario_id = i.id
                WHERE p.especialidad_id = ?
                GROUP BY i.id, i.item
            """
            herramientas_detalles = query_db(query_herramientas, (esp_id,))
            
            texto_tooltip = f"📋 MENCIÓN: {mencion.upper()}\n" + "─" * 34 + "\n"
            if herramientas_detalles: texto_tooltip += "\n".join([f" • {item}: {cant} u." for item, cant in herramientas_detalles])
            else: texto_tooltip += " Sin recursos bajo cargo activo."
            
            if cantidad > 0:
                bar_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_barra, outline="#CBE0E3", width=1)
                self.canvas.create_text((x0 + x1) / 2, y0 - 15, text=f"{cantidad} u.", font=("Century Gothic", 10, "bold"), fill="#1B4953")
                self.canvas.tag_bind(bar_id, "<Enter>", lambda e, txt=texto_tooltip: self.mostrar_tooltip(e, txt))
                self.canvas.tag_bind(bar_id, "<Leave>", lambda e: self.ocultar_tooltip())
                self.canvas.tag_bind(bar_id, "<Motion>", lambda e: self.mover_tooltip(e))
            else:
                self.canvas.create_text((x0 + x1) / 2, y1 - 15, text="0", font=("Century Gothic", 10), fill="#A3C1C6")
                
            txt_id = self.canvas.create_text((x0 + x1) / 2, y1 + 22, text=mencion.upper(), font=("Century Gothic", 9, "bold"), fill="#1B4953", width=bar_width + 25, justify="center")
            self.canvas.tag_bind(txt_id, "<Enter>", lambda e, txt=texto_tooltip: self.mostrar_tooltip(e, txt))
            self.canvas.tag_bind(txt_id, "<Leave>", lambda e: self.ocultar_tooltip())
            self.canvas.tag_bind(txt_id, "<Motion>", lambda e: self.mover_tooltip(e))


# --- ENTORNO PANEL DE CONTROL PRINCIPAL ---
def abrir_sistema():
    global usuario_actual
    main_win = tk.Toplevel()
    main_win.title(f"SOLEIL DATABASES - Panel General [{usuario_actual['cargo']}]")
    main_win.geometry("1180x780")
    
    header = tk.Frame(main_win, bg="#0A4E5C", height=95)
    header.pack(fill="x")
    header.pack_propagate(False) 
    
    lbl_status = tk.Label(header, text=f"SESIÓN: {usuario_actual['username'].upper()}\n[{usuario_actual['cargo']}]", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "bold"), justify="left")
    lbl_status.pack(side="left", padx=20, pady=25)
    
    def cerrar_sesion():
        play_sfx("button_click.ogg")
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea salir?"):
            play_sfx("session.ogg")
            e_user.delete(0, tk.END)
            e_pass.delete(0, tk.END)
            main_win.destroy()
            root.deiconify()
    
    try:
        ruta_neg_logo = resource_path("soleil.png")
        main_win.logo_img = tk.PhotoImage(file=ruta_neg_logo).subsample(4, 4)
        lbl_img = tk.Label(header, image=main_win.logo_img, bg="#0A4E5C")
        lbl_img.pack(side="left", padx=(25, 12), pady=5)
        tk.Label(header, text="SOLEIL DATABASES", fg="white", bg="#0A4E5C", font=("Century Gothic", 16, "bold")).pack(side="left", pady=30)
    except:
        tk.Label(header, text="☀️\n\nSOLEIL DATABASES", fg="white", bg="#0A4E5C", font=("Century Gothic", 16, "bold")).pack(side="left", padx=25, pady=30)

    btn_cerrar = tk.Button(header, text="CERRAR SESIÓN", bg="#631E26", fg="white", font=("Century Gothic", 10, "bold"), command=cerrar_sesion, relief="flat", padx=16, pady=6, cursor="hand2")
    btn_cerrar.pack(side="right", padx=15, pady=25)

    btn_actividad = tk.Button(header, text="📋 REGISTRO DE ACTIVIDAD", bg="#2E3F3F", fg="white", font=("Century Gothic", 10, "bold"), command=lambda: abrir_registro_actividad(main_win), relief="flat", padx=16, pady=6, cursor="hand2")
    btn_actividad.pack(side="right", padx=5, pady=25)
    
    btn_ayuda_main = tk.Button(header, text="❓ AYUDA", bg="#2E3F3F", fg="white", font=("Century Gothic", 10, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=lambda: mostrar_ayuda(main_win))
    btn_ayuda_main.pack(side="right", padx=5, pady=25)
    
    btn_about_main = tk.Button(header, text="ℹ️ ACERCA DE", bg="#2E3F3F", fg="white", font=("Century Gothic", 10, "bold"), relief="flat", padx=14, pady=6, cursor="hand2", command=lambda: mostrar_acerca_de(main_win))
    btn_about_main.pack(side="right", padx=5, pady=25)

    btn_actividad.bind("<Enter>", lambda e: btn_actividad.config(bg="#405858"))
    btn_actividad.bind("<Leave>", lambda e: btn_actividad.config(bg="#2E3F3F"))
    btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#8A2B35"))
    btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg="#631E26"))
    btn_ayuda_main.bind("<Enter>", lambda e: btn_ayuda_main.config(bg="#405858"))
    btn_ayuda_main.bind("<Leave>", lambda e: btn_ayuda_main.config(bg="#2E3F3F"))
    btn_about_main.bind("<Enter>", lambda e: btn_about_main.config(bg="#405858"))
    btn_about_main.bind("<Leave>", lambda e: btn_about_main.config(bg="#2E3F3F"))
    
    tabs = ttk.Notebook(main_win)
    tab_esp = ModuloCRUD(tabs, "especialidades", ("ID", "Especialidad"), {"nombre": "text"})
    tab_users = ModuloCRUD(tabs, "usuarios", ("ID", "Nombre", "Especialidad"), {"nombre": "text", "esp_id": "especialidades"})
    
    tab_inv = ModuloInventarioMenu(tabs)
    tab_est = ModuloEstadisticas(tabs)

    tabs.add(tab_esp, text="  ESPECIALIDADES  ")
    tabs.add(tab_users, text="  PERSONAL  ")
    tabs.add(tab_inv, text="  INVENTARIO  ")
    tabs.add(tab_est, text="  ESTADÍSTICAS  ")
    tabs.pack(expand=1, fill="both", padx=15, pady=15)
    
    def al_cambiar_pestana(event):
        play_sfx("button_click.ogg")
        widget_actual = tabs.nametowidget(tabs.select())
        if hasattr(widget_actual, 'read'):
            widget_actual.read()
            
    tabs.bind("<<NotebookTabChanged>>", al_cambiar_pestana)

def login():
    play_sfx("button_click.ogg")
    global usuario_actual
    user = e_user.get().strip().lower()
    pas = e_pass.get()
    
    if user in USUARIOS_SISTEMA and USUARIOS_SISTEMA[user]["password"] == pas:
        info_user = USUARIOS_SISTEMA[user]
        usuario_actual = {"username": user, "rol": info_user["rol"], "cargo": info_user["cargo"]}
        try: registrar_evento(f"LOGIN: Acceso concedido a '{user}' como [{info_user['cargo']}].")
        except: pass
            
        play_sfx("session.ogg")
        root.withdraw()
        abrir_sistema()
    else:
        try: registrar_evento(f"ALERTA: Intento de acceso fallido para el usuario: '{user}'.")
        except: pass
        play_sfx("error.ogg")
        messagebox.showerror("Error", "Credenciales incorrectas o nivel de acceso no válido")

# --- LOGIN E INICIO ---
inicializar_db()
root = tk.Tk()
root.title("ACCESO - SOLEIL DATABASES")
root.state("zoomed")
root.resizable(False, False)
root.configure(bg="#0A4E5C")

try:
    ruta_logo = resource_path("soleil.png")
    frame_logo = tk.Frame(root, bg="white", padx=10, pady=10)
    frame_logo.pack(pady=(45, 10))
    
    img_login = tk.PhotoImage(file=ruta_logo).subsample(2, 2)
    tk.Label(frame_logo, image=img_login, bg="white").pack()
except:
    tk.Label(root, text="☀️\n\nSOLEIL DATABASES", fg="white", bg="#0A4E5C", font=("Century Gothic", 18, "bold")).pack(pady=40)

tk.Label(root, text="MANAGEMENT SYSTEM CONTROL", font=("Century Gothic", 9, "bold"), fg="white", bg="#0A4E5C").pack(pady=(0, 30))

tk.Label(root, text="USUARIO:", bg="#0A4E5C", font=("Century Gothic", 9, "bold"), fg="white").pack(pady=(5, 2))
e_user = tk.Entry(root, font=("Century Gothic", 11), justify="center", bd=1, relief="solid", highlightthickness=1, highlightbackground="#CBE0E3", highlightcolor="#148197")
e_user.pack(pady=5, ipady=3, ipadx=10)

tk.Label(root, text="CONTRASEÑA:", bg="#0A4E5C", font=("Century Gothic", 9, "bold"), fg="white").pack(pady=(15, 2))
e_pass = tk.Entry(root, show="*", font=("Century Gothic", 11), justify="center", bd=1, relief="solid", highlightthickness=1, highlightbackground="#CBE0E3", highlightcolor="#148197")
e_pass.pack(pady=5, ipady=3, ipadx=10)

e_user.bind("<Return>", lambda e: login())
e_pass.bind("<Return>", lambda e: login())

btn_acceder = tk.Button(root, text="ACCEDER", command=login, bg="#18331A", fg="white", font=("Century Gothic", 11, "bold"), width=22, relief="flat", pady=12, cursor="hand2")
btn_acceder.pack(pady=20)

btn_acceder.bind("<Enter>", lambda e: btn_acceder.config(bg="#244D27"))
btn_acceder.bind("<Leave>", lambda e: btn_acceder.config(bg="#18331A"))

frame_links_login = tk.Frame(root, bg="#0A4E5C")
frame_links_login.pack(side="bottom", pady=25)

btn_about_login = tk.Button(frame_links_login, text="ℹ️ Acerca de", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "underline", "bold"), relief="flat", cursor="hand2", command=lambda: mostrar_acerca_de(root))
btn_about_login.pack(side="left", padx=15)

btn_ayuda_login = tk.Button(frame_links_login, text="❓ Ayuda / Manual", bg="#0A4E5C", fg="white", font=("Century Gothic", 9, "underline", "bold"), relief="flat", cursor="hand2", command=lambda: mostrar_ayuda(root))
btn_ayuda_login.pack(side="left", padx=15)

e_user.focus_set()
root.eval('tk::PlaceWindow . center')

root.mainloop()
