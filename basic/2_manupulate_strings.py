#!/usr/bin/python

# Import library
import os

myStr="hello"
myStr2="world"
# String is a list
for letter in myStr:
  print("letter: "+letter)

# Concatenate strings
mySentence=myStr+" "+myStr2
print("mySentence: "+mySentence)

# String manipulations
## Check if contains 
if mySentence.find("world"):
  print("found")

## Find and replace
mySentenceNew=mySentence.replace("h", "jjj")
print(mySentenceNew)

## Check if string is not empty
myStr3="ff"
if not myStr3:
  print("myStr3 is empty")

## Put string into a list
myList=mySentence.split(" ")
print("myList: "+str(myList))

