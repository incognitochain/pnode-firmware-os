
import os

import thread

import time

import sys
import zmq
import json
 
from aos.ability.install_ability_device.install_app import InstallUpdateAbility
from messages import MESSAGE
from help import Help
from run_update import RunUpdate
from aos.system.libs.ability import Ability
from aos.system.libs.device import Device

from aos.system.configs.channel import __EMAIL_FIX__, PATH_PRODUCT_ID_CONFIG, PATH_WIFI_CONFIG, \
    BRAIN_CONFIG_PATH, PATH_USER_CONFIG, DEVICE_TYPE, PATH_PRODUCT_ADDRESS, PATH_PRODUCT_KEY_CONFIG, BASE_APP
from aos.system.libs.user import User

from aos.system.libs.util import Util
from wifi import Wifi, Hostpot

from aos.system.sdk.python.send import send_json 

from aos.system.sdk.python.service_wrapper import AutonomousService

# =========================================
# init devices ->
# host-post-create 
#     => generator a private KEY KEY1.
#                     mobile connect to device hotspot recevice the KEY1.

# mobile have KEY1 => encryt KEY1-> KEY2 => encryt PRivateKey( by KEY2) -> send to device 

# device -> descript KEY1->KEY2 -> descript PRivateKey (via KEY2) => launch....


IP_HOST_SPOT = '10.42.0.1'
LOCAL_HOTSPOT_INCOGNITO_SERVICE='5055'

class HostService(object):
    def __init__(self):
        print "init zmq ..."
        self.context = None
        self.results_receiver = None

        # for check wifi loop:
        self.check_loop_wifi_is_running = False
        self.hotspot_flag = False
        self.wifi_connecting = False  
        self.source = ""

    # -------------------------------help---------------------------------------------------------------
    @staticmethod
    def return_data(status=1, message="", data=None):
        status = 1 if status else 0
        data = 1 if status == 1 and data is None else data
        return {"status": status, "message": message, "data": data}

    @staticmethod
    def return_unknown_error():
        return Setup.return_data(0, MESSAGE.UNKNOWN_ERROR, 0)

    @staticmethod
    def return_data_from_api(response):
        if response:
            if isinstance(response, dict) and "status" in response:
                if "message" not in response:
                    response['message'] = ""
                if "data" not in response:
                    response['data'] = None
                return response
            return Setup.return_data(0, MESSAGE.REQUEST_API_ERROR, None)
        return Setup.return_data(0, MESSAGE.PRODUCT_ID_NOT_FOUND, None)

    # -----------------------------------------BEGIN CHECK SETUP ---------------------------------------
   
    def start_incognito_service(self, data=None):
            
        ip = Util.get_ip_address2()
        print "check ip => " + ip
        if ip.strip(' \t\n\r') == IP_HOST_SPOT: 
            print "in hotspot mode"
        else:
            print "zmq listen ..." 
            thread.start_new_thread(self.start_listen_data_from_phone, ()) 

    def start_listen_data_from_phone(self):
        # self.stop_listen_hotspot()
        # time.sleep(2)
        ip = Util.get_ip_address2()
        print("Starting zmq Context host-service... " )
        print LOCAL_HOTSPOT_INCOGNITO_SERVICE
        self.context = zmq.Context()
        self.results_receiver = self.context.socket(zmq.REP)
        self.results_receiver.bind("tcp://*:" + LOCAL_HOTSPOT_INCOGNITO_SERVICE)
        print("Listening data info from phone...")
        while True:
            try:
                data_string = self.results_receiver.recv()
                print "Receive data!", data_string 
                key_array = ['type']
                result = Util.check_invalid_data(data_string, key_array) 
                print("result ... ", result.status)
                if not result.status:
                    try:
                        data_send = '{"action": "check_send", "value": "0", "error_message": "' + result.message + '"}'
                        self.results_receiver.send(data_send)
                    except Exception as e:
                        print e
                else:
                    # fwd data to brain.
                    # brain fwd to ability chain... 
                    try:
                        data_json = json.loads(data_string)  
                        print data_json
                        send_json(data_json)
                    except Exception as e:
                        print e
                    # hardcode:
                    data_send = '{"action": "check_send", "value": "1"}'
                    self.results_receiver.send(data_send) 
                    

            except Exception as e:
                print "error receive package!:", sys.exc_info(), str(e) 
        self.stop_listen_service()  

    def stop_listen_service(self):
        print ("stopping listen zmq ...")
        try:
            if self.context:
                self.context.close()
            if self.results_receiver:
                self.results_receiver.term()
        except:
            sys.exc_info()
            pass  

if __name__ == '__main__':
    host = HostService()
    ip = Util.get_ip_address2()
    print "check ip => " + ip
    host.start_listen_data_from_phone()