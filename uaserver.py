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

#Creamos nuestra estructura de datos ElementTree
doc = etree.parse(CONFIG)

#Obtenemos nuestros elementos que forman ElementTree
elementos = doc.getroot()

print(len(elementos))
print(elementos[0].attrib)

#Obtenemos nuestras variables
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

print(username)
print(passwd)
print(ipServer)
print(portServer)
print(portRtp)
print(ipProxy)
print(portProxy)
print(pathLog)
print(pathAudio)
print("--------------------------------")


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:

            line = self.rfile.read()
            if not line:
                break
            Message = line.decode('utf-8')
            print("El cliente nos manda " + Message)
            METODO = Message.split(' ')[0]

            if METODO == 'INVITE':
                


if __name__ == "__main__":
    try:
        CONFIG = sys.argv[1]
        open(CONFIG)
    except:
        sys.exit("Usage: python uaserver.py config")

    #Creamos un servidor y escuchamos
    print("Listening...")
    
    serv = socketserver.UDPServer((ipProxy, int(portProxy)), EchoHandler)
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")
        
