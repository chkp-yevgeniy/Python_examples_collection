#!/usr/bin/python

import sys, os
import subprocess


print("\n Execute shell command, print output into stdout")
my_command="ls -al" # For linux 
# my_command="dir"  # For Windows
os.system(my_command)

print("\n Execute shell command, print output into stdout, get return code")
my_command="ls -al" # For linux 
# my_command="dir"  # For Windows
return_code = os.system(my_command)
print("Following command executed: "+str(my_command))
print("Command return code: "+str(return_code))

# For linux 
print("\n Execute shell command, get stdout and strderr")
my_command="ls -al" # For linux 
# my_command="dir"  # For Windows
process = subprocess.Popen(my_command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print("stdout: "+str(stdout))
print("stderr: "+str(stderr))

print("Type of stdout: "+str(type(stdout)))
print("Type of stderr: "+str(type(stderr)))

# # For Windows
# print("\n Execute shell command, get stdout and strderr")
# my_command=["ipconfig", "/all"]
# process = subprocess.Popen(my_command, shell="False", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()
# print("stdout: "+str(stdout))
# print("stderr: "+stderr)
