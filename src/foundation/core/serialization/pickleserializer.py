# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:14:18 2017

@author: user

Serialization core class based an Python's Pickle library
"""

from foundation.core.log import Logger
import pickle

class PickleSerializer(object):
    
    __log = Logger("network", "serializer")    
    
    def serialize(self, obj):
        try:
            data = pickle.dumps(obj, 2)
        except:
            self.__log.error("Failed to serialize object of type "+str(type(obj)))
            self.__log.debug("Unserializable data: "+str(obj))
            data = None
        return data
        
    def deserialize(self, data):
        try:
            obj = pickle.loads(data)
        except:
            self.__log.error("Failed to deserialize data: "+str(data))
            self.__log.debug("Undeserializable data: "+str(data))
            obj = None
        return obj