#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .datasave import DataSaver
from .connexionthread import DatarcvThread


class MainServer(): #MUST GET DATA SAVING IN THIS
    """
    Main server class - can handle communication with machine, user and data saving.
    """
    def __init__(self, host, commandPort, dataPort, userPort, infoPort):
        """


        Parameters
        ----------
        host : str
            host of the server
        commandPort : int
            port sending commands to the machine.
        dataPort : int
            port receiving data from the machine.
        userPort : int
            port listening to the user.
        infoPort : int
            port sending automatic informations to user.

        Returns
        -------
        None.

        """
        self.host = host
        self.portC = commandPort
        self.portD = dataPort
        self.portU = userPort
        self.portI = infoPort
    
    def start(self):
        """
        Starts the server.

        Returns
        -------
        None.

        """
        self.dsave = DataSaver() #MUST BE CREATED CORRECTLY
        DThread = DatarcvThread((self.host, self.portD), self.DSaver, continuous=True, listenMax=1)
        DThread.start()