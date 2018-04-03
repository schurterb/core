# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:27:30 2016

@author: schurterb

An ID class useful for identifying nodes and subnodes
"""

import re

class Id():
    
    data = None
    length = 0
                
    def _validate_data(self, data):       
        if type(data) == list and [type(x) is int for x in data]:
            return True
        elif type(data) == str and (re.match('^[.0-9]*$', data)):
            return True         
        elif type(data) == int:
            return True
        else:
            return False            
            
    def __init__(self, value=None):
        if value is not None:
            if self._validate_data(value):
                if type(value) is list:
                    self.data = value
                    self.length = len(value)
                else:
                    self.data = [int(x) for x in value.split('.')]
                    self.length = len(self.data)
            else:
                raise(AttributeError("Invalid ID data"))
        
    def __setattr__(self, name, value):
        if self._validate_data(value):
            if name is "parent":        
                if type(value) is list:
                    parent = value
                else:
                    parent = [int(x) for x in value.split('.')]
                self.data = parent + self.child
                self.length = len(self.data)
            elif name is "child":
                if type(value) is list:
                    raise(AttributeError("Invalid ID data"))
                elif type(value) is str and '.' in value:
                    raise(AttributeError("Invalid ID data"))
                else:            
                    self.data = self.parent + [int(value)]
            elif name is "data" or name is "full":
                self.__dict__["data"] = value
            elif name is "len" or name is "length":
                self.__dict__["length"] = value
            else:
                raise(AttributeError("Unable to set attribute"))
        else:
            raise(AttributeError("Invalid ID data"))
            
    def __getattr__(self, name):
        if name is "parent":
            if self.length <= 1:
                return ID()
            return ID([x for x in self.data[:self.length-1]])
        elif name is "child":
            if self.data is None:
                return None
            return self.data[self.length-1]
        elif name is "full":
            return self.data
        elif name is "len":
            return self.length
        else:
            raise(AttributeError("Unable to access attribute"))
            
    def __str__(self):
        if self.data is not None:
            return '.'.join([str(x) for x in self.data])
        else:
            return ''
    
    def __hash__(self):
        res = 0
        for i in range(self.length):
            res += self.data[self.length-i-1] * pow(10,i)
        return res
        
    def __eq__(self, other):
        if self.length == other.length:
            return self.data == other.data
        else:
            return False
        