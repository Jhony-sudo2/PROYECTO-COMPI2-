import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from src.aplicacion.ventanas.reportes.TablaSimbolos import TablaApp
from src.parser.lexer import lexer
from src.parser.parser import parser
from Analizador import Analizador
from src.parser.parser import parsererror

reservadas = {
    # BASE DE DATOS DDL
    'USAR': 'USAR',
    'CREATE': 'CREATE',
    'DATA': 'DATA',
    'BASE': 'BASE',
    'ALTER': 'ALTER',
    'TABLE': 'TABLE',
    'TRUNCATE': 'TRUNCATE',
    'NOT': 'NOT',
    'NULL': 'NULL',
    'DELETE': 'DELETE',
    'FROM': 'FROM',
    'SET': 'SET',

    # DML
    'UPDATE': 'UPDATE',
    'SELECT': 'SELECT',
    'INSERT': 'INSERT',
    'INTO': 'INTO',
    'VALUES': 'VALUES',
    'PRIMARY': 'PRIMARY',
    'KEY': 'KEY',
    'REFERENCE': 'REFERENCES',
    'DATE': 'DATE',
    'DATETIME': 'DATETIME',
    'INT': 'INT',
    'DECIMAL': 'DECIMAL',
    'BOOLEAN': 'BOOL',
    'NVARCHAR': 'NVARCHAR',
    'NCHAR': 'NCHAR',

    # FUNCIONES DEL SISTEMA:
    'CONCATENA': 'CONCATENA',
    'SUBSTRAER': 'SUBSTRAER',
    'HOY': 'HOY',
    'CONTAR': 'CONTAR',
    'SUMA': 'SUMA',
    'CAST': 'CAST',

    # ALTER
    'ADD': 'ADD',
    'COLUMN': 'COLUMN',
    'DROP': 'DROP',

    # TRUNCATE
    'TRUNCATE': 'TRUNCATE',

    # SSL
    'IF': 'IF',
    'ELSE': 'ELSE',
    'AS': 'AS',
    'PROCEDURE': 'PROCEDURE',
    'where': 'where',
    'WHERE': 'WHERE',
    'WHILE': 'WHILE',
    'EXEC': 'EXEC',

    # FUNCIONES
    'FUNCTION': 'FUNCTION',
    'RETURN': 'RETURN',
    'BEGIN': 'BEGIN',
    'END': 'END',
    'DECLARE': 'DECLARE',
}

class LineNumbers(tk.Text):
    def __init__(self, master, *args, **kwargs):
        tk.Text.__init__(self, master, *args, **kwargs)
        self.config(state="disabled", width=4)
        self.insert("1.0", "1")

    def update_line_numbers(self):
        lines = int(self.index(tk.END).split(".")[0])
        line_numbers = "\n".join(str(i) for i in range(1, lines + 1))
        self.config(state="normal")
        self.delete("1.0", tk.END)
        self.insert("1.0", line_numbers)
        self.config(state="disabled")

class CustomLexer:
    def __init__(self):
        self.keywords = set(reservadas.values())
        #self.keywords_lower = set(keyword.lower() for keyword in self.keywords)

    def lex(self, code):
        for token, value in self.tokenize(code.upper()):
            yield token, value

    def tokenize(self, code):
        start = 0
        while start < len(code):
            while start < len(code) and code[start].isspace():
                start += 1
            if start >= len(code):
                break

            end = start + 1
            while end < len(code) and not code[end].isspace():
                end += 1

            value = code[start:end]
            token = 'Token.Keyword' if value in  self.keywords else 'Token.Text'
            yield token, value

            start = end

