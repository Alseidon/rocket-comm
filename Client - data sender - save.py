#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 19:52:24 2019

@author: alseidon
"""

### PROTOTYPE DE TRAVAIL

import socket

class ConnexionSocket(socket.socket):
    def __init__(self):
        pass
    
    def sendChecked(self, msg, maxtrys=10): #msg mustn't be encoded ! #TEMP until creation of motherclass
        checkBytes, attempts = 0, 0
        L = len(msg)
        while checkBytes != L:
            checkBytes = self.send(msg.encode())
            attempts += 1
            if attempts > maxtrys:
                raise RuntimeError('{} couldn\'t be sent in {} attempts'.format(msg, attempts))
        return attempts
    
    def shutdown_server
    

class DataSendSocket(socket.socket):
    def __init__(self, host="", port=1111):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    
    def sendChecked(self, msg, maxtrys=10): #msg mustn't be encoded ! #TEMP until creation of motherclass
        checkBytes, attempts = 0, 0
        L = len(msg)
        while checkBytes != L:
            checkBytes = self.send(msg.encode())
            attempts += 1
            if attempts > maxtrys:
                raise RuntimeError('{} couldn\'t be sent in {} attempts'.format(msg, attempts))
        return attempts
    
    def sendData(self):
        
        print("Data type to send (acceleration, ...):")
        data_type = input(">> ")
        self.send(data_type.encode())
        check = self.recv(2048)
        if check != 'DTYPE RCVED':
            raise RunTimeError('Problem with dtype sending : {}'.format(check))
        print('Data  sent')

        print("Enter data value")
        data_value = input(">> ")
        self.send(str(data_value).encode())
        check = self.recv(2048)
        if check != 'DVALUE RCVED':
            raise RunTimeError('Problem with dtype sending : {}'.format(check))
        print('Data value sent')

        print("Sending end message")
        endmsg = 'DEND'
        self.send(data_value.encode())
        check = self.recv(2048)
        if check != 'DEND RCVED':
            raise RunTimeError('Problem with endmsg sending : {}'.format(check))
        print('End message sent')
        
    def autoSendData(self, data):
        self.sendChecked(data.type)
        check = self.rcv(2048)
        if check != 'DTYPE RCVED':
            raise RunTimeError('Problem with dtype sending : {}'.format(check))
        
        self.sendChecked(str(data.value))
        check = self.rcv(2048)
        if check != 'DVALUE RCVED':
            raise RunTimeError('Problem with dtype sending : {}'.format(check))
        
        self.sendChecked('EOD')
        check = self.rcv(2048)
        if check != 'EOD RCVED':
            raise RunTimeError('Problem with EOD sending : {}'.format(check))