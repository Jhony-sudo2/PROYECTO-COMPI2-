import tkinter as tk
from tkinter import ttk

class TablaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla simbolos")

        # Crear una tabla usando ttk.Treeview
        self.tabla = ttk.Treeview(root)
        self.tabla["columns"] = ("ID", "Nombre", "Edad")

        # Configurar las columnas
        self.tabla.column("#0", width=0, stretch=tk.NO)  # Columna oculta
        self.tabla.column("ID", anchor=tk.W, width=100)
        self.tabla.column("Nombre", anchor=tk.W, width=100)
        self.tabla.column("Edad", anchor=tk.W, width=100)

        # Encabezados de las columnas
        self.tabla.heading("#0", text="", anchor=tk.W)
        self.tabla.heading("ID", text="Nombre", anchor=tk.W)
        self.tabla.heading("Nombre", text="Tipo", anchor=tk.W)
        self.tabla.heading("Edad", text="Valor", anchor=tk.W)

        # Agregar datos a la tabla

        # Empaquetar la tabla
        self.tabla.pack()

    def agregar_datos(self,funciones):
        datos = []
        if len(funciones) != 0:
            for funcion in funciones:
                if len(funcion.tablasimbolos) != 0:
                    tabla = funcion.tablasimbolos
                    for tabla in tabla:
                        tmp = (tabla.nombre,tabla.tipo,tabla.valor)
                        datos.append(tmp)

        # Agregar datos a la tabla
        for dato in datos:
            self.tabla.insert("", "end", values=dato)


