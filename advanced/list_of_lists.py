#!/usr/bin/python

import sys, os


#!/usr/bin/python
import os

# Lists already discussed 
# But we can nest the lists as presented below
networkGroup1=[]
networkGroup2=[]
networkGroups=[]

# Fill first network group
networkGroup1.append("10.1.1.1")
networkGroup1.append("10.1.1.2")
networkGroup1.append("10.1.1.3")

# Fill second network group
networkGroup2.append("10.100.1.1")
networkGroup2.append("10.100.1.2")
networkGroup2.append("10.100.1.3")

# Put network groups into a list
networkGroups.append(networkGroup1) 
networkGroups.append(networkGroup2) 

print("networkGroups: "+str(networkGroups))
