
import os

import thread

import time
from datetime import *
import sys
import zmq
import json
 
from aos.ability.install_ability_device.install_app import InstallUpdateAbility
from messages import MESSAGE
from help import Help
from run_update import RunUpdate
from aos.system.libs.ability import Ability
from aos.system.libs.device import Device

from aos.system.configs.channel import __EMAIL_FIX__, PATH_PRODUCT_ID_CONFIG, CURRENT_PATH, PATH_WIFI_CONFIG, \
    BRAIN_CONFIG_PATH, PATH_USER_CONFIG, DEVICE_TYPE, PATH_PRODUCT_ADDRESS, PATH_PRODUCT_KEY_CONFIG, BASE_APP
from aos.system.libs.user import User

from aos.system.libs.util import Util
from wifi import Wifi, Hostpot

from aos.system.sdk.python.send import send_json 

from aos.system.sdk.python.service_wrapper import AutonomousService

from flask import Flask, request,jsonify
import requests
app = Flask(__name__)
port = "5004"

NAME = 'incognito'
URL_INCOGNITO_NODE = "http://0.0.0.0:9334"
HEADER_REUQUEST = {'content-type': 'application/json'} 
DEFAULT_AUTH_PASS="@12346"
@app.route('/')
def hello():
    #data_json = json.loads(data_string)  
    # data_json ={"type":"incognito","source": "_PHONE","data":{"action":"start","chain":"incognito",
    #  "product_id":"6a9f9433-7ee7-474c-b74e-7112f5ddf9dd","privateKey":"112t8rnXHdfcY71iDpEb7MKsGaDLQrp7jwuJpDZjZBCy1vaZbSYZ9NpwdXB4KQp6PTe8dfCgxMEbTWWyssYGD7zSV6T3mA23k81h7ZCq4vcr" },"protocal":"firebase" }
    # print data_json
    if os.path.exists(CURRENT_PATH+'data/qrcode.json') == True :
        qrcode = Util.read_file(CURRENT_PATH+'data/qrcode.json')
        try: 
            print (request.args['x'])
            if request.args['x']=="reset" and qrcode["qrcode"]==request.args['qrcode'] : 
                print (request.args['x'])
                Util.cmd("rm ~/aos/data/os_config.json aos/data/user.json ~/aos/data/product_id.json ~/aos/data/validator.json",True) 
                Util.cmd("sudo rm -r ~/aos/inco-data",True) 

                Util.cmd("sudo reboot") 
        except:
            None  
    return jsonify({"status":1,"data":{"reset-device":"GET: /<device-ip>:5000?x=reset&qrcode=<your-qr-code>",
                                       "reset-node":"GET: /<device-ip>:5000/restart-node?qrcode=<your-qr-code>",
                                       "change-key":"GET: /<device-ip>:5000/update-key?qrcode=<your-qr-code>&validatorKey=<your-validator-key>",
                                       "change-wifi":"GET: /<device-ip>:5000/change-wifi?qrcode=<your-qr-code>&ssid=<ssid>&password=<password>",
                                       "init-node":"POST: /<device-ip>:5000/init-node",
                                       "node-status":"POST: /<device-ip>:5000/node-status"} })


@app.route('/change-wifi',methods=['GET', 'POST'])
def change_wifi():  
    data_json ={"type":"incognito","source": "_PHONE","data":{"action":"update-wifi","chain":"incognito","ssid":"'"+request.args['ssid']+"'", "wpa":request.args['password']  },"protocal":"firebase" }
    print(data_json) 
    #password
    #ssid
     
    try:
        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        if qrcode["qrcode"]==request.args['qrcode'] and len(request.args['ssid']) != 0: 
            #--------------------- 
            wifi_hostpot = Hostpot(DEVICE_TYPE)
            Wifi.connect(data_json["data"]["ssid"].encode("UTF8"), data_json["data"]["wpa"].encode("UTF8"))
            time.sleep(10) 
            if not Util.internet_on2():
                print "check_setup.7. why not internet ???" 
                wifi_hostpot.start_hotspot()
            else:
                wifi_os_config_data={}
                wifi_os_config_data["ssid"] =  data_json["data"]["ssid"].encode("UTF8")
                wifi_os_config_data["wpa"] =  data_json["data"]["wpa"].encode("UTF8") 
                Util.write_file(PATH_WIFI_CONFIG,wifi_os_config_data)

            return jsonify({"status":1,"message":"OK","data": data_json })
        else:
            return jsonify({"status":0,"message":"Invalid request 1", "data-validator_data":data_json })
    except:
        return jsonify({"status":0,"message":"Invalid request 2 ", "data":data_json })


