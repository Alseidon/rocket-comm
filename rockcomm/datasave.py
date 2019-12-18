#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getcwd

class Data():
    def __init__(self, dtype, dvalue, timeofsave):
        self.dtype = dtype
        self.dvalue = dvalue
        self.timeofsave = timeofsave
    
    def save(self, datasaver):
        datasaver.save(self)
        return

class DataSaver():
    def __init__(self, datatypes=[], maindir=getcwd()+'/data'):
        self.maindir = maindir
        self.paths = [[maindir+'/{}.txt'.format(dtype), dtype] for dtype in datatypes]
        self.writers = {path[1] : open(path[0], 'w+') for path in self.paths}
    def addDtype(self, dtype):
        newpath = [self.maindir+'/{}.txt'.format(dtype), dtype]
        if newpath not in self.paths:
            self.paths.append(newpath)
            self.writers[dtype] = open(newpath[0], 'w+')
        return
    def save(self, dataObj):
        while True:
            try:
                with self.writers[dataObj.dtype] as fichier:
                    fichier.write('{}   {}\n'.format(dataObj.timeofsave, dataObj.dvalue))
            except KeyError:
                self.addDtype(dataObj.dtype)
            else:
                break
        return