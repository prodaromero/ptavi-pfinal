#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
from lxml import etree
import time

try:
    CONFIG = str(sys.argv[1])
    METODO = sys.argv[2]
    OPCION = sys.argv[3]
except:
    sys.exit("Usage: python uaclient.py config metodo opcion")


print(CONFIG)

try:
    open(CONFIG)
except:
    sys.exit("Usage: The file is not a .xml or does not exist")

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

#Imprimimos 
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

print(" Starting...")
hora = time.time()


#Metodos
try:
    Message = METODO + " sip:"
    if METODO == "REGISTER":
        Message = (Message + username +  ":" + str(passwd)
                   + " SIP/2.0\r\n" + "Expires: " + str(OPCION))

    elif METODO == "INVITE":
        Message = (Message + OPCION + " SIP/2.0\r\n" 
                   + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n"
                   + username + " " + ipServer + "\r\n" + "s=misesion\r\n"
                   + "t=0\r\n" + "m=" + str(elementos[5].tag) +" "
                   + portRtp + " RTP")
    elif METODO == "BYE":
        Message = (Message + OPCION + " SIP/2.0")

    print("Enviando: " + Message)
except:
    sys.exit("Usage: Method must be REGISTER, INVITE or BYE")


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((ipProxy, int(portProxy)))

print("Enviando: " + Message)
my_socket.send(bytes(Message, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)












