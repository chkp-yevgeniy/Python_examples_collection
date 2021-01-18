#!/usr/bin/python

# (c) 2020 Check Point Software Technologies
#
# Tool to execute commands on multiple remote machines
#
# VER   DATE            WHO                     WHAT
#------------------------------------------------------------------------------
# v1.0 01.12.2020               Yevgeniy Yeryomin       Creation of the script

# How to run: 
# ./runRemoteCmd.py
# 
# 

# ToDO: 
# - Close ssh session


import os
import os.path as path
import sys
import logging
import yaml
import paramiko
import re
#from ansible_vault import Vault
import time
import datetime
import pprint
import json
import collections
import csv

this_script_path = path.abspath(path.join(__file__, ".."))
sys.path.append(os.path.abspath(os.path.join(this_script_path+"/../")))

project_abs_path=this_script_path+"/../../"

def getLogger(_log_file):
  # Vars
  script_file="run_remote_commands"  
  this_script_path = path.abspath(path.join(__file__, ".."))
  #print("this_script_path "+this_script_path)
  #log_file=project_abs_path + "logs/execute_cmds.log"
  #fileHandlerLevel=logging.DEBUG
  #streamHandlerLevel=logging.DEBUG
  fileHandlerLevel=logging.INFO
  streamHandlerLevel=logging.INFO
  # Create logger instance 
  logger = logging.getLogger(script_file)
  logger.setLevel(logging.DEBUG)
  # create file handler which logs even debug messages
  fh = logging.FileHandler(_log_file)
  fh.setLevel(fileHandlerLevel)
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  # ch.setLevel(logging.ERROR)
  ch.setLevel(streamHandlerLevel)
  # create formatter and add it to the handlers
  formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  # add the handlers to the logger
  logger.addHandler(fh)
  logger.addHandler(ch)

  return logger


def runCmdsOnTarget(_target_dict, _cmds_list, user, pwd):
  result_dict=collections.OrderedDict()
  cmd_result_list=[]
  result_dict["gw_name"]=_target_dict["gw_name"]
  result_dict["gw_ipaddr"]=_target_dict["gw_ipaddr"]
  result_dict["gw_domain"]=_target_dict["gw_domain"]
  result_dict["ssh_access"]=""
  result_dict["cmds_ok"]=0
  result_dict["cmds_failed"]=0
  result_dict["cmd_result_list"]=cmd_result_list
  
  cmds_ok=0
  cmds_failed=0

  
  
  lg.debug("target_dict"+str(_target_dict))  
  target_ip=_target_dict["gw_ipaddr"]
  target_name=_target_dict["gw_name"]
  lg.info("target host: "+ target_ip+" "+target_name)  

  # Create ssh access to the target
  ssh=paramiko.SSHClient()  
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.load_system_host_keys()
    
  try:
    ssh.connect(target_ip,22,user,pwd)
    #ssh.connect(target_ip,22,user,pwd, timeout=3)    
    #ssh.connect("10.1.1.22",22,user,"pwd", timeout=3)
    result_dict["ssh_access"]="ok"
    lg.info("ssh connection established")
  except:
    lg.error("SSH connection to ") #+target_name+" "+target_ip+" failed.")
    result_dict["ssh_access"]="failed"
    return result_dict

  for cmd_dict in _cmds_list:
    cmd_rslt_dict=collections.OrderedDict()
    cmd_result_list.append(cmd_rslt_dict)
    cmd=cmd_dict["command"]  
    #cmd="dafsd"
    cmd_rslt_dict["cmd"]=cmd
    lg.debug("cmd_dict: "+str(cmd_dict))    
    lg.info("run cmd: "+cmd)
    stdin,stdout,stderr=ssh.exec_command(cmd)
    stdout_list=stdout.readlines()
    stderr_list=stderr.readlines()
    #print("stderr_list: "+str(stderr_list))
    
    if stderr_list:      
      cmd_rslt_dict["result"]="failed"
      cmd_rslt_dict["output"]=stderr_list
      lg.info(" Result: failed")    
      cmds_failed=cmds_failed+1
    elif "Invalid command" in str(stdout_list):
        cmd_rslt_dict["result"]="failed"
        cmd_rslt_dict["output"]=stdout_list
        lg.debug("stdout_list "+str(stdout_list))
        lg.info(" Result: failed")    
        cmds_failed=cmds_failed+1
    else:
      cmd_rslt_dict["result"]="ok"      
      cmd_rslt_dict["output"]=stdout_list
      lg.debug("stdout_list "+str(stdout_list))
      lg.info(" Result: ok")    
      cmds_ok=cmds_ok+1

  result_dict["cmds_ok"]=cmds_ok
  result_dict["cmds_failed"]=cmds_failed      

    #lg.info("result_dict: "+str(result_dict))

  return result_dict


