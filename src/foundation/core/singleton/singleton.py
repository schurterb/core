# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 20:54:29 2016

@author: user

Singleton Class 
ensures there is only one of the said object
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#The local singleton is an object of which there can only be 
# one on each server

class LocalSingleton(metaclass=Singleton):
    def __init__(self):
        pass
