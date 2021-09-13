from __future__ import print_function
import json
import time
import subprocess
import os
import os.path
import argparse
import requests
from aos.system.sdk.python.send import send_json
from aos.system.sdk.python.service_wrapper import AutonomousService
from aos.system.libs.util import Util  
from aos.system.configs.channel import __EMAIL_FIX__, PATH_PRODUCT_ID_CONFIG, CURRENT_PATH, PATH_WIFI_CONFIG, \
    BRAIN_CONFIG_PATH, PATH_USER_CONFIG, DEVICE_TYPE, PATH_PRODUCT_ADDRESS, PATH_PRODUCT_KEY_CONFIG, BASE_APP

NAME = 'incognito'
URL_INCOGNITO_NODE = "http://0.0.0.0:9334"
URL_INCOGNITO_NODE_NETWORK_MONITO="http://localhost:5000/"
HEADER_REUQUEST = {'content-type': 'application/json'} 

SYNCING = 1
READY   = 2
MINING  = 3
STOP    = 4
PENDING = 5
###########
miningStatus =[
        {"status":"offline", "message":"ready","code":READY},
        {"status":"syncing", "message":"syncing","code":SYNCING },
        {"status":"ready", "message":"ready","code":READY},
        {"status":"mining", "message":"earning","code":MINING},
        {"status":"waiting", "message":"earning","code":MINING},
        {"status":"pending", "message":"waiting to be selected","code":PENDING},
        {"status":"notmining", "message":"ready","code":READY},
    ] 
###########
def get_logs_info():
    try:
        print("start checking node status") 

        getmininginfo = {
            "jsonrpc": "1.0",
            "method": "getmininginfo",
            "params": [],
            "id": 1
        }
        
        response2=""
        response1="" 
        diskInfo=""
        try:
            response1 = requests.post(
            URL_INCOGNITO_NODE, data=json.dumps(getmininginfo), headers=HEADER_REUQUEST, timeout=5).json() 
            getchainminingstatus ={
                "jsonrpc": "1.0",
                "method": "getchainminingstatus",
                "params": [response1["Result"]["ShardID"]],
                "id": 1
            }    

            response2 = requests.post(
                URL_INCOGNITO_NODE, data=json.dumps(getchainminingstatus), headers=HEADER_REUQUEST, timeout=5 ).json() 
             
        except:  
            pass

        qrcode =""
        ipList =""
        try:
            code = Util.read_file(CURRENT_PATH+'data/qrcode.json')  
            qrcode=code["qrcode"]
        except:  
            None 
        
        try:
            ipLAN = Util.get_ip_address2()
            WifiIp =  Util.cmd("sudo ip -4 -o addr show  wlp2s0 | perl -lane 'print $F[3]'", True)
            WifiIp =WifiIp.strip(' \t\n\r')
            ipLAN = ipLAN.strip(' \t\n\r')
            ipLANs = ipLAN.split("/")
            ipLAN = ipLANs[0]
            ipList = {"lan":ipLAN, "ipWifi":WifiIp} 
        except:
            None 

        dockerps=""
        try:
            dockerps  = Util.cmd("docker inspect -f '{{with .State}} {{.Status}} {{end}}' inc_mainnet", True)
        except:
            None
        
        validatorKey =""

        try :
            if os.path.exists(CURRENT_PATH+'data/validator.json') == True :
                data_object = Util.read_file(CURRENT_PATH+'data/validator.json')  
                validatorKey = data_object["validatorKey"]
        except Exception as e:
            None  
         
        try:
            diskInfo  = Util.cmd("df -h | grep /dev/sda2", True)
        except:
            None

        data_post=json.dumps({ "diskInfo":diskInfo, "dockerps":dockerps, "ip":ipList,"validatorKey":validatorKey, "getmininginfo":response1,"getchainminingstatus":response2})

        try :
            response3 = requests.post(
                URL_INCOGNITO_NODE_NETWORK_MONITO+"/devicespis?qrcode="+qrcode, data=data_post, headers=HEADER_REUQUEST, timeout=5 ).json() 

        except:
            None 

        return {"status": {"code":"OK" ,"message":"post status"}, "networkInfo": data_post }
        
    except Exception as e:
        #print(e)  
        #print(data_post)
        print("start checking node error ")  


