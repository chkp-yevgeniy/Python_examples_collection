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
# export CHECKPOINT_SERVER=192.168.168.100
# export CHECKPOINT_USERNAME=admin2
# export CHECKPOINT_PASSWORD=qwe123
# export CHECKPOINT_PORT=443
# export CHECKPOINT_DOMAIN="CMA1"


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


  hostname="host_2"
  ip_address="10.1.1.2"
  
  print("--- 3. Prepare header and body for CHKP web api call: add_host")
  headers = {'Content-type': 'application/json', 'X-chkp-sid': sid}  
  body = {"name": hostname, "ip-address": ip_address}
  body_json = json.dumps(body)  


  print("--- 4. Execute add-host")
  url="/web_api/add-host"  
  response=sendHttpsPost(env_d["CHECKPOINT_SERVER"], env_d["CHECKPOINT_PORT"], url, headers, body_json)
  response_d=json.loads(response)
  print("Response:")
  print(response_d)
  if "errors" in response_d:
    print("ERROR: WEB API call failed")
  else: 
    print("WEB API call successful")



if __name__ == "__main__":
    # execute only if run as a script
    main()



