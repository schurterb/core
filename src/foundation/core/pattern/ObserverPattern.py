# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:33:48 2017

@author: user

Observer and Observable base class definitions
"""

from foundation.core.log import Logger
import abc

class Observer(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def Update(self, data):
        pass
    
    
class Observable():

    isObservable = False
    
    def __init__(self):
        self.log = Logger("network", "MulticastSocket", "ERROR")
        self.observers = []
        self.isObservable = True
    
    def addObserver(self, observer):
        if not hasattr(observer, 'Update'):
            self.log.warn(str(type(observer))+" is not an observer")
            return
        if observer not in self.observers:
            self.observers.append(observer)
    
    def removeObserver(self, observer):
        if not hasattr(observer, 'Update'):
            self.log.warn(str(type(observer))+" is not an observer")
            return
        if observer in self.observers:
            self.observers.remove(observer)
            
    def PushUpdate(self, data):
        if data is not None:
            for observer in self.observers:
                try:
                    observer.Update(data)
                except Exception as e:
                    print("Failed to update an observer. Reason: "+str(e))
        else:
            print("Update is Nonetype")