def get_status(): 
    dir = os.path.abspath(os.path.dirname(__file__))
    starting_file_status= dir + '/starting_file_status.dat' 
    
    response2=""
    response1="" 
    qrcode =""
    ipList =""
    diskInfo=""
    try:
        print("start checking node status")  

        getmininginfo = {
            "jsonrpc": "1.0",
            "method": "getmininginfo",
            "params": [],
            "id": 1
        } 
        
        
        try:
            #request 1
            response1 = requests.post(
            URL_INCOGNITO_NODE, data=json.dumps(getmininginfo), headers=HEADER_REUQUEST, timeout=5).json() 
            
            #request 2
            getchainminingstatus ={
                "jsonrpc": "1.0",
                "method": "getchainminingstatus",
                "params": [response1["Result"]["ShardID"]],
                "id": 1
            }    
            response2 = requests.post(
                URL_INCOGNITO_NODE, data=json.dumps(getchainminingstatus), headers=HEADER_REUQUEST, timeout=5 ).json() 
        except:  
            pass

        try:
            code = Util.read_file(CURRENT_PATH+'data/qrcode.json')  
            qrcode=code["qrcode"]
        except:  
            None 
        
        try:
            ipLAN = Util.get_ip_address2()
            WifiIp =  Util.cmd("sudo ip -4 -o addr show  wlp2s0 | perl -lane 'print $F[3]'", True)
            WifiIp =WifiIp.strip(' \t\n\r')
            ipLAN = ipLAN.strip(' \t\n\r')
            ipLANs = ipLAN.split("/")
            ipLAN = ipLANs[0]
            ipList = {"lan":ipLAN, "ipWifi":WifiIp} 
        except:
            None 

        dockerps=""
        try:
            dockerps  = Util.cmd("docker inspect -f '{{with .State}} {{.Status}} {{end}}' inc_mainnet", True)
        except:
            None

        try:
            diskInfo  = Util.cmd("df -h | grep /dev/sda2", True)
        except:
            None
        
        for item in miningStatus: 
            if item["status"]==response2["Result"] :
                result = {"status": {"code": item["code"] ,"message":item["message"] }, "networkInfo": response1["Result"],"diskInfo":diskInfo, "ipList":ipList, "getmininginfo":response1,"getchainminingstatus":response2,"dockerps": dockerps  }
                return result

        try:
            if os.path.exists(starting_file_status) == True :
                os.remove( dir + '/starting_file_status.dat')
        except:
            None 

        return {"status": {"code": SYNCING ,"message":'syncing' }, "networkInfo":"","diskInfo":diskInfo,  "ipList":ipList, "getmininginfo":response1,"getchainminingstatus":response2, "dockerps": dockerps }

    except:
        print("start checking node error ") 
        result  = Util.cmd("docker inspect -f '{{with .State}} {{.Status}} {{end}}' inc_mainnet", True)
        if result.strip(' \t\n\r') == "running" :
            return {"status": {"code": SYNCING ,"message":'syncing' }, "networkInfo":"","diskInfo":diskInfo, "ipList":ipList, "getmininginfo":response1,"getchainminingstatus":response2, "dockerps": dockerps }
        else:
            return {"status": {"code": SYNCING ,"message":result }, "networkInfo":"", "diskInfo":diskInfo, "ipList":ipList, "getmininginfo":response1,"getchainminingstatus":response2, "dockerps": dockerps}

    
def set_stop_mining(isStop):
    enablemining  = {
        "jsonrpc": "1.0",
        "method": "enablemining",
        "params":[isStop],
        "id": 1
    }
    try:
        response = requests.post(
                URL_INCOGNITO_NODE, data=json.dumps(enablemining), headers=HEADER_REUQUEST, timeout=5).json() 
        return response  
    except :
        return {"status": {"code":STOP ,"message":"notmining"}, "networkInfo": "" }

      

def start_chain(chain, privateKey ):
    
    print("+++++start_chain CALL SCRIPT ")
    dir = os.path.abspath(os.path.dirname(__file__))
    starting_file_status= 'touch ' + dir + '/starting_file_status.dat' 
    Util.cmd( starting_file_status )
    
    print("+++++start_chain clone script ")

    Util.cmd('cd ' + CURRENT_PATH+'/ability/incognito/ && curl -LO https://storage.googleapis.com/incognito/nodes/start_incognito_privatekey.sh start_incognito.sh', True)

    Util.cmd('cp -r ' + dir + '/start_incognito.sh '+  dir + '/start.sh', True ) 
    
    print("+++++start_chain sed key ")

    Util.cmd( 'sed -i "s/xxx/'+privateKey+'/" ' + dir+ '/start.sh', True )

    print("+++++start_chain run key ")

    start_script ='bash ' + dir + '/start.sh ' + privateKey 

    Util.cmd( start_script, True ) 
    
    print("+++++DONE CALL SCRIPT ") 


