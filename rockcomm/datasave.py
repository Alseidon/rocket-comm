#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getcwd

class Data():
    """
    Data object.
    """
    def __init__(self, dtype, dvalue, timeofsave=None):
        """
        

        Parameters
        ----------
        dtype : str
            type of the data.
        dvalue : any type
            value of the data - type depends on the dtype.
        timeofsave : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        self.dtype = dtype
        self.dvalue = dvalue
        self.timeofsave = timeofsave
    
    def save(self, datasaver):
        """
        Saves the data in the given datasaver.

        Parameters
        ----------
        datasaver : DataSaver
            the instance saving the data.

        Returns
        -------
        None.

        """
        datasaver.save(self)
        return
    
    def __repr__(self):
        return 'Data(dtype={}, dvalue={})'.format(self.dtype, self.dvalue)
    def __str__(self):
        return '{} : {}'.format(self.dtype, self.dvalue)



class DataSaver():
    """
    Object allowing to save every data.
    """
    def __init__(self, datatypes=[], maindir=getcwd()+'/data'):
        """
        

        Parameters
        ----------
        datatypes : list, optional
            List of currently received data types. The default is [].
        maindir : str, optional
            main directory where to save the data files. The default is getcwd()+'/data'.

        Returns
        -------
        None.

        """
        self.maindir = maindir
        self.paths = {dtype : maindir+'/{}.txt'.format(dtype) for dtype in datatypes}
        return
    
    def addDtype(self, dtype):
        """
        adds a new data type

        Parameters
        ----------
        dtype : str
            data type to add.

        Returns
        -------
        None.

        """
        if dtype not in self.paths:
            self.paths[dtype] = self.maindir+'/{}.txt'.format(dtype)
        return
    
    def save(self, dataObj):
        """
        saves a new data.

        Parameters
        ----------
        dataObj : Data
            data to save.

        Returns
        -------
        None.

        """
        if dataObj.dtype not in self.paths:
            self.addDtype(dataObj.dtype)
        with open(self.paths[dataObj.dtype], 'a') as file:
            file.write('{}   {}\n'.format(dataObj.timeofsave, dataObj.dvalue))
        return