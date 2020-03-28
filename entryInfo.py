#!/usr/bin/env python

from os import path
from sys import argv, stderr, exit

class entryInfo (object):

    def __init__(self, name= '', netid= '', email= '', phone= '', description= '', address= ''):
        self._name = name
        self._netid = netid
        self._email = email
        self._phone = phone
        self._description = description
        self._address = address

    def setName(self, name): 
        self._name = name    
    
    def setNetid(self, netid):
        self._netid = netid   

    def setEmail(self, email):
        self._email = email   

    def setPhone(self, phone):
        self._phone = phone   

    def setDescription(self, description):
        self._description = description   

    def getName(self): 
        return self._name    
    
    def getNetid(self):
        return self._netid 

    def getEmail(self):
        return self._email  

    def getPhone(self):
        return self._phone  

    def getDescription(self):
        return self._description  
    
    
    def getAddress(self):
        return self._address  
