#ifndef PARQUEADERO_H
#define PARQUEADERO_H

#include <string>
#include <map>

// Numero total de celdas del parqueadero (¡Cambiado a 27 para tu proyecto!)
const int TOTAL_CELDAS = 27;

// Estructura que representa una celda del parqueadero
struct Celda {
    bool ocupada;
    std::string placa;
    std::string horaIngreso;
};

class Parqueadero {
private:
    Celda celdas[TOTAL_CELDAS];              // Arreglo de 27 celdas (indices 0-26, representan celdas 1-27)
    std::map<std::string, int> placaACelda;            // Mapa: placa -> indice de celda

    // Obtiene la hora actual en formato HH:MM:SS
    std::string obtenerHoraActual();

public:
    // Constructor: inicializa todas las celdas como libres
    Parqueadero();

    // Registra o retira un vehiculo:
    // - Si la placa NO existe: asigna primera celda libre, devuelve celda y hora
    // - Si la placa YA existe: libera la celda, devuelve celda liberada
    // Retorna true si se registro (ingreso), false si se retiro (salida)
    bool registrarPlaca(std::string placa, std::string& celda, std::string& hora);

    // Devuelve un string con el estado completo de las celdas
    std::string obtenerEstado();

    // Devuelve el estado simplificado: "1,0,1,..." para la DLL
    std::string obtenerEstadoRaw();
};

#endif // PARQUEADERO_H