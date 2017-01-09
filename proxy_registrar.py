#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import socket
import sys
import os
from lxml import etree
import random
import json

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
IP = elementos[0].attrib["ip"]
print(IP)
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
    Client_Register = {}
    attr = {}

    def json2registered(self):
        """
        COMPROBAMIS SI HAY FICHERO JSON
        """
        try:
            File = open(databasePath, 'r')
            self.Cilent_Register = File.load(File)
        except:
            self.Client_Register = {}
    def register2json(self):

        """
        CREAMOS ARCHIVO JSON
        """
        file = open('registered.json', 'w')
        json.dump(self.Client_Register, file, sort_keys=True,
                  indent=4, separators=(',', ':'))
        file.close()

    def handle(self):
        while 1:

            self.register2json()

            line = self.rfile.read()
            if not line:
                break
            M_Recieve = line.decode('utf-8')
            print("El cliente nos manda:\r\n" + M_Recieve)
            ServerPort = []
            #Obtenemos variables del mensaje recibido
            Line = M_Recieve.split('\r\n')
            Package = Line[0].split(' ')
            METHOD = Package[0]
            User = Package[1].split(':')[1]
            #Generamos el numero de Autenticación aleatoriamente en un intervalo
            nonce = random.randint(0,999999999999999999999)
            Autorizacion = Line[2]
            if METHOD == 'REGISTER':

                print(User)
                ServerPort = Package[1].split(':')[2]
                print(ServerPort)
                Expires = Line[1].split(' ')[1]
                print(Expires)
                self.attr['PuertoServidor'] = ServerPort
                self.Client_Register[User].append(Serverport)

                if 'Authenticate:' not in Autorizacion:
                    Message = ("SIP/2.0 401 Unanthorized\r\n"
                               + "WWW Authenticate: nonce=" + str(nonce))
                    print("Enviando:\r\n" + Message + "\r\n")
                    self.wfile.write(bytes(Message, 'utf-8'))

                else:
                    Message = "SIP/2.0 200 OK\r\n"
                    print("Enviando:\r\n" + Message + "\r\n")
                    self.wfile.write(bytes(Message, 'utf-8'))

            elif METHOD == 'INVITE':
                print(User)
                for user in self.Client_Register:
                    print(User)
                    print("%%%%%%%%%%%%%%%")
                    print(user)
                    if User == user:
                        self.ServerPort = self.Client_Register[user]
                        print(self.ServerPort)
                        self.ServerPort = self.ServerPort["PuertoServidor"]
                        print(self.ServerPort)
                        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print(self.ServerPort)
                #Recivimos el mensaje y lo reenviamos al Servidor
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.connect((IP, int(self.ServerPort)))
                my_socket.send(bytes(M_Recieve, 'utf-8'))
                print("-----------")
                print("Reenviando:\r\n" + M_Recieve)
                #Recivimos la confirmacion del INVITE y la reenviamos al cliente
                data = my_socket.recv(1024)
                respuesta = data.decode('utf-8')
                print("Reciviendo del Servidor y reenviando al cliente:\r\n" +
                      respuesta)
                self.wfile.write(bytes(respuesta, 'utf-8') + b'\r\n')

            print(self.Client_Register)
     

if __name__ == "__main__":

    print('Listens = socket.socket(socket.AF_INET, socket.SOCK_STREAM)ing...')

    serv = socketserver.UDPServer((IP, int(portProxy)), EchoHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")


