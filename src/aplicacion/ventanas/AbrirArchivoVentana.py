from tkinter import filedialog
from tkinter import *

def abrir_archivo():
    # Abre el cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename()

    # Muestra la ruta del archivo seleccionado en la etiqueta
    etiqueta_archivo.config(text="Archivo seleccionado: " + archivo)

# Crear la ventana principal
ventana = Tk()
ventana.title("Abrir Archivo")

# Crear una etiqueta para mostrar la ruta del archivo seleccionado
etiqueta_archivo = Label(ventana, text="Archivo seleccionado: ")
etiqueta_archivo.pack(pady=10)

# Crear un botón para abrir el cuadro de diálogo
boton_abrir = Button(ventana, text="Abrir Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
