#!/usr/bin/python3

# Import library
import os

# # Define a list 
# bladesList=["fw", "vpn", "ida"]

# # Print the list 
# print("bladesList: "+str(bladesList))

# # Add an element to the list
# bladesList.append("ips")
# # Delete the element on position 1 from the list
# bladesList.pop(1)

# # Print the list 
# print("bladesList: "+str(bladesList))

# # Loop through the list
# for blade in bladesList:
#   print("blade: "+blade)





# Define a list 
bladesList=["fw", "vpn", "ida"]

# Print the list 
print("bladesList: "+str(bladesList))

# Add an element to the list
bladesList.append("ips")
# Delete the element on position 1 from the list
bladesList.pop(1)

# Print the list 
print("bladesList: "+str(bladesList))

# Loop through the list
for blade in bladesList:
  print("blade: "+blade)

# Check if ips is in the list 
if "ips" in bladesList: 
  print("ips is in list")


# Check if ips is in the list 
# if "ips" in bladesList: 
#   print("ips is in list")

