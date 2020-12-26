#!/usr/bin/python3

import http.client
import json
import ssl
import os
import pprint
import json
import time

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


  print("--- 2. Get sid")
  with open(sid_file) as f:
    sid_d = json.load(f)
  #pprint.pprint(sid_d)  
  if "sid" in sid_d:
    sid=sid_d["sid"]
  else: 
    print("ERROR: sid is not found. Please make sure terraform has stored an actual sid in sid.json")
    exit(1)
  print("sid: "+sid)


  print("--- 3. Prepare header and body for CHKP web api call")
  headers = {'Content-type': 'application/json', 'X-chkp-sid': sid}  
  body = {}
  body_json = json.dumps(body)  


  print("--- 4. Execute publish")
  url="/web_api/publish"  
  response=sendHttpsPost(env_d["CHECKPOINT_SERVER"], env_d["CHECKPOINT_PORT"], url, headers, body_json)
  response_d=json.loads(response)
  print("Response:")
  print(response_d)
  if "task-id" in response_d:
    print("Publish successful")
  else: 
    print("ERROR: Publish failed")            

  time.sleep(2)

  print("--- 5. Execute logout")
  url="/web_api/logout"  
  response=sendHttpsPost(env_d["CHECKPOINT_SERVER"], env_d["CHECKPOINT_PORT"], url, headers, body_json)
  response_d=json.loads(response)
  print("Response:")
  print(response_d)  
  if "message" in response_d:
    print(response_d["message"])
    if response_d["message"]=="OK":
      print("Logout successful")
    else: 
      print("ERROR: Logout failed")    
      exit(1)
  #print("Successfully finished")
  

if __name__ == "__main__":
    # execute only if run as a script
    main()