class SyntaxHighlightingText(scrolledtext.ScrolledText):
    def __init__(self, master=None, lexer=None,line_numbers=None, **kwargs):
        scrolledtext.ScrolledText.__init__(self, master, **kwargs)
        self.lexer = lexer
        self.line_numbers = line_numbers
        self.tag_configure("Token.Keyword", foreground="blue")
        self.tag_configure("Token.Text", foreground="black")  # Puedes ajustar el color según tus necesidades

        self.bind("<Control-v>", self.highlight)
        self.bind("<KeyRelease>", self.highlight)
        self.bind("<Key>", self.handle_key_event)
        self.after(500, self.periodic_highlight_check)
        self.bind("<Configure>", self.update_line_numbers)


    def highlight(self, event):
        current_position = self.index(tk.INSERT)
        current_line = current_position.split(".")[0]

        line_number, column = map(int, current_position.split("."))
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"

        line = self.get(line_start, line_end)
        self.tag_remove("Token.Keyword", line_start, line_end)
        self.tag_remove("Token.Text", line_start, line_end)

        for token, value in self.lexer.tokenize(line):
            start = f"{line_number}.{line.find(value)}"
            end = f"{line_number}.{line.find(value) + len(value)}"

            if token == 'Token.Keyword':
                self.tag_add(token, start, end)
            self.tag_add(token, start, end)
        self.line_numbers.update_line_numbers()
    def update_line_numbers(self, event):
        self.line_numbers.update_line_numbers()

    def insert_text(self, text):
        current_position = self.index(tk.INSERT)
        self.insert(tk.INSERT, text)
        self.highlight(None)  # Vuelve a resaltar después de la inserción
        self.mark_set(tk.INSERT, current_position)  # Restaura la posición del cursor

    def handle_key_event(self, event):
        if event.char and event.keysym not in ["BackSpace", "Delete"]:
            self.after(10, self.highlight, None)

    def periodic_highlight_check(self):
        self.highlight(None)
        self.after(5000, self.periodic_highlight_check)
