# -*- coding: utf-8 -*-
"""
Created on Thu May 25 21:59:08 2017

@author: user

Multicast channel for sending and receiving serialized objects.
"""

from core.log import Logger
from core.pattern import Observer, Observable
from core.serialization import PickleSerializer
from core.sockets import MulticastSocket

import threading

class MulticastChannel(Observer, Observable):
    
    def __init__(self, group, port=3528, **kwargs):
        Observable.__init__(self)
        self.log = Logger("network", "MulticastChannel", "DEBUG")
        self.serializeLock = threading.Lock()
        self.serializer = PickleSerializer()
        self.group = group
        bindPort = kwargs.get('bindPort', 17640)
        if bindPort == port:
            bindPort += 1
        try:
            self.channelSocket = MulticastSocket(group, port, bindPort)
            self.channelSocket.addObserver(self)
            self.channelSocket.start()
            self.is_open = True
        except Exception as e:
            self.log.critical("Failed to open channel on "+group+".  Reason: "+str(e))
            self.is_open = False    
           
    def __del__(self):
        if type(self.channelSocket) is not None:
            self.close()

    def close(self):
        try:
            self.channelSocket.stop()
            self.channelSocket.removeObserver(self)
            self.channelSocket = None
            self.is_open = False
            return True
        except Exception as e:
            self.log.critical("Failed to close channel on "+self.group+".  Reason: "+str(e))
            return False

    def send(self, obj):
        if type(obj) is not None:
            try:
                with self.serializeLock:
                    data = self.serializer.serialize(obj)
                    self.channelSocket.write(data)
            except Exception as e:
                self.log.error("Failed to serialize object of type "+str(type(obj))+". Reason: "+str(e))                
        else:
            self.log.debug("Unable to serialize Nonetype object.")
    
    def Update(self, data):
        if type(data) is bytes:
            try:
                with self.serializeLock:
                    obj = self.serializer.deserialize(data)
                    self.PushUpdate(obj)
            except Exception as e:
                self.log.error("Failed to deserialize data. Reason: "+str(e))
        else:
            self.log.debug("Unable to deserialize "+str(type(data))+" object.")