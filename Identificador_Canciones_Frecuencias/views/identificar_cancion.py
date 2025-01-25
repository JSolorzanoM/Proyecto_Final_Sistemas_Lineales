import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IdentificarCancion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.identificador = parent.identificador
        self.archivo = None
        self.resultado = None

        self.configure(bg="#282c34")
        parent.geometry("1300x780") 
        parent.title("Identificar Canción")

        tk.Label(
            self,
            text="Identificar Canción",
            font=("Helvetica", 20, "bold"),
            bg="#282c34",
            fg="#61dafb",
        ).pack(pady=20)

        tk.Button(
            self,
            text="Seleccionar Archivo WAV",
            font=("Helvetica", 14),
            bg="#61dafb",
            fg="#282c34",
            activebackground="#21a1f1",
            activeforeground="#ffffff",
            command=self.seleccionar_archivo,
        ).pack(pady=10)

        self.info_label = tk.Label(
            self,
            text="No se ha seleccionado un archivo.",
            font=("Helvetica", 12),
            bg="#282c34",
            fg="white",
        )
        self.info_label.pack(pady=10)

        tk.Button(
            self,
            text="Identificar",
            font=("Helvetica", 14),
            bg="#61dafb",
            fg="#282c34",
            activebackground="#21a1f1",
            activeforeground="#ffffff",
            command=self.identificar_cancion,
        ).pack(pady=10)

        tk.Button(
            self,
            text="Regresar",
            font=("Helvetica", 14),
            bg="#ff6f61",
            fg="#ffffff",
            activebackground="#d9534f",
            activeforeground="#ffffff",
            command=self.regresar_menu,
        ).pack(pady=10)

        self.canvas_frame = tk.Frame(self, bg="#282c34")
        self.canvas_frame.pack(pady=20, fill="both", expand=True)

    def seleccionar_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")])
        if self.archivo:
            self.info_label.config(text=f"Archivo seleccionado: {self.archivo}")

    def identificar_cancion(self):
        if not self.archivo:
            messagebox.showerror("Error", "Selecciona un archivo para identificar.")
            return

        fs, signal = wavfile.read(self.archivo)

        self.resultado = self.identificador.identificar_cancion(signal, fs)

        if self.resultado:
            messagebox.showinfo("Resultado", f"Canción identificada: {self.resultado}")
            
            huella_identificada = self.identificador.huella_digital[self.resultado]
            espectrograma_identificada, frecuencias, tiempos = self.identificador.generar_huella(
                signal, fs)[1:4]  

            self.mostrar_comparacion_espectrograma(espectrograma_identificada, frecuencias, tiempos, huella_identificada, signal, fs)

        else:
            messagebox.showwarning("Resultado", "Canción no identificada en la base de datos.")

    def mostrar_comparacion_espectrograma(self, espectrograma_identificada, frecuencias, tiempos, huella_identificada, signal, fs):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        huella_cargada, espectrograma_cargada, _, _ = self.identificador.generar_huella(signal, fs)

        espectrograma_identificada = np.where(espectrograma_identificada == 0, 1e-10, espectrograma_identificada)
        espectrograma_cargada = np.where(espectrograma_cargada == 0, 1e-10, espectrograma_cargada)

        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        cax1 = axs[0].imshow(
            10 * np.log10(espectrograma_identificada),
            aspect="auto",
            origin="lower",
            extent=[tiempos[0], tiempos[-1], frecuencias[0], frecuencias[-1]],
        )
        axs[0].set_title(f"Espectrograma de: {self.resultado}", fontsize=14)
        axs[0].set_xlabel("Tiempo (s)")
        axs[0].set_ylabel("Frecuencia (Hz)")
        fig.colorbar(cax1, ax=axs[0], label="Intensidad (dB)")

        cax2 = axs[1].imshow(
            10 * np.log10(espectrograma_cargada),
            aspect="auto",
            origin="lower",
            extent=[tiempos[0], tiempos[-1], frecuencias[0], frecuencias[-1]],
        )
        axs[1].set_title("Espectrograma del Archivo Cargado", fontsize=14)
        axs[1].set_xlabel("Tiempo (s)")
        axs[1].set_ylabel("Frecuencia (Hz)")
        fig.colorbar(cax2, ax=axs[1], label="Intensidad (dB)")

        picos_tiempos_identificada = [tiempo for _, tiempo in huella_identificada]
        picos_frecuencias_identificada = [frecuencia for frecuencia, _ in huella_identificada]
        axs[0].scatter(picos_tiempos_identificada, picos_frecuencias_identificada, color="red", s=10, label="Picos Identificados")
        axs[0].legend()

        picos_tiempos_cargada = [tiempo for _, tiempo in huella_cargada]
        picos_frecuencias_cargada = [frecuencia for frecuencia, _ in huella_cargada]
        axs[1].scatter(picos_tiempos_cargada, picos_frecuencias_cargada, color="red", s=10, label="Picos Cargados")
        axs[1].legend()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def regresar_menu(self):
        from views.menu_principal import MenuPrincipal
        nueva_vista = MenuPrincipal(self.master)
        nueva_vista.pack(fill="both", expand=True)
        self.destroy()
