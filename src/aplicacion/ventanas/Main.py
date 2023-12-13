from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from Analizador import Analizador

def ejecutar_consulta():
    analizador = Analizador("parser")
    analizador.escribir()
    consola.delete("1.0", END)
    texto = campo_texto.get("1.0", END)  # Obtener el texto del campo
    print(texto)
    consola.insert(END, texto)
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


#imortamos una ventana
aplicacion= Tk()

etiqueta_archivo = Label(aplicacion, text="Archivo seleccionado: ")
etiqueta_archivo.pack(pady=10)

#tamaño de la ventana
aplicacion.geometry('1020x630+0+0')

#evitar la maximizacib
aplicacion.resizable(0,0)

#def titulo
aplicacion.title("XSQL-IDE")

#panele superior Barra
panel_superior= Frame(aplicacion, bd=1, relief=FLAT)
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
#-------------------------------------------
#panele izquierdo Arbol
panel_izquierdo= Frame(aplicacion, bd=1, relief=FLAT)
panel_izquierdo.pack(side=LEFT)

# Crear el árbol de bases de datos
arbol = ttk.Treeview(panel_izquierdo)
arbol.pack(side=LEFT, fill=Y)

# Agregar algunas bases de datos y tablas al árbol
db1 = arbol.insert("", "end", text="Base de datos 1")
arbol.insert(db1, "end", text="Tabla 1")
arbol.insert(db1, "end", text="Tabla 2")

db2 = arbol.insert("", "end", text="Base de datos 2")
arbol.insert(db2, "end", text="Tabla 3")
arbol.insert(db2, "end", text="Tabla 4")
#----------------------------------------------------------------------------------------
#panele central
panel_central= Frame(aplicacion, bd=1, relief=FLAT)
panel_central.pack(side=RIGHT)

#panele interno central- Querys
panel_querys= Frame(panel_central, bd=1, relief=FLAT)
panel_querys.pack(side=TOP)

#panele intreno central- editor
panel_editor= Frame(panel_central, bd=1, relief=FLAT)
panel_editor.pack()

# Crear el campo de texto para la consulta
campo_texto = Text(panel_editor)
campo_texto.pack()

#panele interno central- button
panel_buton= Frame(panel_central, bd=1, relief=FLAT)
panel_buton.pack()
# Crear el botón para ejecutar la consulta
boton = Button(panel_buton, text="Ejecutar consulta", command= ejecutar_consulta)
boton.pack()

#panele intreno central- consola
panel_consola= Frame(panel_central, bd=1, relief=FLAT)
panel_consola.pack(side=TOP)

# Crear el campo de texto para la consola
consola = Text(panel_consola)
consola.pack()


aplicacion.mainloop()