def writeReports(_rslt_dict, _report_files):
  lg.info("Write json report")
  #with open(_report_files["detailed_json"], 'w', encoding='utf-8') as f:
  with open(_report_files["detailed_json"], 'a') as f:
    json.dump(_rslt_dict, f, ensure_ascii=False, indent=4)  
  
  lg.info("Write csv report")
  #f = csv.writer(open(_report_files["short_csv"], "wb+"))
  with open(_report_files["short_csv"], 'a' ) as f:
    csv_w = csv.writer(f)
    #csv_w.writerow(["gw_name", "gw_ipaddr", "gw_domain", "ssh_access", "cmd_result", "cmd"])
    for cmd_rslt in _rslt_dict["cmd_result_list"]:    
      csv_w.writerow([_rslt_dict["gw_name"],
               _rslt_dict["gw_ipaddr"], 
               _rslt_dict["gw_domain"],
               _rslt_dict["ssh_access"], 
               cmd_rslt["result"],
               cmd_rslt["cmd"]])
    
    if not _rslt_dict["cmd_result_list"]:
      csv_w.writerow([_rslt_dict["gw_name"],
               _rslt_dict["gw_ipaddr"], 
               _rslt_dict["gw_domain"],
               _rslt_dict["ssh_access"], 
               "",
               ""])


