from tkinter import Tk
from identificador.identificador import IdentificadorDeCanciones
from views.menu_principal import MenuPrincipal

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Identificador de Canciones")
        self.geometry("600x400")

        self.identificador = IdentificadorDeCanciones()

        self.menu_principal = MenuPrincipal(self)
        self.menu_principal.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
