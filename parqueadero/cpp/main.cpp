#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include "generador.h"
#include "parqueadero.h"
#include "socket_cliente.h"

using namespace std;

int main() {
    srand(time(0));
    
    string ipServidor;
    cout << "============================================" << endl;
    cout << "      AUTOPARKING - CLIENTE C++" << endl;
    cout << "============================================" << endl;
    cout << "Ingrese la IP del servidor (Computador 2): ";
    cin >> ipServidor;

    Parqueadero parking;
    SocketCliente cliente;

    if (!cliente.conectar(ipServidor, 5000)) {
        cout << "[ERROR] No se pudo establecer conexion inicial con el servidor." << endl;
        cout << "Asegurese de que el servidor Python este corriendo y la IP sea correcta." << endl;
        return 1;
    }

    cout << "\nIniciando simulacion automatica (Asignacion Aleatoria)..." << endl;
    cout << "Presione Ctrl+C para detener." << endl;
    cout << "--------------------------------------------" << endl;

    while (true) {
        string placa = generarPlaca();
        
        string celda, hora;
        bool esIngreso = parking.registrarPlaca(placa, celda, hora);
        string estadoStr = esIngreso ? "ENTRADA" : "SALIDA";

        if (esIngreso && celda == "-1") {
            cout << "[LLENO] Intento de ingreso: " << placa << " - Sin espacio disponible." << endl;
        } else {
            cout << "[" << estadoStr << "] Placa: " << placa 
                 << " | Celda Asignada: " << celda 
                 << " | Hora: " << hora << endl;

            string mensaje = placa + "|" + hora + "|" + celda + "|" + estadoStr;
            cliente.enviar(mensaje); 
        }

        int espera = 2 + (rand() % 4); 
        this_thread::sleep_for(chrono::seconds(espera));
    }

    return 0;
}