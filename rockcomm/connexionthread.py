#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
from time import sleep

from .commsocket import DatarcvSocket, CommandSocket, UserSocket, InfoSocket, bindsocket
# from .manager import CommandManager

class ConnexionThread(threading.Thread):
    """
    General class for threads used to send or receive instances.
    """
    def __init__(self, address, listenMax=10, continuous=True):
        """
        

        Parameters
        ----------
        address : (str, int)
            IP address (host, port) assigned to the connexion.
        listenMax : int, optional
            Parameter passed to socket.listen . The default is 10.
        continuous: bool, optional
            Whether to continue the loop of the thread. The default is True.

        Returns
        -------
        None.

        """
        threading.Thread.__init__(self)
        self.address = address
        self.listenMax = listenMax
        self.continuous = continuous
    
    def run(self):
        """
        Method required by motherclass threading.Thread .

        Returns
        -------
        None
        
        """        
        while(self.continuous):
            try:
                print('{} - running new loop'.format(self.address))
                sock = bindsocket(self.address[1], self.address[0])
                sock.listen(self.listenMax)
                (clientsock, IPaddress) = sock.accept()
                self.commsock = self.createCommSock(clientsock, IPaddress)
                self.comm()
                sock.close()
            except ConnectionResetError:
                print('Connexion reset at address {}- reloading the loop'.format(self.address))
        print('{} - shutting down'.format(self.address))
        return
    
    def stopconnexion(self):
        """
        Stops communication at the end of the following iteration

        Returns
        -------
        None.

        """
        self.continuous = False
        return
    
    # def forcestop(self):
    #     pass
    
    def createCommSock(self, sock, address):
        """
        Method defined for each daughter class. Creates a CommSock according to the ConnexionThread used

        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        address : (str, int)
            IP address (host, port) assigned to the socket.

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

    def __init__(self, address, DSaver, listenMax=1, continuous=True):
        """
        

        Parameters
        ----------
        address :  (str, int)
            ip address to receive the data to.
        DSaver :  Datasaver
            Data saving instance.
        listenMax : int, optional
            Parameter passed to socket.listen . The default is 1.

        Returns
        -------
        None.

        """
        ConnexionThread.__init__(self, address, listenMax, continuous)
        self.DSaver = DSaver

    def createCommSock(self, sock, address):
        """
        Creates a CommSock; here it is a DatarcvSocket.

        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        address : (str, int)
            IP address (host, port) assigned to the socket.
        
        Returns
        -------
        DatarcvSocket
            the created socket.

        """
        return DatarcvSocket(sock, address)
    
    def comm(self):
        """
        Starts reception and save of one data.

        Returns
        -------
        None.

        """
        data = self.commsock.comm(sendChecked=True)
        self.DSaver.save(data)



class CommandThread(ConnexionThread):
    """
    Threads sending commands to the machine and getting the answers.
    """
    def __init__(self, address, CManager, listenMax=10, continuous=True):
        """
        

        Parameters
        ----------
        address : (str, int)
            ip address assigned to the command sending.
        CManager : CommandManager
            Source of the commands to send.
        listenMax : int, optional
            parameter passed to socket.listen . The default is 10.
        continuous : bool, optional
            whether to continuously run the thread. The default is True.

        Returns
        -------
        None.

        """
        ConnexionThread.__init__(self, address, listenMax, continuous)
        self.CManager = CManager
        return
    
    def createCommSock(self, sock, address, msg=''):
        """
        Creates a CommSock; here it is a CommandSocket.

        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        address : (str, int)
            IP address (host, port) assigned to the socket.
        msg: str, optional
            command to send to the machine. The default is ''.
        Returns
        -------
        CommandSocket
            the created socket.

        """
        return CommandSocket(sock, address, msg)
    
    def comm(self):
        """
        Starts sending of one command. If no command is up for processing, sends 0.

        Returns
        -------
        None.

        """
        key, self.commsock.msg = self.CManager.get_command('MACH')
        print(key)
        if key == None:
            self.commsock.msg = b'0'
            self.commsock.comm(sendChecked=True)
            return
        answer = self.commsock.comm(sendChecked=True)
        self.CManager.add_answer(key, answer)
        return
    
    def stopconnexion(self):
        """
        Sends information that server is shutting down.

        Returns
        -------
        None.

        """
        self.CManager.add_command(b'SERV SHUTOWN MACH')



class UserThread(ConnexionThread):
    """
    Thread processing the user's commands.
    """
    def __init__(self, address, CManager, listenMax=10, continuous=True):
        ConnexionThread.__init__(self, address, listenMax, continuous)
        self.CManager = CManager
        return
    
    def createCommSock(self, sock, address):
        """
        Creates a CommSock; here it is a UserSocket.

        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        address : (str, int)
            IP address (host, port) assigned to the socket.
        
        Returns
        -------
        UserSocket
            the created socket.

        """
        return UserSocket(sock, address)
    
    def comm(self):
        """
        Starts receiving and answering one command. If no answer is achieved in 10 seconds, sends back this information.

        Returns
        -------
        None.

        """
        command = self.commsock.comm_command(sendChecked=True)
        key = self.CManager.add_command(command)
        answer = None
        time_passed = 0
        while answer == None:
            sleep(.1)
            time_passed += 1
            if time_passed >= 100:
                answer = 'No answer in {}s'.format(time_passed / 10).encode()
                break
            answer = self.CManager.answers[key]
        del(self.CManager.answers[key])
        self.commsock.comm_answer(answer, sendChecked=True)
        return



class InfoThread(ConnexionThread):
    """
    Thread sending automatic informations to the user.
    """
    def __init__(self, address, IManager, listenMax=10, continuous=True):
        ConnexionThread.__init__(self, address,listenMax, continuous)
        self.IManager = IManager
        return
    def createCommSock(self, sock, address):
        """
        Creates a CommSock; here it is a InfoSocket.
        Parameters
        ----------
        sock : socket.socket
            connexion socket to be upgraded.
        address : (str, int)
            IP address (host, port) assigned to the socket.
        
        Returns
        -------
        InfoSocket
            the created socket.
        """
        return InfoSocket(sock, address,'')
    
    def comm(self):
        """
        sends an information to the user. If there is nothing to send, sends 0.

        Returns
        -------
        None.

        """
        self.commsock.info = self.IManager.get_info()
        if self.commsock.info == None:
            self.commsock.info = 0
        self.commsock.comm()
        return
    
    def stopconnexion(self): 
        """
        Sends information that server is shutting down and stops the thred.

        Returns
        -------
        None.

        """
        self.IManager.add_info(b'Server shutting down')
        while self.IManager != []:
            sleep(.5)
        ConnexionThread.stopconnexion(self)