import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AgregarCancion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.identificador = parent.identificador
        self.archivo = None

        self.configure(bg="#282c34")
        parent.geometry("1000x780")
        parent.title("Agregar Canción")

        tk.Label(
            self, text="Agregar Canción", font=("Helvetica", 20, "bold"), bg="#282c34", fg="#61dafb"
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
            self, text="No se ha seleccionado un archivo.", font=("Helvetica", 12), bg="#282c34", fg="white"
        )
        self.info_label.pack(pady=10)

        tk.Label(
            self, text="Nombre de la canción:", font=("Helvetica", 12), bg="#282c34", fg="white"
        ).pack(pady=5)
        self.nombre_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.nombre_entry.pack(pady=5)

        tk.Button(
            self,
            text="Agregar Canción",
            font=("Helvetica", 14),
            bg="#61dafb",
            fg="#282c34",
            activebackground="#21a1f1",
            activeforeground="#ffffff",
            command=self.agregar_cancion,
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
            fs, signal = wavfile.read(self.archivo)

            huella, espectrograma, frecuencias, tiempos = self.identificador.generar_huella(signal, fs)

            self.mostrar_espectrograma(espectrograma, frecuencias, tiempos, huella, signal, fs)

    def mostrar_espectrograma(self, espectrograma, frecuencias, tiempos, huella, signal, fs):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        espectrograma = np.where(espectrograma == 0, 1e-10, espectrograma)

        fig, axs = plt.subplots(3, 1, figsize=(10, 12))

        # Espectrograma
        cax = axs[0].imshow(
            10 * np.log10(espectrograma),
            aspect='auto',
            origin='lower',
            extent=[tiempos[0], tiempos[-1], frecuencias[0], frecuencias[-1]],
        )
        axs[0].set_title("Espectrograma de la Canción", fontsize=14)
        axs[0].set_xlabel("Tiempo (s)", fontsize=12)
        axs[0].set_ylabel("Frecuencia (Hz)", fontsize=12)
        fig.colorbar(cax, ax=axs[0], label="Intensidad (dB)")

        picos_tiempos = [tiempo for _, tiempo in huella]
        picos_frecuencias = [frecuencia for frecuencia, _ in huella]
        axs[0].scatter(picos_tiempos, picos_frecuencias, color="red", s=10, label="Picos")
        axs[0].legend(fontsize=10)

        if signal.ndim > 1:
            signal_mono = np.mean(signal, axis=1)
        else:
            signal_mono = signal
        # Dominio de la frecuencia
        N = len(signal)
        fft_signal = np.fft.fft(signal_mono)
        freqs = np.fft.fftfreq(N, 1 / fs)
        
        # Limitar las frecuencias de 0 a 10000 Hz
        mask = (freqs >= 0) & (freqs <= 10000)
        freqs = freqs[mask]
        fft_signal = fft_signal[mask]
        
        axs[1].plot(freqs, np.abs(fft_signal), label="Original (FFT)", color="orange")
        axs[1].set_title("Dominio de la Frecuencia", fontsize=14)
        axs[1].set_xlabel("Frecuencia (Hz)", fontsize=12)
        axs[1].set_ylabel("Magnitud", fontsize=12)
        axs[1].legend(fontsize=10)
        axs[1].grid()

        # Dominio del tiempo
        time = np.arange(len(signal_mono)) / fs
        axs[2].plot(time, signal_mono, label="Señal Original", color="blue")
        axs[2].set_title("Dominio del Tiempo", fontsize=14)
        axs[2].set_xlabel("Tiempo (s)", fontsize=12)
        axs[2].set_ylabel("Amplitud", fontsize=12)
        axs[2].legend(fontsize=10)
        axs[2].grid()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def agregar_cancion(self):
        if not self.archivo:
            messagebox.showerror("Error", "Selecciona un archivo.")
            return

        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingresa un nombre para la canción.")
            return

        fs, signal = wavfile.read(self.archivo)
        self.identificador.agregar_cancion(nombre, signal, fs)

        messagebox.showinfo("Éxito", f"Canción '{nombre}' agregada correctamente.")
        self.regresar_menu()

    def regresar_menu(self):
        from views.menu_principal import MenuPrincipal
        nueva_vista = MenuPrincipal(self.master)
        nueva_vista.pack(fill="both", expand=True)
        self.destroy()
