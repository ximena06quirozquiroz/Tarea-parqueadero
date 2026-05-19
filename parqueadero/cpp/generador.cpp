#include "generador.h"
#include <cstdlib>
#include <ctime>
#include <string>

// Genera una placa colombiana aleatoria con iniciales comunes de Medellín/Antioquia
std::string generarPlaca() {
    std::string placa = "";

    // Lista de letras comunes para la primera letra (Medellín y alrededores)
    std::string primerasLetras = "AMKJTIF"; 
    // Letras permitidas para las otras dos posiciones (sin Ñ ni letras extrañas)
    std::string todasLetras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // 1ra Letra (Filtro Medellín)
    placa += primerasLetras[rand() % primerasLetras.length()];

    // 2da y 3ra Letra (Cualquiera del abecedario)
    for (int i = 0; i < 2; i++) {
        placa += todasLetras[rand() % todasLetras.length()];
    }

    placa += "-";

    // 3 dígitos (0-9)
    for (int i = 0; i < 3; i++) {
        char digito = '0' + (rand() % 10);
        placa += digito;
    }

    return placa;
}