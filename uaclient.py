#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import xml.etree.ElementTree as ET


try:
    CONFIG = str(sys.argv[1])
    METODO = sys.argv[2]
    OPCION = sys.argv[3]
except:
    sys.exit("Usage: python uaclient.py config metodo opcion")


print(CONFIG)


# Comprobamos que es un fichero .xml
xml_comp = CONFIG.split('.')
try:
    if xml_comp[1] == 'xml':
        tree = ET.parse(CONFIG)
        root = tree.getroot()

        for child in root:
            print(child.tag, child.attrib)
except:
    sys.exit("Usage: The file is not a .xml or does not exist")





# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
#my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#my_socket.connect((IP, PORT))
