import socket
import threading
import datetime

class SocketServidor:
    def __init__(self, host="0.0.0.0", puerto=5000):
        self.host = host
        self.puerto = puerto
        self.callback = None
        self.running = False

    def iniciar(self, callback_evento):
        self.callback = callback_evento
        self.running = True
        # Iniciar el servidor en un hilo separado
        hilo = threading.Thread(target=self._escuchar, daemon=True)
        hilo.start()
        print(f"[SERVIDOR] Escuchando en {self.host}:{self.puerto}...")

    def _escuchar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            # Reutilizar puerto para evitar errores de 'Address already in use'
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.host, self.puerto))
            servidor.listen(5)

            while self.running:
                try:
                    conn, addr = servidor.accept()
                    with conn:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            
                            # Mensaje esperado: "PLACA|HORA|CELDA|ESTADO"
                            mensaje = data.decode('utf-8')
                            partes = mensaje.split('|')
                            
                            if len(partes) == 4:
                                placa = partes[0]
                                hora = partes[1]
                                celda = partes[2]
                                estado = partes[3]
                                
                                # SALVAVIDAS: Si la hora viene vacía o mocha desde C++, Python la pone
                                if not hora or hora.strip() == "" or hora == "-1":
                                    hora = datetime.datetime.now().strftime("%H:%M")
                                
                                # Notificar al visualizador a través del callback
                                if self.callback:
                                    self.callback(placa, hora, celda, estado)
                            else:
                                print(f"[ERROR] Mensaje mal formado: {mensaje}")
                except Exception as e:
                    if not self.running:
                        break
                    print(f"[ERROR SOCKET] {e}")

    def detener(self):
        self.running = False
        print("[SERVIDOR] Detenido.")
