# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 18:37:40 2017

@author: user

Base Message type for sending across channel
"""

import time

class Message(type):
    
    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination
        self.timestamp = time.time()