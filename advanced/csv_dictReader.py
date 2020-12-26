#!/usr/bin/python

import csv

#input_file = csv.DictReader(open("people.csv"))

# for item in input_file:
#   print("dict item: "+str(item))
#   print(item["name"])


with open('people.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=";")
  print("Reader type: "+str(type(reader)))
  for row in reader:    
      print("Row of dictReader "+str(row))
      print("Type of row from dictReader"+str(type(row)))
      print("name: "+row['name']+", age: "+row['age'])
      

  print("input_file: "+str(reader))
