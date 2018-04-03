# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 20:54:29 2016

@author: user

Singleton Class 
ensures there is only one of the said object
"""


#The local singleton is an object of which there can only be 
# one on each server

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class LocalSingleton(metaclass=Singleton):
    def __init__(self):
        pass


'''Currently ineffective'''
#Distributed Singleton is a distributed object of which there 
# can only be one on each server and all act as one object
class data:
    def __init__(self):
        pass

class DistributedSingletonInstance(metaclass=Singleton):
    def __init__(self, port=None):
        self.local = data()
        self.shared = data()
        if port is not None:
            self.port = port
        
    
    
class DistributedSingleton(object):
    def __call__(cls, *args, **kwargs):
        pass
    
    def __init__(self):
        pass

    def __getattr__(self, name):
        pass
    
    def __setattr__(self, name, value):
        pass

'''Currently ineffective'''
#Global Singleton is a singleton on a distributed system,
# such that there is only one object on the entire system
class GlobalSingleton(metaclass=Singleton):
    def __init__(self):
        pass
        

