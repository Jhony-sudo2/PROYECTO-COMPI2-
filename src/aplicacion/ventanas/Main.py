import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from src.aplicacion.querys import Usar
from src.parser.lexer import lexer
from src.parser.parser import parser
from Analizador import Analizador
from src.parser.parser import parsererror

db = ''
def ejecutar_consulta():
    global db

    analizador = Analizador("parser")
    analizador.escribir()
    consola.delete("1.0", END)
    texto = campo_texto.get("1.0", END).strip()
    print("**********la db select es " + db)
    try:
        s = texto
        result = parser.parse(s, lexer=lexer)
        print(parser)
        print(len(parsererror))
        if len(parsererror) !=0 and len(parsererror[0]) != 0:
            consola.insert(END,parsererror[0])
            parsererror.clear()
        else:
            salida = ''
            for elemento in result:
                elemento.ejecutar(db)
                if len(elemento.errores) != 0:
                    salida += elemento.errores
                if hasattr(elemento,'resultado'):
                    if len(elemento.resultado) !=0:
                        salida += str(elemento.resultado)
                if hasattr(elemento,'nueva'):
                    db = elemento.nueva
            print('la nueva db es',db)
            consola.insert(END,salida)
        cargar_carpetas()
        cargarArbol(db)
    except EOFError:
        print("Error")

def abrir_archivo():
    # Abre el cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename()
    # Verifica si se seleccionó un archivo
    if archivo:
        # Lee el contenido del archivo
        with open(archivo, 'r') as file:
            contenido = file.read()

        # Borra el contenido actual del campo de texto
        campo_texto.delete(1.0, END)

        # Inserta el nuevo contenido en el campo de texto
        campo_texto.insert(END, contenido)

        # Muestra la ruta del archivo seleccionado en la etiqueta
        etiqueta_archivo.config(text="Archivo seleccionado: " + archivo)

def cargar_carpetas():
    # Especifica la ruta del directorio que contiene las carpetas
    ruta_directorio = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'databases'))
    carpetas = [nombre for nombre in os.listdir(ruta_directorio) if
                os.path.isdir(os.path.join(ruta_directorio, nombre))]

    # Añade las carpetas al menú desplegable
    menu_desplegable['values'] = tuple(carpetas)

def seleccionar_carpeta( event):
    global db
    carpeta_seleccionada = menu_desplegable.get()
    db = carpeta_seleccionada
    print(f"Se seleccionó la carpeta: {carpeta_seleccionada} y es {db}")
    cargarArbol(carpeta_seleccionada)

def cargarArbol(carpeta_seleccionada):
    arbol.delete(*arbol.get_children())
    db3 = arbol.insert("", "end", text=carpeta_seleccionada)
    ruta_directorio = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'databases', carpeta_seleccionada + '/Tables'))
    carpetas = [nombre for nombre in os.listdir(ruta_directorio) if
                os.path.isdir(os.path.join(ruta_directorio, nombre))]
    for carpeta in carpetas:
        sub = arbol.insert(db3, "end", text=carpeta)
        ruta_carpeta = ruta_directorio + "/" + carpeta
        archivos = [nombre for nombre in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, nombre))]
        # Añadir los archivos al Treeview



# Importamos una ventana
aplicacion = Tk()

etiqueta_archivo = Label(aplicacion, text="Archivo seleccionado: ")
etiqueta_archivo.pack(pady=10)

# Tamaño de la ventana
aplicacion.geometry('1200x800+100+50')

# Evitar la maximización
aplicacion.resizable(0, 0)

# Definir título
aplicacion.title("XSQL-IDE")

# Panel superior Barra
panel_superior = Frame(aplicacion, bd=1, relief=FLAT)
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
aplicacion.config(menu=barra_menu)
# -------------------------------------------
# Panel izquierdo Arbol
panel_izquierdo = Frame(aplicacion, bd=1, relief=FLAT, width=200, height=2)
panel_izquierdo.pack(side=LEFT, fill=Y)

# Crear un menú desplegable para seleccionar db
db_label = Label(panel_izquierdo, text="Base de datos: ", width=18)
db_label.pack()
menu_desplegable = ttk.Combobox(panel_izquierdo, state="readonly", width=18)
menu_desplegable.pack(pady=10)
cargar_carpetas()
menu_desplegable.bind("<<ComboboxSelected>>", seleccionar_carpeta)
db = menu_desplegable.get()

# Crear el árbol de bases de datos
arbol = ttk.Treeview(panel_izquierdo)
arbol.pack(side=LEFT, fill=Y, anchor=CENTER)

# ----------------------------------------------------------------------------------------
# Panel central
panel_central = Frame(aplicacion, bd=1, relief=FLAT)
panel_central.pack(side=TOP, fill=Y)

# Panel interno central- Querys
panel_querys = Frame(panel_central, bd=1, relief=FLAT)
panel_querys.pack(side=TOP)

# Panel interno central- editor
panel_editor = Frame(panel_central, bd=1, relief=FLAT)
panel_editor.pack()

# Crear el campo de texto para la consulta
campo_texto = Text(panel_editor, height=20, width=90)
campo_texto.pack()

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
consola = Text(panel_consola,  height=10, width=90)
consola.pack()

aplicacion.mainloop()