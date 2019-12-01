#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 19:43:57 2019

@author: alseidon
"""

#PROTOTYPE DE TRAVAIL

import socket
import threading

class DataRcvThread(threading.Thread):

    def __init__(self, ip, port, sendersocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sendersocket = sendersocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def sendChecked(self, msg, maxtrys=10): #msg mustn't be encoded ! #TEMP until creation of motherclass #MUST rethink rcv accordingly
        checkBytes, attempts = 0, 0
        L = len(msg)
        while checkBytes != L:
            checkBytes = self.sendersocket.send(msg.encode())
            attempts += 1
            if attempts > maxtrys:
                raise RuntimeError('{} couldn\'t be sent in {} attempts'.format(msg, attempts))
        return attempts
    
    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        dtype = self.serversocket.recv(2048)
        self.sendChecked('DTYPE RCVED')
        dvalue = self.serversocket.rcv(2048)
        self.sendChecked('DVALUE RCVED')
        EndMsg = self.serversocket.rcv(2048)
        if EndMsg != 'EOD':
            self.sendChecked('Error: EOD not recieved')

        self.clientsocket.send(fp.read())

        print("Client déconnecté...")


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (GetDataSock, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, GetDataSock)
    newthread.start()