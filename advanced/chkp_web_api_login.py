#!/usr/bin/python3

import http.client
import json
import ssl
import os
import pprint
import json
import time
from pathlib import Path
import ast

## This tool sends publish and logout to mgmt server

## Make sure following parameters are conifigured as env vars:
# export CHECKPOINT_SERVER=10.211.55.10
# export CHECKPOINT_USERNAME=automation_user
# export CHECKPOINT_PASSWORD=qwe123
# export CHECKPOINT_PORT=433
# export CHECKPOINT_DOMAIN="CMA2"

def sendHttpsPost(_ip, _port, _url, _headers, _body):  
  conn = http.client.HTTPSConnection(_ip+":"+_port, context = ssl._create_unverified_context())
  conn.request('POST', _url, _body, _headers)
  response = conn.getresponse()
  #print("\n Response")
  #print(response.read().decode())
  return response.read().decode()


def main():
  sid_file="../vars/sid.json"
  print("Execute publish and logout for Terraform plan")

  print("--- 1. Get vars from env")
  #pprint.pprint(os.environ)
  env_d=os.environ


  print("--- 2. Prepare header and body")  
  headers = {'Content-type': 'application/json'}  
  body = {"user": env_d["CHECKPOINT_USERNAME"], "password": env_d["CHECKPOINT_PASSWORD"], "domain": env_d["CHECKPOINT_DOMAIN"] }
  body_json = json.dumps(body)  
  pprint.pprint(body_json)


  print("--- 3. Send Login API call")
  url="/web_api/login"  
  response=sendHttpsPost(env_d["CHECKPOINT_SERVER"], env_d["CHECKPOINT_PORT"], url, headers, body_json)
  response_d=json.loads(response)
  print("Response:")
  print(response_d)
  if response_d["sid"]:
    print("Login successful")
  else: 
    print("ERROR: Login failed")            
    

  print("--- 4. Save reponse into "+sid_file)   
  with open(sid_file, 'w') as outfile:
    json.dump(response_d, outfile)   



if __name__ == "__main__":
    # execute only if run as a script
    main()



