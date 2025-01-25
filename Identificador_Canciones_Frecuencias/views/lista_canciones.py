import tkinter as tk
from tkinter import messagebox


class ListaCanciones(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.identificador = parent.identificador

        parent.geometry("800x600") 
        parent.title("Lista de Canciones")
        self.configure(bg="#282c34")

        tk.Label(
            self,
            text="Lista de Canciones",
            font=("Helvetica", 20, "bold"),
            bg="#282c34",
            fg="#61dafb",
        ).pack(pady=20)

        self.lista = tk.Listbox(
            self, width=50, height=15, font=("Helvetica", 12), bg="#333333", fg="white"
        )
        self.lista.pack(pady=10)

        canciones = self.identificador.huella_digital.keys()
        if canciones:
            for cancion in canciones:
                self.lista.insert(tk.END, cancion)
        else:
            tk.Label(
                self,
                text="No hay canciones en la base de datos.",
                font=("Helvetica", 12),
                bg="#282c34",
                fg="white",
            ).pack(pady=10)


        botones_frame = tk.Frame(self, bg="#282c34")
        botones_frame.pack(pady=10)
        tk.Button(
            botones_frame,
            text="Eliminar Canción",
            font=("Helvetica", 12),
            bg="#ff6f61",
            fg="#ffffff",
            activebackground="#d9534f",
            activeforeground="#ffffff",
            command=self.eliminar_cancion,
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            botones_frame,
            text="Regresar",
            font=("Helvetica", 12),
            bg="#61dafb",
            fg="#282c34",
            activebackground="#21a1f1",
            activeforeground="#ffffff",
            command=self.regresar_menu,
        ).grid(row=0, column=1, padx=10)

    def eliminar_cancion(self):
        seleccion = self.lista.curselection()
        if seleccion:
            cancion_seleccionada = self.lista.get(seleccion)
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de eliminar '{cancion_seleccionada}' de la base de datos?",
            )
            if respuesta:
                del self.identificador.huella_digital[cancion_seleccionada]
                self.identificador.guardar_base_datos()

                self.lista.delete(seleccion)
        else:
            messagebox.showwarning(
                "Selección", "Por favor, selecciona una canción para eliminar."
            )

    

    def regresar_menu(self):
        from views.menu_principal import MenuPrincipal

        nueva_vista = MenuPrincipal(self.master)
        nueva_vista.pack(fill="both", expand=True)
        self.destroy()
