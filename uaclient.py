#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
from lxml import etree
import time
import os


try:
    CONFIG = str(sys.argv[1])
    METODO = sys.argv[2]
    OPCION = sys.argv[3]
except:
    sys.exit("Usage: python uaclient.py config metodo opcion")

try:
    open(CONFIG)
except:
    sys.exit("Usage: The file is not a .xml or does not exist")


def CreateLog(Log, Time, Message):

    """
    CREAMOS ARCHIVO LOG
    """

    FichLog = open(Log, 'a')
    FichLog.write(Time)
    FichLog.write(Message)
    FichLog.close

# Creamos nuestra estructura de datos ElementTree
doc = etree.parse(CONFIG)

# Obtenemos nuestros elementos que forman ElementTree
elementos = doc.getroot()

# Obtenemos nuestras variables
account = elementos[0].attrib
username = account.get("username")
print(username)
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


print("Starting...\r\n")
print("-----------\r\n")
hora = time.time()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((ipProxy, int(portProxy)))


try:
    Metodos = ['REGISTER', 'INVITE', 'BYE']

    Cabecera = METODO + " sip:"
    if METODO == "REGISTER":

        open(pathLog, 'w')
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        Message = " Starting..."
        CreateLog(pathLog, Time, Message + "\r\n")
        Message = (Cabecera + username + ":" + str(portServer) +
                   " SIP/2.0\r\n" + "Expires: " + str(OPCION) + "\r\n")

        print("Enviando: " + Message)
        print("-----------\r\n")
        # Enviamos el mensaje Register
        my_socket.send(bytes(Message, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Sent to " + ipProxy + ":" + portProxy + ": " +
                      Cabecera + username + " [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        # Esperamos a recibir la Autorizacion
        M_Recieve = data.decode('utf-8')
        print("Recibido -- " + M_Recieve + "\r\n")
        print("-----------\r\n")
        Autorizacion = M_Recieve.split("\r\n")[1]
        nonce = Autorizacion.split('=')[1]

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Recieved from: " + ipProxy + ":" + portProxy + ": " +
                      Autorizacion + " [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        Message = Message + Autorizacion

        # Enviamos el nuevo mensaje
        my_socket.send(bytes(Message, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print("Enviando:\r\n" + Message + "\r\n")
        print("-----------\r\n")

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Sent to " + ipProxy + ":" + portProxy + ": " +
                      Autorizacion + " [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        M_Recieve = data.decode('utf-8')
        print("Recibido -- " + M_Recieve + "\r\n")
        print("-----------\r\n")

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Recieved from: " + ipProxy + ":" + portProxy + ": " +
                      M_Recieve)
        CreateLog(pathLog, Time, MessageLog + "\r\n")

    elif METODO == "INVITE":

        open(pathLog, 'a')

        Message = (Cabecera + OPCION + " SIP/2.0\r\n" +
                   "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" +
                   "o=" + username + " " + ipServer + "\r\n" +
                   "s=misesion\r\n" + "t=0\r\n" + "m=" +
                   str(elementos[5].tag) +
                   " " + portRtp + " RTP")
        print("Enviando:\r\n" + Message + "\r\n")
        print("-----------\r\n")
        my_socket.send(bytes(Message, 'utf-8') + b'\r\n')

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Sent to " + ipProxy + ":" + portProxy + ": " + METODO +
                      " " + OPCION + " [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        # Datos recividos del Servidor
        data = my_socket.recv(1024)
        respuesta = data.decode('utf-8')
        print("Recibiendo del Servidor:\r\n" + respuesta)
        print("-----------\r\n")
        Lines = respuesta.split('\r\n')
        Trying = Lines[0].split(' ')[1]
        Rining = Lines[1].split(' ')[1]
        OK = Lines[2].split(' ')[1]
        Client = Lines[6].split(' ')[0]
        UserClient = Client.split('=')[1]

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Recieved from: " + ipProxy + ":" + portProxy + ": " +
                      Lines[0] + " [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        if Trying == '100' and Rining == '180' and OK == '200':
            Message = ('ACK sip:' + UserClient + " SIP/2.0")
            my_socket.send(bytes(Message, 'utf-8') + b'\r\n')
            print("Enviando:\r\n" + Message + "\r\n")
            print("-----------\r\n")

            # LOG
            Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
            MessageLog = (" Sent to: " + ipProxy + ":" + portProxy +
                          ": ACK [...]")
            CreateLog(pathLog, Time, MessageLog + "\r\n")
        else:
            # LOG
            Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
            MessageLog = (" Recieve from: " + ipProxy + ":" + portProxy +
                          ": 404 User Not Foun")
            CreateLog(pathLog, Time, MessageLog + "\r\n")

    elif METODO == "BYE":
        Message = (Cabecera + OPCION + " SIP/2.0")
        print("Enviando:\r\n" + Message + "\r\n")
        print("-----------\r\n")
        my_socket.send(bytes(Message, 'utf-8') + b'\r\n')

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Sent to: " + ipProxy + ":" + portProxy + ": BYE [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        data = my_socket.recv(1024)
        respuesta = data.decode('utf-8')

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Recieve from: " + ipProxy + ":" + portProxy +
                      ": BYE [...]")
        CreateLog(pathLog, Time, MessageLog + "\r\n")

        print("Recibiendo del Servidor:\r\n" + respuesta)
        print("-----------\r\n")

        # LOG
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        MessageLog = (" Finishing.")
        CreateLog(pathLog, Time, MessageLog + "\r\n")


except:
        sys.exit("Error: No server listening")
