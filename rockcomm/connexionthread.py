#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading

from .commsocket import DatarcvSocket, bindsocket

class ConnexionThread(threading.Thread):
    """
    General class for threads used to send or receive instances.
    """
    def __init__(self, adress, listenMax=10):
        """
        

        Parameters
        ----------
        adress : (str, int)
            IP adress (host, port) assigned to the connexion.
        listenMax : int, optional
            Parameter passed to socket.listen . The default is 10.

        Returns
        -------
        None.

        """
        
        self.adress = adress
        self.listenMax = listenMax
        self.continuous = True
    
    def run(self):
        """
        Method required by motherclass threading.Thread .

        Returns
        -------
        None
        
        """
        while(self.continuous):
            sock = bindsocket(self.adress[1], self.adress[0])
            sock.listen(self.listenMax)
            (clientsock, IPadress) = sock.accept()
            self.commsock = self.createCommSock(clientsock, IPadress)
            self.comm()
        return
    
    def createCommSock(self, sock, adress):
        """
        Method defined for each daughter class. Creates a CommSock according to the ConnexionThread used

        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        adress : (str, int)
            IP adress (host, port) assigned to the socket.

        Returns
        -------
        None.

        """
        pass
    
    def comm(self):
        """
        Method defined for each daughter class. Communicates to send or receive the instance.

        Returns
        -------
        None.

        """
        pass


class DatarcvThread(ConnexionThread):
    """
    Thread to receive data.
    """
    
    def __init__(self, sock, DSaver, listenMax=1):
        """
        

        Parameters
        ----------
        sock :  CommSocket
            Socket listening for data.
        DSaver :  Datasaver
            Data saving instance.
        listenMax : int, optional
            Parameter passed to socket.listen . The default is 1.

        Returns
        -------
        None.

        """
        self.__init__(sock, listenMax)
        self.DSaver = DSaver
    
    def createCommSock(self, sock, adress):
        return DatarcvSocket(sock, adress)
    
    def comm(self):
        """
        Starts reception and save of one data.

        Returns
        -------
        None.

        """
        while(self.continuous):
            data = self.commsock.comm()
            self.DSaver.save(data)