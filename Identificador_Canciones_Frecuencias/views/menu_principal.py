import tkinter as tk
from views.agregar_cancion import AgregarCancion
from views.identificar_cancion import IdentificarCancion
from views.lista_canciones import ListaCanciones

class MenuPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(bg="#282c34")
        
        titulo = tk.Label(
            self, 
            text="Menú Principal", 
            font=("Helvetica", 24, "bold"), 
            bg="#282c34", 
            fg="#61dafb"
        )
        titulo.pack(pady=30)

        estilo_boton = {
            "font": ("Helvetica", 14),
            "bg": "#61dafb",
            "fg": "#282c34",
            "activebackground": "#21a1f1",
            "activeforeground": "#ffffff",
            "relief": "raised",
            "bd": 2,
            "width": 20,
            "height": 2
        }
        
        botones = [
            ("Agregar Canción", lambda: self.cambiar_vista(AgregarCancion)),
            ("Identificar Canción", lambda: self.cambiar_vista(IdentificarCancion)),
            ("Lista de Canciones", lambda: self.cambiar_vista(ListaCanciones)),
            ("Salir", parent.quit),
        ]
        
        for texto, comando in botones:
            boton = tk.Button(self, text=texto, command=comando, **estilo_boton)
            boton.pack(pady=10)

    def cambiar_vista(self, vista):
        nueva_vista = vista(self.master)
        nueva_vista.pack(fill="both", expand=True)
        self.destroy()