### MAIN 
def main():

  global lg  

  user="admin"
  # FIXME: user public key authentication instead of pwd
  # If using pwd, it has to be saved in a secure manner
  pwd="qwe123"

  _log_file=project_abs_path+"remote_cmds.log"
  lg=getLogger(_log_file)
  lg.info("### ### ### Start tool to run remote commands ### ### ###")  
  lg.info("This_script_path: "+this_script_path)
  lg.info("Project_abs_path: "+project_abs_path)
  lg.info("All logs will be written in : "+_log_file)
  #exit()

  curDateTimeYMD_HMS=os.popen('date +%Y%m%d_%H%M%S').read().strip()
  report_files={}
  report_files["short_csv"]="../output/run_rcmds_short_"+curDateTimeYMD_HMS+".csv"  
  report_files["detailed_json"]="../output/run_rcmds_detailed_"+curDateTimeYMD_HMS+".json"  
  lg.info("Reports will be written in:")
  lg.info("Report short csv: "+report_files["short_csv"])  
  lg.info("Report detailed json : "+report_files["detailed_json"])
  
  lg.info("Create csv report file and write header")
  with open(report_files["short_csv"], 'w' ) as f:
    csv_w = csv.writer(f)
    csv_w.writerow(["gw_name", "gw_ipaddr", "gw_domain", "ssh_access", "cmd_result", "cmd"])

  #ToDo Put them as arguments
  cmds_file="../vars/shell_commands_list.yml"
  targets_file="../vars/target_hosts.yml"
  lg.info("----Input data--------")
  lg.info("Commands list will be imported from: "+cmds_file)
  lg.info("Targets list will be imported from: "+targets_file)
  lg.info("----------------------")
 
  # Commands result output report short
  # time; target_name; target_ip; command; result; success/failed

  
  lg.info("--- 0. Get arguments")

  lg.info("--- 1. Get list of targets")
  targets_list=[]
  with open(targets_file, 'r') as stream:
    targets_list = yaml.safe_load(stream)
  targets_list=targets_list["gateways"]
  lg.info("Targets imported into list")
  #pprint.pprint(targets_list)
  # ToDo:
  #lg.info("Verify list")


  lg.info("--- 2. Get list of commands to be executed")
  cmds_list=[]
  with open(cmds_file, 'r') as stream:
    cmds_list = yaml.safe_load(stream)  
  cmds_list=cmds_list["shellCommands"]
  lg.info("Commands imported into list")
  #pprint.pprint(cmds_list)
  # ToDo:
  #lg.info("Verify list")
  

  lg.info("--- 2.1. Following commands will be executed on following targets:")
  lg.info("Commands:")
  for cmd in cmds_list:
    lg.info(cmd["command"])
  lg.info("Targets:")
  for target in targets_list:
    lg.info(target["gw_name"]+" "+target["gw_ipaddr"])
  lg.info("Do you want to run commands (listed above) on the gateways (listed above)?")  
  lg.info("If \"yes\", hit enter. If \"no\", hit escape.")  
  choice = raw_input().lower()
  #print(choice)


  lg.info("--- 3. Run commands on each target")
  rslt_list=[]
  if cmds_list and targets_list: 
    for target in targets_list:       
      rslt_dict=runCmdsOnTarget(target, cmds_list, user, pwd)

      #pprint.pprint(rslt_dict)
      writeReports(rslt_dict, report_files)
      rslt_list.append(rslt_dict)



  lg.info("--- 4. Summary")    
  
  # Get data for summary 
  #targets_avail_via_ssh_status=[d['ssh_access'] for d in rslt_list if 'ssh_access' in d]
  targets_ssh_access_ok=[d['ssh_access'] for d in rslt_list if d['ssh_access']=="ok"]
  lg.debug("targets_ssh_access_ok: "+str(targets_ssh_access_ok))
  targets_ssh_access_failed=[d['ssh_access'] for d in rslt_list if d['ssh_access']!="ok"]
  lg.debug("targets_ssh_access_failed: "+str(targets_ssh_access_failed))

  cmds_ok_l=[d['cmds_ok'] for d in rslt_list if 'cmds_ok' in d]  
  cmds_failed_l=[d['cmds_failed'] for d in rslt_list if 'cmds_failed' in d]    
  cmds_ok_num=sum(cmds_ok_l)   
  cmds_failed_num=sum(cmds_failed_l)   
  #cmds_ok_num=reduce(lambda x, y: (int(x) + int(y)), cmds_ok_l)  

  lg.info("Targets total:         "+str(len(targets_list)))
  lg.info("Targets reachable:     "+str(len(targets_ssh_access_ok)))
  lg.info("Targets NOT reachable: "+str(len(targets_ssh_access_failed)))
  lg.info("Commands total:        "+str(len(cmds_list)))
  lg.info("Commands successfull:  "+str(cmds_ok_num))
  lg.info("Commands failed:       "+str(cmds_failed_num))
  
  # Get data per target
  lg.info("Summary per target:")
  #lg.info("target_name     target_ip,     cmds_ok,  cmds_failed")
  #lg.info({} {} {} "target_name","target_ip", "ssh_access", "cmds_ok", "cmds_failed")
  lg.info("{:23} {:15} {:10} {:10} {:5}".format("target_name","target_ip", "ssh_access", "cmds_ok", "cmds_failed"))
  for rslt_dict in rslt_list:    
    #lg.info(rslt_dict["gw_name"]+" "+rslt_dict["gw_ipaddr"]+" "+rslt_dict["ssh_access"] +"  "+str(rslt_dict["cmds_ok"])+"  "+str(rslt_dict["cmds_failed"]))
    lg.info("{:23} {:15} {:10} {:10} {:5}".format(rslt_dict["gw_name"],rslt_dict["gw_ipaddr"],rslt_dict["ssh_access"],str(rslt_dict["cmds_ok"]),str(rslt_dict["cmds_failed"])))

  lg.info("SUCCESSFULLY FINISHED")
  lg.info("Reports were written in:")
  lg.info("Report short csv:      "+report_files["short_csv"])  
  lg.info("Report detailed json : "+report_files["detailed_json"])

if __name__ == "__main__":
    main()