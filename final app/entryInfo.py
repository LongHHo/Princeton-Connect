#!/usr/bin/env python

from os import path
from sys import argv, stderr, exit

class entryInfo (object):

    def __init__(self, name= '', netid= '', email= '', phone= '', description= '', address= '', city=''):
        self._name = name
        self._netid = netid
        self._email = email
        self._phone = phone
        self._description = description
        self._address = address
        self._city = city

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

    def setCity(self, city):
        if (city is None):
            city = ''
        self._city = city  
    
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

    def getCity(self):
        return self._city  

    def getAddress(self):
        return self._address 

    # ret method returns modified string for sql queries 

    def retName(self): 
      if (self._name == ''):
          return '%'
      else:
        newString = ""
        for char in self._name:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString
    
    def retNetid(self): 
      if (self._netid == ''):
          return '%'
      else:
        newString = ""
        for char in self._netid:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString
    
    def retEmail(self): 
      if (self._email == ''):
          return '%'
      else:
        newString = ""
        for char in self._email:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString
    
    def retPhone(self): 
      if (self._phone == ''):
          return '%'
      else:
        newString = ""
        for char in self._phone:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString
    
    def retDescription(self): 
      if (self._description == ''):
          return '%'
      else:
        newString = ""
        for char in self._description:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString

    def retAddress(self): 
      if (self._address == ''):
          return '%'
      else:
        newString = ""
        for char in self._address:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString

    def retCity(self): 
      if (self._city == ''):
          return '%'
      else:
        newString = ""
        for char in self._city:
          if (char == "%"):
             char = "\%"
          elif(char == "_"):
             char = "\_"
          newString += char
        newString = '%' + newString + '%'
        return newString
    
    # returns user Information as a complete string
    def retUserInfo(self):
        string = self._name +  '  ' + self._netid + '  ' + \
            self._email + '  ' + \
            self._phone + '  ' + \
            self._description + '  ' + self._address
        return string
        
    
