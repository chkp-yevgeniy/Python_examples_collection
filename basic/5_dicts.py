#!/usr/bin/python

# Import library
import os


# Define a dict
gwDict = {
  "gwName": "gateway1",
  "swVersion": "R80.30",
  "idaBladeActivated": True,
  "vpnBladeActivated": False
}
print("gwDict: "+str(gwDict))

# Append an element
gwDict["gwIP"]="10.1.3.1"

# Accessing an element
print("swVersion: "+gwDict["swVersion"])

# Loop trough the dict
for key, value in gwDict.items():
  print(str(key)+": "+str(value))

# Check if a key exists
if "idaBladeActivated" in gwDict:
  print("idaBladeActivated is in my dict")
