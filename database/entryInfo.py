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
        if (name is None):
            name = ''
        self._name = name    
    
    def setNetid(self, netid):
        if (netid is None):
            netid = ''
        self._netid = netid   

    def setEmail(self, email):
        if (email is None):
            email = ''
        self._email = email   

    def setPhone(self, phone):
        if (phone is None):
            phone = ''
        self._phone = phone   

    def setDescription(self, description):
        if (description is None):
            description = ''
        self._description = description 

    def setAddress(self, address):
        if (address is None):
            address = ''
        self._address = address  
    
    # get method returns raw string as is
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

    # ret method returns modified string for sql queries 

    def retName(self): 
      if (self._name == ''):
          return '%'
      else:
        newString = '%' + self._name + '%'
        return newString
    
    def retNetid(self): 
      if (self._netid == ''):
          return '%'
      else:
        newString = '%' + self._netid + '%'
        return newString
    
    def retEmail(self): 
      if (self._email == ''):
          return '%'
      else:
        newString = '%' + self._email + '%'
        return newString
    
    def retPhone(self): 
      if (self._phone == ''):
          return '%'
      else:
        newString = '%' + self._phone + '%'
        return newString
    
    def retDescription(self): 
      if (self._description == ''):
          return '%'
      else:
        newString = '%' + self._description + '%'
        return newString

    def retAddress(self): 
      if (self._address == ''):
          return '%'
      else:
        newString = '%' + self._address + '%'
        return newString
    
    # returns user Information as a complete string
    def retUserInfo(self):
        string = self._name +  '  ' + self._netid + '  ' + \
            self._email + '  ' + \
            self._phone + '  ' + \
            self._description + '  ' + self._address
        return string
        
    
