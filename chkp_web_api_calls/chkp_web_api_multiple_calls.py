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

## This tool sends multiple web api calls to chkp management server.

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


def send_api_call(_api_call_name, _body_json, _env_d, _sid_file):
  sid=""
  
  # Get sid  
  if _api_call_name!="login":
    print("--- --- 3.1 Get sid")
    with open(_sid_file) as f:
      sid_d = json.load(f)    
    if "sid" in sid_d:
      sid=sid_d["sid"]
    else: 
      print("ERROR: sid is not found. Please make sure terraform has stored an actual sid in sid.json")
      exit(1)
    print("sid: "+sid)

  print("--- --- 3.2 Prepare headers")
  if _api_call_name=="login":
    headers = {'Content-type': 'application/json'}  
  else: 
    headers = {'Content-type': 'application/json', 'X-chkp-sid': sid}

  
  print("--- --- 3.3 Send API")
  url="/web_api/"+_api_call_name  
  response=sendHttpsPost(_env_d["CHECKPOINT_SERVER"], _env_d["CHECKPOINT_PORT"], url, headers, _body_json)
  response_d=json.loads(response)
  
  print("--- --- 3.4 Response:")
  print(response_d)
  # If "login" API call
  if _api_call_name=="login":
    if response_d["sid"]:
      print(_api_call_name+" successful")
    else: 
      print("ERROR: "+_api_call_name+" failed")            
  # If not "login" API call
  else: 
    if "errors" in response_d:
      print("ERROR: WEB API call failed")
    else: 
      print("WEB API call successful")


  if _api_call_name=="login":
    print("--- ---- 3.5 Save session id in"+_sid_file)   
    with open(_sid_file, 'w') as outfile:
      json.dump(response_d, outfile)   


def main():
  sid_file="../vars/sid.json"

  print("--- 1. Get vars from env")
  #pprint.pprint(os.environ)
  env_d=os.environ
  print("Print MGMT access data:")
  print(env_d["CHECKPOINT_PORT"])
  print(env_d["CHECKPOINT_SERVER"])
  print(env_d["CHECKPOINT_USERNAME"])
  print(env_d["CHECKPOINT_PASSWORD"]) 
  print(env_d["CHECKPOINT_DOMAIN"])

  
  #################################################
  #           Your API calls                      #  
  #################################################

  print("#################### login ######################")
  print("--- 2.1 Prepare API call vars")    
  api_call_name="login"
  body = {"user": env_d["CHECKPOINT_USERNAME"], "password": env_d["CHECKPOINT_PASSWORD"], "domain": env_d["CHECKPOINT_DOMAIN"] }
  body_json = json.dumps(body)  
  pprint.pprint(body_json)
  
  print("--- 2.2 Send API call "+api_call_name)    
  send_api_call(api_call_name, body_json, env_d, sid_file)


  print("#################### add-host ######################")
  print("--- 2.1 Prepare API call vars")    
  api_call_name="add-host"
  hostname="host_9"
  ip_address="10.1.1.9"
  body = {"name": hostname, "ip-address": ip_address}
  body_json = json.dumps(body)  
  pprint.pprint(body_json)
  
  print("--- 2.2 Send API call")    
  send_api_call(api_call_name, body_json, env_d, sid_file)


  print("#################### Publish ######################")
  print("--- 2.1 Prepare API call vars")    
  api_call_name="publish"
  body = {}
  body_json = json.dumps(body)  
  pprint.pprint(body_json)
  
  print("--- 2.2 Send API call")    
  send_api_call(api_call_name, body_json, env_d, sid_file)


  print("#################### logout ######################")
  print("--- 2.1 Prepare API call vars")    
  api_call_name="logout"
  body = {}
  body_json = json.dumps(body)  
  pprint.pprint(body_json)
  
  print("--- 2.2 Send API call "+api_call_name)    
  send_api_call(api_call_name, body_json, env_d, sid_file)




if __name__ == "__main__":
    # execute only if run as a script
    main()



