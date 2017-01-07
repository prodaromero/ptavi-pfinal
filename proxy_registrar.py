#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import os
from lxml import etree
import random

try:
    CONFIG = sys.argv[1]
    open(CONFIG)
except:
    sys.exit("Usage: python proxy_registrar.py config")


#Creamos nuestra estructura de datos ElementTree
doc = etree.parse(CONFIG)

#Obtenemos nuestros elementos que forman ElementTree
elementos = doc.getroot()

#Obtenemos nuestras variables
name = elementos[0].attrib["name"]
print(name)
ipProxy = elementos[0].attrib["ip"]
print(ipProxy)
portProxy = elementos[0].attrib["puerto"]
print(portProxy)

databasePath = elementos[1].attrib["path"]
print(databasePath)
passwdpath = elementos[1].attrib["passwdpath"]
print(passwdpath)

log = elementos[2].attrib["path"]
print(log)

print("---------------------------")


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:

            line = self.rfile.read()
            if not line:
                break
            Package = line.decode('utf-8')
            print("El cliente nos manda:\r\n" + Package)

            #Obtenemos variables del mensaje recibido
            Package = Package.split(' ')
            METHOD = Package[0]
            Direction = Package[1].split(':')[1]
            #Generamos el numero de Autenticación aleatoriamente en un intervalo
            nonce = random.randint(0,999999999999999999999)
            if METHOD == 'REGISTER':
                if 'Authenticate:' not in Package:
                    Message = ("SIP/2.0 401 Unanthorized\r\n"
                               + "WWW Authenticate: nonce=" + str(nonce))
                    print("Enviando: " + Message + "\r\n")
                    self.wfile.write(bytes(Message, 'utf-8'))
                    
if __name__ == "__main__":

    print('Listening...')

    serv = socketserver.UDPServer((ipProxy, int(portProxy)), EchoHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")


