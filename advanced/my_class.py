#!/usr/bin/python

import sys, os


class Firewall:
   # Class attribute
    name = ""
    version=""
    ip= ""    
   
    def __init__(self, _name, _version, _ip):
      self.name = _name
      self.version = _version
      self.ip = _ip      
    
    # Public method
    def to_str(self):      
      print("--------------")
      print("Firewall "+self.name+" Version"+self.version)   
      self.__print_ip()

    # Private method
    def __print_ip(self):
      print("Firewall IP:"+self.ip)   




### Start MAIN here
print("Start to work with classes")

firewall_objs_list=[]

# Create object for FW1 
fwObj1=Firewall("fw1", "R80.10", "10.1.1.1")
# Create object for FW2
fwObj2=Firewall("fw2", "R80.30", "10.1.1.2")

# Put the objects in the list 
firewall_objs_list.append(fwObj1)
firewall_objs_list.append(fwObj2)


for fw_obj in firewall_objs_list:
  fw_obj.to_str()  
