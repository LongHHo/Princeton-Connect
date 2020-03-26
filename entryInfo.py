#!/usr/bin/env python

from os import path
from sys import argv, stderr, exit

class entryInfo (object):

    def __init__(self, name= None, netid= None, email= None, phone= None, description= None, address= None):
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

    def getName(self, name): 
        return self._name    
    
    def getNetid(self, netid):
        return self._netid 

    def getEmail(self, email):
        return self._email  

    def getPhone(self, phone):
        if (isinstance(phone, )):
            raise Exception('Phone number is invalid')
        return self._phone  

    def getDescription(self, description):
        return self._description  
