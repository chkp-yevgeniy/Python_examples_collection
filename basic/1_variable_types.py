#!/usr/bin/python

# Learn to use:
# - Output 
# - Variable types:
#   - Numbers (int, float)
#   - String
#   - Boolean


# Import library
import os


a="test"
b="test2"

print("a: "+a)
print("b: "+b)
a=b
a="changed a"
print("----------")
print("a: "+a)
print("b: "+b)

var1=["aaaa","bbbb","cccc"]
print("var1 at the beginning: "+str(var1))
var2 = str(var1.copy())
var1.append("zzzz")
print("var1 current state: "+str(var1))
print("var2: "+str(var2))

# Uncomment next line to activate the code below
exit()

# I am a comment

# Variable types 
## Numbers 

print("\n Numbers")
a=2
b=3.4 
c=a+b
### Print output
print("Sum (int): "+str(c))

### Convert c to string
cStr=str(c)
print("I am sum converted to str: "+cStr)

## Strings
print("\n Strings")
myString="I am a string"
myString2="1234"
### Print output
print("MyString \""+myString+"\"")
print("MyString2 \""+myString2+"\"")
### Convert str to int
myString2Int=int(myString2)
print("I am MyString2 converted to int \""+str(myString2Int)+"\"")

## Boolean
print("\n Booleans")
myBool=True
myBool2=False
print("myBool "+str(myBool))
print("myBool2 "+str(myBool2))




