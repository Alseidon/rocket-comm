#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:48:10 2019

@author: alseidon
"""

import socket
import time
from .datasave import Data

class CommSocket():
    """
    Motherclass of socket designed to send or receive one instance.
    """
    def __init__(self, sock, adress):
        """
        

        Parameters
        ----------
        sock : socket.socket
            socket to upgrade.
        adress : (host, port)
            IP adress (host, port)= assigned to the socket.

        Returns
        -------
        None.

        """
        self.sock = sock
        self.adress = adress

    
    def sendChecked(self, msg, maxtrys=10): #MUST rethink rcv accordingly
        """
        Improved version of socket.send : verifies length of received message and tries again if needed.
        
        Parameters
        ----------
        msg : str
            message to send. WARNING mustn't be encoded.
        maxtrys : int, optional
            maximum send trys. The default is 10.
        
        Returns
        -------
        None.
        """
        checkBytes, attempts = 0, 0
        L = len(msg)
        while checkBytes != L:
            checkBytes = self.sock.send(msg.encode())
            attempts += 1
            if attempts > maxtrys:
                raise RuntimeError('{} couldn\'t be sent in {} attempts'.format(msg, attempts))
        return attempts
    
    def comm(self):
        """
        Method defined for each daughter class. Communicates to send or receive the instance.

        Returns
        -------
        None.

        """
        pass

class DatarcvSocket(CommSocket):
    """
    Socket to receive one data
    """
    def comm(self):
        """
        Recieves one data at (self.ip, self.port).
        Format : receives the data type, then data value, then sends EOD (end of data) ; then deconnects.

        Returns
        -------
        Data
            Instance of Data, with dtype, dvalue and time of reception.

        """
        
        print("Connexion de {}" % (self.adress))
        dtype = self.sock.recv(2048)
        self.sendChecked('DTYPE RCVED')
        dvalue = self.sock.rcv(2048)
        self.sendChecked('DVALUE RCVED')
        EndMsg = self.sock.rcv(2048)
        if EndMsg != 'EOD':
            self.sendChecked('Error: EOD not recieved')
        self.sock.close()
        print("Client déconnecté...")
        return Data(dtype, dvalue, time.time()) #at this point we consider time of measure and time of rcv are similar


class CommandSocket(CommSocket):
    """
    Socket to send one command to the machine.
    """
    def __init__(self, sock, adress, msg=''):
        """
        

        Parameters
        ----------
        sock : socket.socket
            socket to upgrade.
        adress : (host, port)
            IP adress (host, port)= assigned to the socket.
        msg : str, optional
            command to send. The default is ''.

        Returns
        -------
        None.

        """
        self.sock = sock
        self.adress = adress
        self.msg = msg

    def comm(self):
        """
        Sends the command.

        Raises
        ------
        NameError
            if the command is unknown.

        Returns
        -------
        None.

        """
        
        print("Connexion de %s %s" % (self.ip, self.port, ))
        self.sendChecked(self.msg)
        answer = self.listen(2048).decode()
        if answer == 'unknown command':
            raise NameError('Command not known by the machine.')
        return


class UserSocket(CommSocket):
    """
    Socket to receive commands from the user
    """
    def comm(self):
        pass



# def createCommSock(sockettype, ip, port, socktypelist=['command', 'datarcv', 'user']): # sockettype MUST BE in socktypelist
#     """
#     Creates a CommSocket according to the given name
    
#     Parameters
#     ----------
#     sockettype : str
#         type of socket.
#     ip : str
#         IP assigned to the socket.
#     port : int
#         port assigned to the socket.
#     socktypelist: list, optional
#         list of available CommSocket types.
    
#     Raises
#     ------
#     NameError
#         if the sockettype isn't in the list.
    
#     Returns
#     -------
#     The created CommSocket.
#     """
#     if sockettype not in socktypelist:
#         raise NameError('socket type doesn\'t exist - input error or type hasn\'t been listed yet')
#     elif sockettype == 'command':
#         return CommandSocket(ip, port)
#     elif sockettype == 'datarcv':
#         return DatarcvSocket(ip, port)
#     elif sockettype == 'user':
#         return UserSocket(ip, port)


def bindsocket(port, host=''):
    """
    Creates a socket assigned to the IP adress (host, port).

    Parameters
    ----------
    port : int
        port assigned to the socket.
    host : str, optional
        host assigned to the socket. The default is ''.

    Returns
    -------
    tcpsock : socket
        socket connected at (host, port).

    """
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((host, port))
    return tcpsock