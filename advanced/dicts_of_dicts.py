#!/usr/bin/python3

import sys, os



#### Option A
anthony='anthony'
maxime='maxime'
famille = {
  anthony: {'name': 'Antho', 'age': '35', 'sex': 'Male', 'speaking langage':['french','english']},
  maxime: {'name': 'Max', 'age': '31', 'sex': 'Male', 'speaking langage':['french']}
  }

print("Anthony:")
print(famille[anthony])
print(famille[anthony]['speaking langage'])
print("Maxime:")
print(famille[maxime])
print(famille[maxime]['speaking langage'])

print("------------------------")

#### Option B
# anthony='anthony'
# maxime='maxime'
famille = {
  'anthony': {'name': 'Antho', 'age': '35', 'sex': 'Male', 'speaking langage':['french','english']},
  'maxime': {'name': 'Max', 'age': '31', 'sex': 'Male', 'speaking langage':['french']}
  }

print("Anthony:")
print(famille['anthony'])
print(famille['anthony']['speaking langage'])
print("Maxime:")
print(famille['maxime'])
print(famille['maxime']['speaking langage'])