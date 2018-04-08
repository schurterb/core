# -*- coding: utf-8 -*-
"""
Created on Thu May  4 23:19:07 2017

@author: user

basic multicast socket
"""

from foundation.core.log import Logger
from .BaseSocket import BaseSocket

import socket
import struct

class MulticastSocket(BaseSocket):
    
    def __init__(self, group, port, bindPort):
        BaseSocket.__init__(self)
        self.log = Logger("network", "MulticastSocket", "DEBUG")
        self.multicast_addr = group
        self.multicast_dst_port = port
        self.multicast_src_port = bindPort
        
    def _doWriteToSocket(self, data):
        self.insock.sendto(data, (self.multicast_addr, self.multicast_dst_port))
    
    def _doReadFromSocket(self):
        data = self.insock.recv(10240)
        if self.readQueue.qsize() == self.maxQueueSize:
            self.readQueue.get(False)
        self.readQueue.put(data)
        with self.updateLock:
            if self.updateQueue.qsize() == self.maxQueueSize:
                self.updateQueue.get(False)
            self.updateQueue.put(data)
        
    def _initSocket(self):
        #Initialize input socket
        self.insock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.insock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.insock.bind(('', self.multicast_dst_port))
        mreq = struct.pack("4sl", socket.inet_aton(self.multicast_addr), socket.INADDR_ANY)
        self.insock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.insock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        #Initialize output socket
        #self.outsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #self.outsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.outsock.bind(('', self.multicast_src_port))
        #self.outsock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)