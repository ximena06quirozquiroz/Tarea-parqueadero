# Tarea-parqueadero
 Sistema de Gestión de Parqueadero 

Este proyecto es un sistema de parqueadero distribuido y optimizado que utiliza **C++** para la lógica de bajo nivel, sockets y simulación, y **Python** para la interfaz gráfica de usuario en tiempo real.

## Requisitos
* **Compilador C++**: g++ (MinGW-w64) instalado en el PATH del sistema.
* **Python 3.x**: Instalado en el sistema (con la librería Tkinter activa).
* **Conexión de Red**: Protocolo TCP/IP a través de Sockets (Puerto 5000).

---

## Guía de Configuración e Inicio

### Paso 1: Compilación del Motor C++
Para compilar los cambios de la lógica y generar los archivos del puente:
1. Abre la terminal en la carpeta `parqueadero/cpp/`.
2. Compila el código usando el comando de g++ (esto actualizará la lógica a las celdas reglamentarias y generará el ejecutable `autoparking.exe`).

### Paso 2: Ejecutar la Interfaz Gráfica (Servidor Python)
Este componente levanta el servidor de datos y pinta el entorno visual.
1. En el explorador de VS Code, ve a la carpeta `parqueadero/python/`.
2. Abre el archivo `main.py` y dale al botón de **Play** (triángulo arriba a la derecha).
3. Verás en la consola el mensaje: `[BRIDGE] DLL de C++ cargada e inicializada correctamente.` seguido de `Servidor Python escuchando en el puerto 5000...`

### Paso 3: Conectar el Simulador (Cliente C++)
Este programa simula el flujo vehicular enviando datos en vivo por sockets.
1. En la terminal de la carpeta `cpp`, ejecuta el simulador con:
    ```bash
    .\autoparking.exe
    ```
2. Cuando el sistema solicite la IP, ingresa la dirección local `127.0.0.1` para conectar de inmediato.

---

## Interfaz Gráfica Custom (Visualizador Cyberpunk)
La interfaz fue rediseñada desde cero con un estilo neón personalizado:
* **Estructura Sincronizada**: Grilla exacta de **27 celdas** distribuidas simétricamente en 3 filas de 9 columnas.
* **Celda en Gris Oscuro (Borde Morado)**: Estado **LIBRE**.
* **Celda en Fucsia Neón Brillante**: Estado **OCUPADA** (Muestra la placa del vehículo en tiempo real).
* **Historial de Eventos**: Tabla inferior que registra de manera síncrona la Hora exacta, Placa, Celda y el Tipo de Evento (ENTRADA/SALIDA).

## Estructura del Proyecto
* `cpp/`: Cliente socket, generador aleatorio de placas colombianas y wrapper de la DLL.
