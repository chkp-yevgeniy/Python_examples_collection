#!/usr/bin/python3

import sys, os


import csv

txt = "The firewalls are for the protection"

# Write a csv file
my_csv_file="firewalls.csv"
listOfRowLists=[]
# We fill here the list with the lists
listOfRowLists.append(["gwName","swVersion", "ip"])
listOfRowLists.append(["gw1","R80.10", "10.1.1.1"])
listOfRowLists.append(["gw2", "R80.10", "10.1.1.2"]) 

# with open(my_csv_file, 'w', newline="") as file:
with open(my_csv_file, 'w') as file:
  writer=csv.writer(file, delimiter=";")  
  for rowList in listOfRowLists:        
    print("rowList: "+str(rowList))
    writer.writerow(rowList)

print("\nPrint content of created file.")
print("Run Linux shell command with os.system.")
os.system("cat "+my_csv_file)

print("\nRead the csv file, write each line into rowList") 
listOfRowLists=[]
with open(my_csv_file, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader, None)
    print("headers:"+str(headers))# Read csv         
    for rowList in reader:        
        print("Csv row:"+str(rowList))# Read csv       
