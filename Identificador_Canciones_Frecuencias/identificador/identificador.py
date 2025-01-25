import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

class IdentificadorDeCanciones:
    def __init__(self, base_datos="assets/base_datos_canciones.pkl"):
        self.base_datos = base_datos
        self.cargar_base_datos()

    def cargar_base_datos(self):
        if os.path.exists(self.base_datos):
            with open(self.base_datos, "rb") as archivo:
                self.huella_digital = pickle.load(archivo)
        else:
            self.huella_digital = {}

    def guardar_base_datos(self):
        with open(self.base_datos, "wb") as archivo:
            pickle.dump(self.huella_digital, archivo)

    def agregar_cancion(self, nombre, signal, fs):
        huella, _, _, _ = self.generar_huella(signal, fs)
        self.huella_digital[nombre] = huella
        self.guardar_base_datos()

    def generar_huella(self, signal, fs):
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)

        ventana_tamaño = 256
        desplazamiento = ventana_tamaño // 2
        espectrograma = []
        ventana_hann = 0.5 * (1 - np.cos(2 * np.pi * np.arange(ventana_tamaño) / (ventana_tamaño - 1)))

        for inicio in range(0, len(signal) - ventana_tamaño, desplazamiento):
            ventana = signal[inicio:inicio + ventana_tamaño] * ventana_hann
            fft = np.fft.fft(ventana)[:ventana_tamaño // 2]
            espectrograma.append(np.abs(fft))

        espectrograma = np.array(espectrograma).T
        tiempos = np.arange(0, espectrograma.shape[1]) * desplazamiento / fs
        frecuencias = np.fft.fftfreq(ventana_tamaño, 1 / fs)[:ventana_tamaño // 2]
        picos = np.argmax(espectrograma, axis=0)
        huella = [(frecuencias[pico], tiempo) for pico, tiempo in zip(picos, tiempos)]
        return huella, espectrograma, frecuencias, tiempos

    def identificar_cancion(self, signal, fs):
        huella_entrada, _, _, _ = self.generar_huella(signal, fs)
        for nombre, huella_guardada in self.huella_digital.items():
            if self.comparar_huellas(huella_entrada, huella_guardada):
                return nombre
        return None

    def comparar_huellas(self, huella1, huella2):
        coincidencias = sum(1 for punto1, punto2 in zip(huella1, huella2) if punto1 == punto2)
        return coincidencias > len(huella1) * 0.8
    
  