class TextEditorApp():
    db = ''
    funciones = []
    def __init__(self, master):
        self.master = master
        self.master.title("XSQL-IDE")

        self.custom_lexer = CustomLexer()

        def ejecutar_consulta():
            global db
            global funciones
            consola.delete("1.0", END)
            texto = self.editor.get("1.0", END).strip()
            # print("**********la db select es " + db)
            db = self.db
            # if  self.db:
            try:
                lexer.lineno = 0
                s = texto
                result = parser.parse(s, lexer=lexer)
                if parsererror:
                    errores = ''
                    for r in parsererror:
                        errores += r + '\n'
                    consola.insert(END, errores)
                    parsererror.clear()
                else:
                    salida = ''
                    for elemento in result:
                        if hasattr(elemento, 'tablafunciones'):
                            elemento.tablafunciones = self.funciones
                        elemento.ejecutar(db)
                        if len(elemento.errores) != 0:
                            salida += elemento.errores
                        if hasattr(elemento, 'resultado'):
                            if len(elemento.resultado) != 0:
                                salida += str(elemento.resultado)
                        if hasattr(elemento, 'nueva'):
                            db = elemento.nueva
                    consola.insert(END, salida)
                cargar_carpetas()
                cargarArbol(db)
                self.reporte(self.funciones)
            except EOFError:
                print("Error")
            # else:
            #   consola.insert(END, 'NO HAY NINGUNA BASE DE DATOS SELECCIONADA')

        def abrir_archivo():
            # Abre el cuadro de diálogo para seleccionar un archivo
            archivo = filedialog.askopenfilename()
            # Verifica si se seleccionó un archivo
            if archivo:
                # Lee el contenido del archivo
                with open(archivo, 'r') as file:
                    contenido = file.read()

                # Borra el contenido actual del campo de texto
                self.editor.delete(1.0, END)

                # Inserta el nuevo contenido en el campo de texto
                self.editor.insert(END, contenido)

                # Muestra la ruta del archivo seleccionado en la etiqueta
                etiqueta_archivo.config(text="Archivo seleccionado: " + archivo)

        def cargar_carpetas():
            # Especifica la ruta del directorio que contiene las carpetas
            ruta_directorio = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'databases'))
            carpetas = [nombre for nombre in os.listdir(ruta_directorio) if
                        os.path.isdir(os.path.join(ruta_directorio, nombre))]

            # Añade las carpetas al menú desplegable
            menu_desplegable['values'] = tuple(carpetas)

        def seleccionar_carpeta(event):
            global db
            carpeta_seleccionada = menu_desplegable.get()
            self.db = carpeta_seleccionada
            print(f"Se seleccionó la carpeta: {carpeta_seleccionada} y es {self.db}")
            cargarArbol(carpeta_seleccionada)

        def cargarArbol(carpeta_seleccionada):
            arbol.delete(*arbol.get_children())
            db3 = arbol.insert("", "end", text=carpeta_seleccionada)
            ruta_directorio = os.path.abspath(
                os.path.join(os.getcwd(), '..', '..', 'databases', carpeta_seleccionada + '/Tables'))
            carpetas = [nombre for nombre in os.listdir(ruta_directorio) if
                        os.path.isdir(os.path.join(ruta_directorio, nombre))]
            for carpeta in carpetas:
                sub = arbol.insert(db3, "end", text=carpeta)
                ruta_carpeta = ruta_directorio + "/" + carpeta
                archivos = [nombre for nombre in os.listdir(ruta_carpeta) if
                            os.path.isfile(os.path.join(ruta_carpeta, nombre))]
                # Añadir los archivos al Treeview

        # Importamos una ventana
        #aplicacion = Tk()

        etiqueta_archivo = Label(self.master, text="Archivo seleccionado: ")
        etiqueta_archivo.pack(pady=10)

        # Tamaño de la ventana
        self.master.geometry('1650x900+100+50')

        # Evitar la maximización
        self.master.resizable(0, 0)

        # Definir título
        self.master.title("XSQL-IDE")

        # Panel superior Barra
        panel_superior = Frame(self.master, bd=1, relief=FLAT)
        panel_superior.pack(side=TOP)

        # Crear la barra de menú
        barra_menu = Menu(panel_superior)
        archivo_menu = Menu(barra_menu, tearoff=0)
        archivo_menu.add_command(label="Nuevo")
        archivo_menu.add_command(label="Abrir", command=abrir_archivo)
        archivo_menu.add_command(label="Guardar")
        archivo_menu.add_command(label="Guardar como")
        archivo_menu.add_command(label="Cerrar")
        barra_menu.add_cascade(label="Archivo", menu=archivo_menu)

        barra_menu.add_cascade(label="Herramientas", menu=archivo_menu)
        self.master.config(menu=barra_menu)
        # -------------------------------------------
        # Panel izquierdo Arbol
        panel_izquierdo = Frame(self.master, bd=1, relief=FLAT, width=200, height=2)
        panel_izquierdo.pack(side=LEFT, fill=Y)

        # Crear un menú desplegable para seleccionar db
        db_label = Label(panel_izquierdo, text="Base de datos: ", width=18)
        db_label.pack()
        menu_desplegable = ttk.Combobox(panel_izquierdo, state="readonly", width=18)
        menu_desplegable.pack(pady=10)
        cargar_carpetas()
        menu_desplegable.bind("<<ComboboxSelected>>", seleccionar_carpeta)
        self.db = menu_desplegable.get()

        # Crear el árbol de bases de datos
        arbol = ttk.Treeview(panel_izquierdo)
        arbol.pack(side=LEFT, fill=Y, anchor=CENTER)

        # ----------------------------------------------------------------------------------------
        # Panel central
        panel_central = Frame(self.master, bd=1, relief=FLAT)
        panel_central.pack(side=TOP, fill=Y)

        # Panel interno central- Querys
        panel_querys = Frame(panel_central, bd=1, relief=FLAT)
        panel_querys.pack(side=TOP)

        # Panel interno central- editor
        panel_editor = Frame(panel_central, bd=1, relief=FLAT)
        panel_editor.pack()

        # Crear el campo de texto para la consulta
        # campo_texto = Text(panel_editor, height=20, width=90)
        # campo_texto.pack()
        self.custom_lexer = CustomLexer()


        self.line_numbers = LineNumbers(panel_editor, wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.editor = SyntaxHighlightingText(panel_editor, lexer=self.custom_lexer, wrap=tk.WORD,
                                             line_numbers=self.line_numbers, height=5, width=120)
        self.editor.pack(expand=True, fill='both')

        # Panel interno central- button
        panel_buton = Frame(panel_central, bd=1, relief=FLAT)
        panel_buton.pack()
        # Crear el botón para ejecutar la consulta
        boton = Button(panel_buton, text="Ejecutar consulta", command=ejecutar_consulta)
        boton.pack()

        # Panel interno central- consola
        panel_consola = Frame(panel_central, bd=1, relief=FLAT)
        panel_consola.pack(side=TOP)

        # Crear el campo de texto para la consola
        consola = Text(panel_consola, height=10, width=120)
        consola.pack()
    def reporte(self,tabla):
        root = tk.Tk()
        app = TablaApp(root)
        app.agregar_datos(tabla)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
