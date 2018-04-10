# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 12:46:27 2018

@author: user

A threadsafe version of the observerable pattern (locks on the observer list)
"""

from foundation.core.log import Logger
from threading import Lock

class ThreadsafeObservable():

    isObservable = False
    
    def __init__(self):
        self.log = Logger("system", "ThreadsafeObservable", "ERROR")
        self.observers = []
        self.isObservable = True
        self.observerLock = Lock()
    
    def addObserver(self, observer):
        if not hasattr(observer, 'Update'):
            self.log.warn(str(type(observer))+" is not an observer")
            return
        if observer not in self.observers:
            with self.observerLock:
                self.observers.append(observer)
    
    def removeObserver(self, observer):
        if not hasattr(observer, 'Update'):
            self.log.warn(str(type(observer))+" is not an observer")
            return
        if observer in self.observers:
            with self.observerLock:
                self.observers.remove(observer)
            
    def PushUpdate(self, data):
        if data is not None:
            with self.observerLock:
                for observer in self.observers:
                    try:
                        observer.Update(data)
                    except Exception as e:
                        print("Failed to update an observer. Reason: "+str(e))
        else:
            print("Update is Nonetype")