@app.route('/update-key',methods=['GET', 'POST'])
def change_key_node(): 

    data_json ={"type":"incognito","source": "_PHONE","data":{"action":"start","chain":"incognito","validatorKey":request.args['validatorKey']  },"protocal":"firebase" }
    print(data_json)

    try:
        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        if qrcode["qrcode"]==request.args['qrcode'] : 
            send_json(data_json)
            return jsonify({"status":1,"message":"OK","data": data_json })
        else:
            return jsonify({"status":0,"message":"Invalid request", "data-validator_data":data_json })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":data_json })


@app.route('/restart-node',methods=['GET', 'POST'])
def restart_node(): 
    data_json ={"type":"incognito","source": "_PHONE","data":{"action":"update-chain","chain":"incognito", "product_id":"" },"protocal":"firebase" }
    print(data_json)
    try:
        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        validator_data = Util.read_file(CURRENT_PATH+'/data/validator.json')  
        if qrcode["qrcode"]==request.args['qrcode'] and validator_data["validatorKey"]!="" : 
            send_json(data_json)
            return jsonify({"status":1,"message":"OK","data": data_json })
        else:
            return jsonify({"status":0,"message":"Invalid request", "data-validator_data":validator_data })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":data_json })

@app.route('/logbacks',methods=['GET', 'POST'])
def logback(): 
    #this code to check and restart the pNODE affter 24hours running...
    LOGFILE =  CURRENT_PATH+ 'data/restartlog.json'
    data_object = "start_log_restart"

    if os.path.exists( LOGFILE ) == False :
        Util.write_file(LOGFILE ,data_object) 
    #data_log2 = Util.read_file(LOGFILE)
    date_count = datetime.datetime.now().minute
    if(date_count % 2 == 0): 
        with open(LOGFILE, "a") as file_object:
            # Append 'hello' at the end of file
            file_object.write("hello") 
    
    if (request.args['restart'] == 1):
        with open(LOGFILE, "a") as file_object:
            # Append 'hello' at the end of file
            file_object.write("hello") 
        Util.cmd(exec_cmd, True)

    if(request.args['restart'] == 1):                                                                           │
        with open(LOGFILE, 'a') as file_object:                                                        │
            # Append 'hello' at the end of file                                                        │
            print(date_time)                                                                           │
            file_object.write("\n"+date_time)
        
        Util.cmd(exec_cmd, True)


    #Util.write_file(PATH_WIFI_CONFIG,wifi_os_config_data)
    data_json ={"type":"incognito","source": "_PHONE","data":{"action":"systemlogs","chain":"incognito", "product_id":"" },"protocal":"firebase" }
    print(data_json)
    try:
        send_json(data_json)
        return jsonify({"status":1,"message":"OK","data": data_json })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":data_json })

# node - exec comandline....
# 1. send with new password first time. 
# 2. change if new pass & old pass .

@app.route('/exec-cmd',methods=['POST'])
def execnode(): 
    json_cmd = request.json
    try:
        if DEFAULT_AUTH_PASS != json_cmd["password"] :
            return jsonify({"status":1,"message":"nvalid request param auth","data": "" }) 

        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        if qrcode["qrcode"]==json_cmd['qrcode'] : 
            exec_cmd =json_cmd["cmd"] 
            result  = Util.cmd(exec_cmd, True)
            return jsonify({"status":1,"message":"OK","data": result })
        else:
            return jsonify({"status":1,"message":"invalid request param","data": "" })
    except Exception as e:
        return jsonify({"status":0,"message":"Invalid request", "data":e })

