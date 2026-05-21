import tkinter as tk
import pyautogui
import threading
import time
import random
from pynput import keyboard


class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AndySniper Clicker")
        self.root.geometry("300x200")

        self.cliqueando = False
        self.tecla_activacion = 'r'

        # Etiqueta de estado
        self.label_estado = tk.Label(
            root, text="Estado: DESACTIVADO", fg="red", font=("Arial", 12, "bold"))
        self.label_estado.pack(pady=10)

        # Entrada para la velocidad
        tk.Label(root, text="Intervalo entre clics (segundos):").pack()
        self.entry_velocidad = tk.Entry(root, justify='center')
        self.entry_velocidad.insert(0, "0.1")
        self.entry_velocidad.pack(pady=5)

        tk.Label(root, text=f"Presiona '{self.tecla_activacion.upper()}' para activar").pack(
            pady=10)

        # Hilo para el clicker
        self.hilo = threading.Thread(target=self.ejecutar_clicker, daemon=True)
        self.hilo.start()

        # Escucha del teclado
        self.listener = keyboard.Listener(on_press=self.al_presionar)
        self.listener.start()

    def al_presionar(self, key):
        try:
            if key.char == self.tecla_activacion:
                self.cliqueando = not self.cliqueando
                self.actualizar_interfaz()
        except AttributeError:
            pass

    def actualizar_interfaz(self):
        if self.cliqueando:
            self.label_estado.config(text="Estado: ACTIVADO", fg="green")
        else:
            self.label_estado.config(text="Estado: DESACTIVADO", fg="red")

    def ejecutar_clicker(self):
        while True:
            if self.cliqueando:
                try:
                    # Obtenemos la velocidad de la interfaz
                    intervalo = float(self.entry_velocidad.get())
                    # Añadimos un pequeño "jitter" aleatorio para evitar detección
                    variacion = intervalo + random.uniform(0, 1)

                    pyautogui.click()
                    time.sleep(variacion)
                except ValueError:
                    time.sleep(1)  # Si el input no es número, espera
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()
