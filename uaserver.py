#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os
from lxml import etree
import time


try:
    CONFIG = sys.argv[1]
    open(CONFIG)
except:
    sys.exit("Usage: python uaserver.py config")


# Creamos nuestra estructura de datos ElementTree
doc = etree.parse(CONFIG)

# Obtenemos nuestros elementos que forman ElementTree
elementos = doc.getroot()

# Obtenemos nuestras variables
account = elementos[0].attrib
username = account.get("username")
passwd = account.get("passwd")

uaserver = elementos[1].attrib
ipServer = uaserver.get("ip")
portServer = uaserver.get("puerto")

rtpaudio = elementos[2].attrib
portRtp = rtpaudio.get("puerto")

regproxy = elementos[3].attrib
ipProxy = regproxy.get("ip")
portProxy = regproxy.get("puerto")

log = elementos[4].attrib
pathLog = log.get("path")

audio = elementos[5].attrib
pathAudio = audio.get("path")

print("-----------\r\n")


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    METHOD_CLASS = ['INVITE', 'ACK', 'BYE']
    IpClient = []
    PortClient = []

    def handle(self):
        while 1:

            line = self.rfile.read()
            if not line:
                break
            M_Recieve = line.decode('utf-8')
            print("El cliente nos manda:\r\n" + M_Recieve)
            print("-----------\r\n")
            Line = M_Recieve.split('\r\n')
            Package = Line[0].split(' ')
            METODO = Package[0]
            OPCION = Package[1].split(':')[1]

            if METODO == 'INVITE':
                print(Line)
                IpClient = Line[5].split(' ')[1]

                Message = ("SIP/2.0 100 Trying\r\n\r\n" +
                           "SIP/2.0 180 Ring\r\n\r\n" +
                           "SIP/2.0 200 OK\r\n\r\n" +
                           "Content-Type: application/sdp\r\n\r\n" +
                           "v=0\r\n" + "o=" + username + " " + ipServer +
                           "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m=" +
                           str(elementos[5].tag) + " " + portRtp + " RTP")

                self.wfile.write(bytes(Message, 'utf-8') + b'\r\n')
                print("Enviando:\r\n" + Message)
                print("-----------\r\n")

            elif METODO == 'ACK':
                # aEjecutar es un string con lo que se ha de ejecutar en shell
                aEjecutar = "./mp32rtp -i " + ipServer + " -p " + portRtp
                aEjecutar += " < " + pathAudio
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
                print("-----------\r\n")

            elif METODO == 'BYE':

                Message = "SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(bytes(Message, 'utf-8') + b'\r\n')

                print("Enviando:\r\n" + Message)
                print("-----------\r\n")

            elif METODO not in METHOD_CLASS:

                Message = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
                self.wfile.write(bytes(Message, 'utf-8') + b'\r\n')

                print("Enviando:\r\n" + Message)
                print("-----------\r\n")

            else:
                Message = "SIP/2.0 400 Bad Request\r\n\r\n"
                self.wfile.write(bytes(Message, 'utf-8') + b'\r\n')
                print("Enviando:\r\n" + Message)
                print("-----------\r\n")


if __name__ == "__main__":

    # Creamos un servidor y escuchamos
    print("Listening...")

    serv = socketserver.UDPServer((ipServer, int(portServer)), EchoHandler)

    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")
