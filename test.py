# -*- coding: utf-8 -*-
# version of : 25/12/2019
# import socket
#

import rockcomm

host = ''
portD = 1111
portC = 1112
portU = 2111
portI = 2112
Serv = rockcomm.MainServer(host, portC, portD, portU, portI)
Serv.start()

Serv.IManager.add_periodic_info(b'still running', 2)

# Serv.CThread.stopconnexion()
# Serv.DThread.stopconnexion()
# Serv.UThread.stopconnexion()
# Serv.IThread.stopconnexion()
# Serv.CThread.join()
# Serv.CThread.join()
# Serv.UThread.join()
# Serv.IThread.join()

# Serv.stop()
    


# class CMSCK():
#     def __init__(self, sck):
#         self.sck = sck
    
#     def close(self):
#         self.sck += 2

# class Thr():
#     def __init__(self, sck):
#         self.cmmsck = CMSCK(sck)
    
#     def close(self):
#         self.cmmsck.close()
#         return