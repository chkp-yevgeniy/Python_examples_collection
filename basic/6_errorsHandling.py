#!/usr/bin/python3

# Import library
import os

# Define a dict
gwDict = {
  "gwName": "gateway1",
  "swVersion": "R80.30",
  #"idaBladeActivated": True  
}
# # Access a dict element 
# print(gwDict["idaBladeActivated"])


# Access a dict element 
try: 
  print(gwDict["idaBladeActivated"])
except KeyError: 
  print("We have an error")
