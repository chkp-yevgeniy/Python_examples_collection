#!/usr/bin/python3

import sys, os


#!/usr/bin/python
import os
import re

txt = "The firewalls are for the protection"

print("Check if string matches a regex expression")
regexExpr="^The.*fire.*$"
rslt = re.search(regexExpr, txt)
if rslt: 
  print("matches")
else:
  print("don't matches")
print(rslt)


#exit()

print("\nGet a substring from string")
rslt = re.search('The(.*)are', txt)
if rslt:
    found = rslt.group(1)
#print(rslt.group)
print(found)

#exit()

print("\nGet all matches into a list")
rslt2 = re.findall("[Tt]he", txt)
print(rslt2)

# exit()

print("\nSplit a string into list")
rslt3 = re.split("\s", txt)
print(rslt3)

#exit()

print("\nReplace")
rslt4 = re.sub("[Tt]he", "", txt)
print(rslt4)