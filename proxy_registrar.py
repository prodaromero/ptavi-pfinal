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

#Obtenemos nuestras variables del xml
name = elementos[0].attrib["name"]
IP = elementos[0].attrib["ip"]
portProxy = elementos[0].attrib["puerto"]
databasePath = elementos[1].attrib["path"]
passwdpath = elementos[1].attrib["passwdpath"]
log = elementos[2].attrib["path"]


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
            MethodServer = ['INVITE', 'ACK', 'BYE']
            #Obtenemos variables del mensaje recibido
            Line = M_Recieve.split('\r\n')
            Package = Line[0].split(' ')
            METHOD = Package[0]
            User = Package[1].split(':')[1]
            #Generamos el numero de Autenticación aleatoriamente en un intervalo
            nonce = random.randint(0,999999999999999999999)
            if METHOD == 'REGISTER':

                Autorizacion = Line[2]
                ServerPort = Package[1].split(':')[2]
                Expires = Line[1].split(' ')[1]
                self.Client_Register[User] = ServerPort

                if 'Authenticate:' not in Autorizacion:
                    Message = ("SIP/2.0 401 Unanthorized\r\n"
                               + "WWW Authenticate: nonce=" + str(nonce))
                    print("-----------\r\n")
                    print("Enviando:\r\n" + Message + "\r\n")
                    print("-----------\r\n")
                    self.wfile.write(bytes(Message, 'utf-8'))

                else:
                    Message = "SIP/2.0 200 OK\r\n"
                    print("-----------\r\n")
                    print("Enviando:\r\n" + Message + "\r\n")
                    self.wfile.write(bytes(Message, 'utf-8'))
                    print("-----------\r\n")

            elif METHOD in MethodServer:
                for user in self.Client_Register:
                    if User == user:
                        self.ServerPort = self.Client_Register[user]

                #Recivimos el mensaje y lo reenviamos al Servidor
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.connect((IP, int(self.ServerPort)))

                if METHOD == 'INVITE':
                    
                    my_socket.send(bytes(M_Recieve, 'utf-8'))
                    print("-----------\r\n")
                    print("Reenviando:\r\n" + M_Recieve)
                    #Recivimos la confirmacion del INVITE y la reenviamos 
                    print("-----------\r\n")
                    data = my_socket.recv(1024)
                    respuesta = data.decode('utf-8')
                    print("Recibiendo del Servidor y reenviando al cliente:\r\n"
                          + respuesta)
                    print("-----------\r\n")
                    self.wfile.write(bytes(respuesta, 'utf-8') + b'\r\n')

                elif METHOD == 'ACK':

                    my_socket.send(bytes(M_Recieve, 'utf-8'))
                    print("-----------\r\n")
                    print("Reenviando:\r\n" + M_Recieve)
                elif METHOD == 'BYE':

                    my_socket.send(bytes(M_Recieve, 'utf-8'))
                    print("-----------\r\n")
                    print("Reenviando:\r\n" + M_Recieve)

                    data = my_socket.recv(1024)
                    respuesta = data.decode('utf-8')
                    print("-----------\r\n")
                    print("Recibindo del Servidor y reenviando al cliente:\r\n" +
                          respuesta)
                    self.wfile.write(bytes(respuesta, 'utf-8') + b'\r\n')
                    print("-----------\r\n")


if __name__ == "__main__":

    print('Listens = socket.socket(socket.AF_INET, socket.SOCK_STREAM)ing...')

    serv = socketserver.UDPServer((IP, int(portProxy)), EchoHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")