def start_chain_validator_key(chain, validator_key ):
    
    print("+++++start_chain CALL SCRIPT ")
    dir = os.path.abspath(os.path.dirname(__file__))
    starting_file_status= 'touch ' + dir + '/starting_file_status.dat' 
    Util.cmd( starting_file_status )
    
    print("+++++dowload script :" + CURRENT_PATH)

    Util.cmd('cd ' + CURRENT_PATH+'ability/incognito/ && curl -LO https://storage.googleapis.com/incognito/nodes/start_incognito.sh start_incognito.sh ', True)
    
    print("+++++start_chain clone script ")

    Util.cmd( 'cp -r ' + dir + '/start_incognito.sh '+  dir + '/start.sh', True)

    print("+++++start_chain sed key ")

    Util.cmd( 'sed -i "s/xxx/'+validator_key+'/" ' + dir+ '/start.sh', True)

    print("+++++start_chain run key ")

    start_script ='bash ' + dir + '/start.sh ' + validator_key 

    Util.cmd( start_script, True ) 
    
    print("+++++DONE CALL SCRIPT ") 


def stop_chain():
    dir = os.path.abspath(os.path.dirname(__file__))
    stop_script = dir + '/stop_incognito.sh' 
    #check miner docker container 
    result  = Util.cmd("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inc_miner", True)
    print(result)
 

def main(data, source):
    print("+++++ RECEIVE from brain data =>" + data)
    dir = os.path.abspath(os.path.dirname(__file__))
    try:
        data_object = json.loads(data)
        print(data_object)
        action = data_object["action"]
        if action == "start":
            chain = data_object["chain"]
            try :
                print("start with privatekey")
                privateKey = data_object["privateKey"] 
                if privateKey !="": 
                    #stored data in ~/aos/data
                    Util.write_file(CURRENT_PATH+'data/privatekey.json',data_object)   
                    start_chain(chain, privateKey)
            except Exception as e:
                print(e)   
            
            try :
                print("start with validatorKey")    
                validatorKey = data_object["validatorKey"]
                if validatorKey !="":
                    #stored data in ~/aos/data
                    print("start store data " + CURRENT_PATH+'/data/validator.json')
                    Util.write_file(CURRENT_PATH+'/data/validator.json',data_object)   
                    start_chain_validator_key(chain, validatorKey)

            except Exception as e:
                print("cant write file")
                print(e)    

            nodedata = {"status": {"code": 1 ,"message":"syncing"}, "networkInfo": "" }  
            package = {"type": "phone_control", "source": source, "data": {"action": action, "from": "incognito", 
                 "data":  {"status": 1, "data": nodedata }}}   

            send_json(package)
        
        elif action == "update-chain":
            print("start update-chain")
            try :
                if os.path.exists(CURRENT_PATH+'data/privatekey.json') == True :
                    data_object = Util.read_file(CURRENT_PATH+'data/privatekey.json')  
                    print("start with privatekey")
                    privateKey = data_object["privateKey"] 
                    if privateKey !="":
                        start_chain("", privateKey) 
            except Exception as e:
                print(e)    

            try :
                if os.path.exists(CURRENT_PATH+'data/validator.json') == True :
                    data_object = Util.read_file(CURRENT_PATH+'data/validator.json')  
                    print("start with validatorKey")    
                    validatorKey = data_object["validatorKey"]
                    if validatorKey !="":
                        start_chain_validator_key("", validatorKey)

            except Exception as e:
                print(e)    
            

        elif action == "stop":
            stop_chain()  

        elif action == "status": 
            nodedata = get_status()   
            package = {"type": "phone_control", "source": source, "data": {"action": action, "from": "incognito", 
                     "data":  {"status": 1, "data": nodedata }}}  
            print (package)
            send_json(package)
        
        elif action == "systemlogs": 
            nodedata = get_logs_info()   
            print (nodedata)
            
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '-data', help='data', required=True)
    parser.add_argument('-s', '-source', help='source', required=True)
    parser.add_argument('-p', '-protocol', help='protocol', required=False)
    args = parser.parse_args()
    main(args.d, args.s)
