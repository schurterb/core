# -*- coding: utf-8 -*-
"""
Created on Thu May 25 22:02:41 2017

@author: user

Base socket for all Observer-pattern platform sockets
This class only requires three private methods to be implemented
  doWriteToSocket( byte[] data ) : void
  doReadFromSocket() : void
  initSocket() : void
"""

from foundation.core.log import Logger
from foundation.core.pattern import Observer, Observable

import abc
import socket
import queue
import threading
from time import sleep

class BaseSocket(Observer, Observable, metaclass=abc.ABCMeta):
    
    def __init__(self, **kwargs):
        Observable.__init__(self)
        self.log = Logger("network", "BaseSocket", "DEBUG")
        self.writeLock = threading.Lock()
        self.readLock = threading.Lock()
        self.updateLock = threading.Lock()
        self.running = False
        self.threads = []
        self.maxQueueSize = kwargs.get('queueSize', 256)
        self.readQueue = queue.Queue(self.maxQueueSize)
        self.writeQueue = queue.Queue(self.maxQueueSize)
        self.updateQueue = queue.Queue(self.maxQueueSize)
        
    def start(self):
        try:
            self._initSocket()
            self.running = True
            self.log.info("Starting Read Thread")
            rt = threading.Thread(target=self.__readThread)
            self.threads.append(rt)
            rt.start()
            self.log.info("Starting Write Thread")
            wt = threading.Thread(target=self.__writeThread)
            self.threads.append(wt)
            wt.start()
            self.log.info("Starting Update Thread")
            ut = threading.Thread(target=self.__updateThread)
            self.threads.append(ut)
            ut.start()
            return True
        except Exception as e:
            self.log.critical("Failed to start MulticastSocket: "+str(e))
            return False
        
    def stop(self):
        try:
            self.log.info("Stopping threads")
            self.running = False            
            self.log.info("Closing socket(s)")
            for var in self.__dict__:
                if type(var) is socket.socket:
                    var.close()
            self.writeQueue.queue.clear()
            self.readQueue.queue.clear()
            self.updateQueue.queue.clear()            
            for thread in self.threads:
                thread.join(1)
            self.threads.clear()
            return True
        except Exception as e:
            self.log.critical("Failed to stop MulticastSocket: "+str(e))
            return False                       
    
    def read(self):
        if not self.readQueue.empty():
            self.log.debug("Reading data from read queue")
            return self.readQueue.get(False)
        else:
            return b''
        
    def write(self, data):
        if type(data) is str:
            self.log.debug("Adding data to write queue")
            self.writeQueue.put(bytes(data.encode("utf-8").strip()))
        elif type(data) is bytes:
            self.log.debug("Adding data to write queue")
            self.writeQueue.put(data)
        else:
            self.log.warn("Invalid datatype to write to socket:",type(data))
    
    def __readThread(self, bufferSize=1024):
        while(self.running):
            try:
                with self.readLock:
                    self.log.debug("Read thread receiving data")
                    self._doReadFromSocket()
            except Exception as e:
                self.log.error("Exception while reading socket: "+str(e))
            try:
                sleep(0.000001)
            except:
                self.log.warn("Inter-read sleep interrupted in read thread.")
            
    def __writeThread(self):
        while(self.running):
            if not self.writeQueue.empty():
                try:
                    with self.writeLock:
                        data = self.writeQueue.get(False)
                        self.log.debug("Write thread sending "+str(len(data))+" bytes of data")
                        self._doWriteToSocket(data)
                except Exception as e:
                    self.log.error("Exception while writing to socket: "+str(e))
            else:
                try:
                    sleep(0.00001)
                except:
                    self.log.warn("Inter-write sleep interrupted in write thread.")
    
    def __updateThread(self):
        while(self.running):
            if not self.updateQueue.empty():
                with self.updateLock:
                    self.log.debug("Update thread pushing data")
                    self.PushUpdate(self.updateQueue.get(False))
            else:
                try:
                    sleep(0.00001)
                except:
                    self.log.warn("Inter-update sleep interrupted in update thread.")
                    
    def Update(self, data):
        self.write(data)
        
    @abc.abstractmethod
    def _doWriteToSocket(self, data):
        pass
    
    @abc.abstractmethod
    def _doReadFromSocket(self):
        pass
        
    @abc.abstractmethod    
    def _initSocket(self):
        pass
        
