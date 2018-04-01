# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 20:54:29 2016

@author: user

Singleton Class 
ensures there is only one of the said object
"""

from .singleton import Singleton
from core.data import MulticastChannel
from core.pattern import Observer

import threading
import time

#Distributed Singleton is a distributed object of which there 
# can only be one on each server and all act as one object


class distributedDataUpdate(type):
    
    def __init__(self, item, value):
        self.source = None
        self.destination = None
        self.timestamp = time.time()
        self.item = item
        self.value = value


class distributedData(Observer):
    
    channel = None
    data = {}
    
    def __init__(self, channel=None):
        if type(channel) is MulticastChannel:
            self.channel = channel
    
    def __setattr__(self, item, value):
        if type(item) is str:
            self.__dict__[item] = value
            if self.channel is not None and type(value) is not MulticastChannel:
                data = distributedDataUpdate(item, value)
                self.channel.send(data)
    
    def Update(self, data):
        if type(data) is distributedDataUpdate and type(data.item) is str:
            self.__dict__[data.item] = data.value

class DistributedSingleton(metaclass=Singleton):
    
    def __init__(self, **kwargs):
        self.shared = distributedData()
        self.group = None
        self.port = None
        self.bindPort = None
        self.channel = None
        
    def __del__(self):
        if self.channel is not None:
            self.channel.removeObserver(self.shared)
            self.channel.close()
            del self.channel
                
    def setGroup(self, group, **kwargs):
        if self.channel is not None:
            self.channel.removeObserver(self.shared)
            self.channel.close()
        self.group = group
        self.port = kwargs.get('port',self.port)
        self.bindPort = kwargs.get('bindPort',self.bindPort)
        self.channelLock = threading.Lock()
        if self.port is not None and self.bindPort is not None:
            self.channel = MulticastChannel(self.group, self.port, bindPort=self.bindPort)
        elif self.port is not None:
            self.channel = MulticastChannel(self.group, self.port)
        elif self.bindPort is not None:
            self.channel = MulticastChannel(self.group, bindPort=self.bindPort)
        else:
            self.channel = MulticastChannel(self.group)
        self.channel.addObserver(self.shared)
        self.shared.channel = self.channel
        