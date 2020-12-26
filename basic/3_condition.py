#!/usr/bin/python

# Import library
import os

print("Get relevant blade.")
relevantBlade="ida"
print("RelevantBlade is: "+ relevantBlade)
if relevantBlade=="vpn": 
  print("  Perform actions on vpn blade")
  # Start here to work on vpn blade
elif relevantBlade=="ida": 
  print("  Perform actions on vpn blade")
  # Start here to work on ida blade
else:
  print("  Blade type is unknown")


