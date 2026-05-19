#pragma once

#ifndef SOCKET_CLIENTE_H
#define SOCKET_CLIENTE_H

#include <winsock2.h>
#include <string>

class SocketCliente {
private:
    SOCKET sock;
    WSADATA wsaData;
    bool conectado;

public:
    SocketCliente();
    ~SocketCliente();

    // Establece la conexion con el servidor
    bool conectar(std::string ip, int puerto);

    // Envia un mensaje en formato "PLACA|HORA|CELDA|ESTADO"
    bool enviarMensaje(std::string mensaje);

    // NUEVA: Enlace directo para que main.cpp no saque error en línea roja
    bool enviar(std::string mensaje);

    // Cierra el socket
    void desconectar();

    // NUEVA: Enlace directo para cerrar la conexión al final del main.cpp
    void cerrar();
};

#endif // SOCKET_CLIENTE_H