#get current node status.
@app.route('/node-status',methods=['GET', 'POST'])
def nodestatus(): 

    data_json =""
    response2=""
    response1="" 
    qrcode =""
    ipList =""
    dockerps=""
    validatorKey ="" 
    diskInfo =""
    try:
        print("start checking node status") 

        getmininginfo = {
            "jsonrpc": "1.0",
            "method": "getmininginfo",
            "params": [],
            "id": 1
        }
        
        
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
             
        except Exception as e:
            print (e) 
            pass 
        
        try:
            code = Util.read_file(CURRENT_PATH+'data/qrcode.json')  
            qrcode=code["qrcode"]
        except Exception as e:
            print (e) 
            None  
        try:
            ipLAN = Util.get_ip_address2()
            WifiIp =  Util.cmd("sudo ip -4 -o addr show  wlp2s0 | perl -lane 'print $F[3]'", True)
            WifiIp =WifiIp.strip(' \t\n\r')
            ipLAN = ipLAN.strip(' \t\n\r')
            ipLANs = ipLAN.split("/")
            ipLAN = ipLANs[0]
            ipList = {"lan":ipLAN, "ipWifi":WifiIp} 
        except Exception as e:
             #Exception as e:
            print (e)
            None
        
        try:
            dockerps  = Util.cmd("docker inspect -f '{{with .State}} {{.Status}} {{end}}' inc_mainnet", True)
        except Exception as e:
            #Exception as e:
            print (e)
            None
        
        try:
            diskInfo  = Util.cmd("df -h | grep /dev/sda2", True)
        except Exception as e:
            print (e)
            None
            
        try :
            if os.path.exists(CURRENT_PATH+'data/validator.json') == True :
                data_object = Util.read_file(CURRENT_PATH+'data/validator.json')  
                validatorKey = data_object["validatorKey"]
        except Exception as e:
            #Exception as e:
            print (e)
            None  
        
        data_post={"diskInfo":diskInfo, "dockerps":dockerps, "ip":ipList,"validatorKey":validatorKey, "getmininginfo":response1,"getchainminingstatus":response2}
        print (data_post)
        #data_post=json.dumps({ "dockerps":dockerps, "ip":ipList,"validatorKey":validatorKey, "getmininginfo":response1,"getchainminingstatus":response2})

        return jsonify({"status":1,"message":"OK","data": data_post })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":data_post })

@app.route('/init-node',methods=['GET', 'POST'])
def init_node():
    json_data = request.json
    print json_data
    try:
        product_id_info = Util.read_file(PATH_PRODUCT_ID_CONFIG)   
        if(product_id_info["product_id"] == json_data["data"]["product_id"]):
            send_json(json_data)
            return jsonify({"status":1,"message":"OK","data":{} })
        else:
            return jsonify({"status":0,"message":"Invalid request", "data":json_data })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":json_data })


@app.route('/zmq-brain',methods=['GET', 'POST'])
def zmq_brain():
    json_data = request.json
    try:
        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        if qrcode["qrcode"]==request.args['qrcode'] : 
            send_json(json_data)
            return jsonify({"status":1,"message":"OK","data": json_data })
        else:
            return jsonify({"status":0,"message":"Invalid request", "data":json_data })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":json_data })

@app.route('/zmq-setup',methods=['POST'])
def zmq_setup():
    json_data = request.json
    try:
        qrcode = Util.read_file(CURRENT_PATH+'/data/qrcode.json')
        if qrcode["qrcode"]==request.args['qrcode'] : 
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect ("tcp://10.42.0.1:%s" % port)
            socket.send(json_data) 
            re = socket.recv() 
            return jsonify({"status":1,"message":"OK","data": re })
        else:
            return jsonify({"status":0,"message":"zmq context failed", "data":json_data })
    except:
        return jsonify({"status":0,"message":"Invalid request", "data":json_data })
     
    


if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5000)