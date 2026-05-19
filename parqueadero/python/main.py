import os
# Asegúrate de poner exactamente el mismo nombre aquí
os.add_dll_directory(r"D:\Escritorio\SimuladorParqueadero\parqueadero\cpp")

import tkinter as tk
from socket_servidor import SocketServidor
from libreria_bridge import LibreriaBridge
from visualizador import Visualizador

def main():
    print("--- INICIANDO SISTEMA DE PARQUEADERO (SERVIDOR PYTHON) ---")
    
    # 1. Inicializar la conexion con la DLL de C++
    try:
        bridge = LibreriaBridge()
        bridge.inicializar()
        print("[BRIDGE] DLL de C++ cargada e inicializada correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar la DLL: {e}")
        return

    # 2. Crear la ventana principal de Tkinter (Estilo Negro Cyberpunk)
    root = tk.Tk()
    root.title("Sistema de Parqueadero — En vivo")
    root.configure(bg="#0a0a0c") # Fondo exterior negro para que combine con el neón
    
    app = Visualizador(root, bridge)

    # 3. Definir que hacer cuando llegue un mensaje por socket
    def callback_nuevo_mensaje(placa, hora, celda, estado):
        # Esta funcion corre en el hilo del socket.
        # Para actualizar la UI de Tkinter de forma segura, usamos root.after()
        root.after(0, app.agregar_evento, placa, hora, celda, estado)

    # 4. Iniciar el servidor socket
    servidor = SocketServidor()
    servidor.iniciar(callback_nuevo_mensaje)

    # 5. Loop principal de la interfaz
    try:
        root.mainloop()
    finally:
        # Limpieza al cerrar
        print("Cerrando servidor...")
        servidor.detener()

if __name__ == "__main__":
    main()