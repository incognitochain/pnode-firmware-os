#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import os

import thread

import time

import sys
import zmq

from Commands import COMMANDS
from aos.ability.install_ability_device.install_app import InstallUpdateAbility
from messages import MESSAGE
from help import Help
from run_update import RunUpdate
from aos.system.libs.ability import Ability
from aos.system.libs.device import Device

from aos.system.configs.channel import __EMAIL_FIX__, PATH_PRODUCT_ID_CONFIG, PATH_WIFI_CONFIG, \
    BRAIN_CONFIG_PATH, PATH_USER_CONFIG, DEVICE_TYPE, PATH_PRODUCT_ADDRESS, PATH_PRODUCT_KEY_CONFIG, BASE_APP, \
    LOCAL_HOTSPOT
from aos.system.libs.user import User

from aos.system.libs.util import Util
from wifi import Wifi, Hostpot

from aos.system.sdk.python.send import send_json

IP_HOST_SPOT = '10.42.0.1'
IP_HOSTSPOT_NET='10.42.0.1/24'

class Setup(object):
    def __init__(self):
        print "init hotspot class ..."
        self.wifi_hostpot = Hostpot(DEVICE_TYPE)

        print "init zmq ..."
        self.context = None
        self.results_receiver = None

        # for check wifi loop:
        self.check_loop_wifi_is_running = False
        self.hotspot_flag = False
        self.wifi_connecting = False

        self.ssid = None
        self.wpa = None

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
    def check_setup(self):
        # Check os_config:
        if not os.path.isfile(PATH_WIFI_CONFIG):
            print "check_setup.1. path " + PATH_WIFI_CONFIG + " config not exits"
            self.start_hotspot()

        else:
            # case for already setup, should be check hotspot is turn on -> off -> check internet:
            # this case just check internet address. via bot LAN & WIFI 
            ipLAN = Util.get_ip_address2() 
            staipWifiCardtus = Util.cmd("sudo ip -4 -o addr show  wlp2s0 | perl -lane 'print $F[3]'", True)
            staipWifiCardtus =staipWifiCardtus.strip(' \t\n\r')
            ipLAN = ipLAN.strip(' \t\n\r')
            print "check_setup.2. check ipLAN => " + ipLAN
            print "check_setup.2. check staipWifiCardtus => " + staipWifiCardtus
            if ipLAN == IP_HOST_SPOT or staipWifiCardtus == IP_HOSTSPOT_NET: 
                print "check_setup.3. wifi_hostpot.stop_hotspot => sleep10 " 
                self.wifi_hostpot.stop_hotspot()
                time.sleep(10) 
                # try connect wifi if exits path wifi... 

            #check internet:
            if not Util.internet_on2():
                print "check_setup.4. Wifi.reconnect => " 
                if not Wifi.reconnect():
                    print "check_setup.5. Wifi.reconnect.failed=>start_hotspot =>" 
                else:
                    print "check_setup.6. s2b_start_check_internet_connection =>" 
                    Help.s2b_start_check_internet_connection()
                #neu van khong the reconnect -- hotpost
                time.sleep(5) 
                if not Util.internet_on2():
                    print "check_setup.7. why not internet ???" 
                    self.start_hotspot()

            else:
                print "check_setup.8. s2b_start_check_internet_connection" 
                Help.s2b_start_check_internet_connection()

    def start_hotspot(self, data=None):
        self.hotspot_flag = True
        print "start_hotspot.1. status is false, sleep 5s for creating hotspot ..."
        self.wifi_hostpot.start_hotspot()
        time.sleep(5)
        ipLAN = Util.get_ip_address2() 
        staipWifiCardtus = Util.cmd("sudo ip -4 -o addr show  wlp2s0 | perl -lane 'print $F[3]'", True)
        staipWifiCardtus =staipWifiCardtus.strip(' \t\n\r')
        ipLAN = ipLAN.strip(' \t\n\r')
        print "start_hotspot.2. check ipLAN => " + ipLAN
        print "start_hotspot.2. check staipWifiCardtus => " + staipWifiCardtus

        if ipLAN == IP_HOST_SPOT or staipWifiCardtus == IP_HOSTSPOT_NET:
            print "start_hotspot.3. zmq listen data from mobile setup"
            thread.start_new_thread(self.start_listen_data_from_phone, ())
        else:
            print "start_hotspot.4. Not create hotspot, create again ..."
            self.start_hotspot()

    def start_listen_data_from_phone(self):
        self.stop_listen_hotspot()
        time.sleep(2)

        print("start_listen_data_from_phone.1. Starting zmq Context to get wifi data... ")
        self.context = zmq.Context()
        self.results_receiver = self.context.socket(zmq.REP)
        self.results_receiver.bind(LOCAL_HOTSPOT)
        print("start_listen_data_from_phone.2. Listening data info from phone...")

        while True:
            try:
                data_string = self.results_receiver.recv()
                print "Receive data!", data_string

                key_array = ['action', 'verify_code', 'time_zone', 'user_id', 'wpa', 'ssid', 'token']                

                result = Util.check_invalid_data(data_string, key_array)
                if not result.status:
                    data_send = '{"action": "check_send", "value": "0", "error_message": "' + result.message + '"}'
                    self.results_receiver.send(data_send)
                else:                    
                    # hardcode:
                    data_info = result.message
                    data_info["address_long"] = -95.712891
                    data_info["address_lat"] = 37.090240
                    data_info['product_name'] = "The Miner"
                    data_info['platform'] = "MINER"
                    data_info["address"] = "US"

                    if data_info['action'] == 'send_wifi_info' or data_info['action'] == 'hotpost_connected':
                        data_send = '{"action": "check_send", "value": "1"}'
                        self.results_receiver.send(data_send)

                        if data_info['action'] == 'send_wifi_info':
                            print "sleep for send to phone ..."
                            time.sleep(3)
                            self.setup_from_phone_data(data_info)
                            break
            except Exception as e:
                print "error receive package!:", sys.exc_info(), str(e)

        self.stop_listen_hotspot()

    def setup_from_phone_data(self, wifi_data):

        if wifi_data:
            try:
                print "wifi connecting ..."
                self.ssid = wifi_data['ssid']
                self.wpa = wifi_data['wpa']
                if self.wifi_hostpot.stop_hotspot_and_connect_wifi(self.ssid, self.wpa):
                    print "wifi connected"
                    print "1: save address:"
                    address_data = {wifi_data['address'], wifi_data['address_lat'], wifi_data['address_long'], wifi_data['time_zone']}
                    self.save_desk_address(address_data)

                    print "2: check_in:"
                    response = self.get_qr_image({"token": wifi_data['token'], 'user_id': wifi_data['user_id']})
                    print "status get_qr_image =>", response['status']
                    if response['status'] == 1:
                        print "3: add_product"
                        if self.add_product(wifi_data):
                            Help.s2b_start_check_internet_connection()
                            return True
                else:
                    print "wifi not connected!!!"

            except Exception as e:
                print "data error => " + str(e)

            # self.start_hotspot()
            Setup.restart_brain()

    def stop_listen_hotspot(self):
        print ("stopping listen zmq ...")
        try:
            if self.context:
                self.context.close()
            if self.results_receiver:
                self.results_receiver.term()
        except:
            sys.exc_info()
            pass

    # -----------------------------------------BEGIN ACTION FUNCTION ------------------------------------
    def check_wifi(self, data=None):
        return Setup.return_data()

    def wifi_current_name(self, data=None):
        return Setup.return_data(data=Wifi.get_current_wifi())

    def display_image(self, data=None):
        from display_image import DisplayImage
        return Setup.return_data(data=DisplayImage.display_image(data['data'], data["type"]))

    def user_info(self, data):
        if "force_refresh_data" in data and Util.smart_bool(data["force_refresh_data"]) == True:
            return_data = Setup.return_data_from_api(User.refresh_user())
            if return_data['status'] == 1:
                user_old_data = Util.get_user_data()
                if user_old_data:
                    user_new_data = return_data['data']
                    user_old_data.update(user_new_data)
                    Util.write_file(PATH_USER_CONFIG, user_old_data)
                    return Setup.return_data(data=user_new_data)

        return Setup.return_data(data=Util.get_user_data())

    def restart_os(self, data=None):
        Util.cmd("sudo reboot")

    def get_qr_image(self, data=None):

        # try:
        # Neu chua check_out thi ko duoc gen qr_image code:
        os_config = Util.get_product_config()
        product_id_info = Util.read_file(PATH_PRODUCT_ID_CONFIG)
        if os_config:
            if product_id_info and 'barcode_url' in product_id_info and data['user_id'] == product_id_info['is_used']:
                thread.start_new_thread(Setup.restart_firebase, ())
                return Setup.return_data(data=product_id_info)

        # Neu da gen 1 lan thi ko gen nua:
        if product_id_info and data['user_id'] == product_id_info['is_used']:
            if 'barcode_url' in product_id_info:
                thread.start_new_thread(Setup.restart_firebase, ())
                return Setup.return_data(data=product_id_info)
        try:
            response = Device.get_qr_image()
        except Exception as e:
            print str(e)
            response = Device.get_qr_image()

        if response and 'status' in response and response['status'] == 1:
            print "save product_id data json->" + PATH_PRODUCT_ID_CONFIG
            Util.write_file(PATH_PRODUCT_ID_CONFIG, response['data'])

            thread.start_new_thread(Setup.gen_update_firebase_id, (response['data']['product_id'], "", data['token']))

        return Setup.return_data_from_api(response)

    def check_product(self, data=None):
        product_id = Util.get_product_id()
        if product_id:
            data = Device.check_product(product_id, DEVICE_TYPE)

            if data and data['status'] == 1:
                data = data['data']
                os_config_data = {}
                os_config_data.update(data)
                os_config_data['user_hash'] = data['user']['user_hash']
                os_config_data['email'] = data['user']['email']

                Util.write_file(PATH_USER_CONFIG, data['user'])

                del os_config_data['user']
                Util.write_file(PATH_WIFI_CONFIG, os_config_data)

                product_id_config = Util.read_file(PATH_PRODUCT_ID_CONFIG)
                product_id_config['is_used'] = data['user']['id']
                Util.write_file(PATH_PRODUCT_ID_CONFIG, product_id_config)

                if not os.path.isfile(PATH_PRODUCT_KEY_CONFIG):
                    Util.write_file(PATH_PRODUCT_KEY_CONFIG, {"product_key": product_id})

                thread.start_new_thread(Setup.gen_update_firebase_id, (product_id, os_config_data['user_hash'], os_config_data['token']))

            return data

        return Setup.return_data(0, MESSAGE.PRODUCT_ID_NOT_FOUND, 0)

    def add_product(self, data):

        print "add product with data: ", data

        data['product_id'] = Util.get_product_id()

        device = Device(**data)

        response = device.add_product(data['token'])

        print "add product with response: ", response

        if response and isinstance(response, dict) and 'status' in response and response['status'] == 1:

            # luu lai data:
            user_data = response['data']['user']

            product_ids = response['data']['user']['products']

            if len(product_ids):
                for product_id in product_ids:
                    if product_id['is_checkin'] == 1:

                        user_data['product'] = product_id

                        product_id_config = Util.read_file(PATH_PRODUCT_ID_CONFIG)
                        product_id_config['is_used'] = user_data['user_id'] if 'user_id' in user_data else user_data['id']
                        Util.write_file(PATH_PRODUCT_ID_CONFIG, product_id_config)

                        user_data['access_token'] = data['token']
                        user_data['token'] = data['token']

                        Util.write_file(PATH_USER_CONFIG, user_data)
                        if not os.path.isfile(PATH_PRODUCT_KEY_CONFIG):
                            Util.write_file(PATH_PRODUCT_KEY_CONFIG, {"product_key": product_id['product_id']})

                        del user_data['product']

                        os_config_data = {}
                        for k, v in user_data.items():
                            os_config_data[k] = v

                        for k, v in product_id.items():
                            os_config_data[k] = v

                        Util.write_file(PATH_WIFI_CONFIG, os_config_data)

                        Setup.broadcast("user_check_in")

                        response['data']['user'] = user_data

                        return True
        return False

    def save_desk_address(self, data):
        # try:
        array_key = ("address", "address_lat", "address_long", "time_zone")
        if not isinstance(data, dict) or (isinstance(data, dict) and not all(k in data for k in array_key)):
            return Setup.return_data(0, MESSAGE.ADDRESS_ERROR)
        else:
            if data['address_long'] and data['address_lat'] and data["address"] and data["time_zone"]:
                config_address = Util.get_product_address_config()
                need_update = False
                if config_address and all(k in config_address for k in array_key):
                    if config_address['address_lat'] != data["address_lat"] or config_address['address_long'] != \
                            data["address_long"] or data["time_zone"] != config_address['time_zone']:
                        need_update = True
                else:
                    need_update = True

                if need_update:
                    # update product_address if ready check-in:
                    user = User.get_user_info()
                    if user:
                        response = Setup.return_data_from_api(Device.update_address(address_data=data))
                        if response['status'] == 1:
                            Util.write_file(PATH_PRODUCT_ADDRESS, data)
                            Util.set_date_time(data['time_zone'])
                        return Setup.return_data_from_api(response)
                    else:
                        Util.write_file(PATH_PRODUCT_ADDRESS, data)
                        Util.set_date_time(data['time_zone'])

                return Setup.return_data(status=1)

        return Setup.return_data(0, MESSAGE.ADDRESS_ERROR)

        # except Exception as e:
        #     print str(e)
        #     return Setup.return_data(0, str(e))

    def user_check_out(self, data=None):
        # we should send first for sign out immediately
        package = {"type": "phone_control", "source": self.source,
                   "data": {"action": "user_check_out", "from": "product_control",
                            "data": {"message": 0, "status": 1, "data": {}}}}
        send_json(package)
        time.sleep(3)
        try:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()
                thread.start_new_thread(Device.check_out, (token, product_id))
        except Exception as e:
            print str(e)

        # if os.path.isfile(PATH_PRODUCT_ID_CONFIG):
        #     os.unlink(PATH_PRODUCT_ID_CONFIG)
        #     print "removed " + PATH_PRODUCT_ID_CONFIG

        Setup.remove_all_config_check_out()

        thread.start_new_thread(Setup.stop_firebase, ())
        thread.start_new_thread(Setup.broadcast, (COMMANDS.CHECK_OUT,))
        self.check_setup()
        return Setup.return_data(status=1)

    def ready_in_use(self, data=None):

        # 1. check save_address:
        save_desk_address = Setup.get_current_address()

        # 2. check wifi has internet:
        wifi_has_internet = Util.check_internet_connection()

        # 3. Check xem da check_in tren board chua?
        user_check_in = Util.get_user_data()
        if wifi_has_internet:
            if user_check_in:
                product_id_info = Util.read_file(PATH_PRODUCT_ID_CONFIG)
                # kiem tra da co is_used chua? neu chua co thi bat check_in lai:
                if product_id_info:
                    if 'is_used' not in product_id_info:
                        os.unlink(PATH_PRODUCT_ID_CONFIG)
                        if not Setup.__auto_login__(user_check_in):
                            user_check_in = None
                    else:
                        # kiem tra xem product_id nay tren dababase co check_out chua?
                        product_data = Device.get_info()
                        if not (product_data and product_data['status'] == 1 and product_data['data']['is_checkin'] == 1):
                            Setup.remove_all_config_check_out()
                            user_check_in = {}
                else:
                    if not Setup.__auto_login__(user_check_in):
                        user_check_in = None

        if user_check_in is None:
            user_check_in = {}

        Help.s2b_start_check_internet_connection()

        return Setup.return_data(data={"wifi_has_internet": wifi_has_internet, "user_check_in": user_check_in,
                                       "save_desk_address": save_desk_address})

    @staticmethod
    def __auto_login__(user_data):
        try:
            __check_in__ = "product/auto-checkin"

            if 'access_token' in user_data:
                status, _, _ = Setup.get_qr_image()
                if status == 0:
                    return False

                product_id = Util.get_product_id()
                product_key = Util.get_product_key()
                data_address = Util.get_product_address_config()
                data = {"product_id": product_id, "product_key": product_key}
                if product_id:
                    if data_address:
                        for key, value in data_address.iteritems():
                            if isinstance(data_address[key], (str, unicode)):
                                data_address[key] = data_address[key].encode('utf-8', 'replace').strip()
                        data.update(data_address)

                    from aos.system.libs.request_api import RequestApi
                    response = RequestApi(token=user_data['access_token']).get_json(__check_in__, "POST", data=data)

                    # if product is used by other user:
                    if response and isinstance(response, dict) and response.get('error_code', "") == 'product_used':
                        return False

                    response = Setup.return_data_from_api(response)

                    if response['status'] == 1:
                        # luu lai data:
                        user_data = response['data']['user']

                        product_ids = response['data']['user']['products']

                        if len(product_ids):
                            for product_id in product_ids:
                                if product_id['is_checkin'] == 1:

                                    user_data['product'] = product_id

                                    product_id_config = Util.read_file(PATH_PRODUCT_ID_CONFIG)
                                    product_id_config['is_used'] = user_data['id'] if "id" in user_data else user_data['user_id']
                                    Util.write_file(PATH_PRODUCT_ID_CONFIG, product_id_config)

                                    Util.write_file(PATH_USER_CONFIG, user_data)
                                    if not os.path.isfile(PATH_PRODUCT_KEY_CONFIG):
                                        Util.write_file(PATH_PRODUCT_KEY_CONFIG, {"product_key": product_id['product_id']})

                                    del user_data['product']

                                    os_config_data = {}
                                    for k, v in user_data.items():
                                        os_config_data[k] = v

                                    for k, v in product_id.items():
                                        os_config_data[k] = v

                                    Util.write_file(PATH_WIFI_CONFIG, os_config_data)

                                    thread.start_new_thread(Setup.gen_update_firebase_id,
                                                            (os_config_data["product_id"], os_config_data['user_hash'], os_config_data['token']))

                                    Setup.broadcast("user_check_in")

                                    response['data']['user'] = user_data

                                    return True
        except Exception as e:
            print str(e)

        return False

    def user_add_ability(self, data):
        response = Ability.add(data)
        return Setup.return_data_from_api(response)

    def user_update_ability(self, data):
        ability_data = {
            'is_local': data['app']['is_local'],
            'is_service': data['app']['is_service'],
            'is_core_app': data['app']['is_core_app'],
            'boot': data['app']['is_service'] == 1,
            'app': data['version'][0]['app_name'],
            'application_file': data['version'][0]['application_file'],
            'version': data['version'][0]['version'],
            'link': data['version'][0]['source_codeURL'],
            'md5_hash': data['version'][0]['md5_hash'],
            'action': "add"
        }

        user_oauth = data['user_oauth'] if 'user_oauth' in data else None

        if not ability_data['is_core_app'] and ability_data['is_local'] == 1:

            new_version = Util.convert_version(ability_data['version'])
            app_base_dir = BASE_APP + ability_data['app']
            app_config = Util.read_file(app_base_dir + "/config.json")
            current_version = -1
            if app_config:
                current_version = Util.convert_version(app_config['version'])
            print "app_config: ", app_config, "current_version: ", current_version, " new_version: ", new_version
            if current_version < new_version:

                Help.s2b_stop_check_update()

                print "install local app ...."
                ability_data['action'] = "add"
                ability_data['silent'] = True

                if ability_data['is_service']:
                    Help.s2b_updating(ability_data['app'])
                    Help.s2b_kill_app(ability_data['app'])

                if InstallUpdateAbility(ability_data, "").add():
                    status = 1
                    message = MESSAGE.ABILITY_UPDATE_SUCCESS % ability_data['app']
                else:
                    status = 0
                    message = MESSAGE.ABILITY_UPDATE_FAIL % ability_data['app']

                Help.s2b_remove_updating(ability_data['app'])
                Help.s2b_result_install(status, ability_data['app'], message, ability_data['action'])

                if ability_data['boot']:
                    time.sleep(2)
                    Help.s2b_list_tasks(ability_data['app'], {"user_oauth": user_oauth})

                Help.s2b_continue_check_update()

                return Setup.return_data(status, message, status)

            if ability_data['boot']:
                Help.s2b_list_tasks(ability_data['app'], {"user_oauth": user_oauth})

        return Setup.return_data(1, "", True)

    def user_remove_ability(self, data):
        if 'id' not in data:
            return Setup.return_data(0, MESSAGE.PARAM_REQUIRED % "id", None)
        data = Ability.remove(data)
        return Setup.return_data_from_api(data)

    @staticmethod
    def remove_all_config_check_out():

        if os.path.isfile(PATH_WIFI_CONFIG):
            os.unlink(PATH_WIFI_CONFIG)
            print "removed os_config"

        # if os.path.isfile(BRAIN_CONFIG_PATH):
        #     pr_device_data = Util.read_file(BRAIN_CONFIG_PATH)
        #     if pr_device_data and 'firebase' in pr_device_data:
        #         pr_device_data['firebase']['uid'] = ''
        #         Util.write_file(BRAIN_CONFIG_PATH, pr_device_data)
        #         print "update pr_device.json"

        if os.path.isfile(PATH_USER_CONFIG):
            os.unlink(PATH_USER_CONFIG)
            print "removed user_config"

    def download_ability(self, data=None):
        # call api get list ability:
        ability_list = Ability.list()
        # ability_list = [{"is_local": 1, "version": "1.0", "link": "https://s3.amazonaws.com/robotbase-cloud/static/upload_apps/googleapp_1.0_608_95.zip", "is_service": 1, "md5_hash": "6d7fbf2e9f3aeb76b54161e943c48e5d", "action": "add", "is_core_app": 0, "app": "googleapp", "boot": True, "application_file": "main.py"}, {"is_local": 0, "version": "1.0", "link": "https://s3.amazonaws.com/robotbase-cloud/static/upload_apps/facebook_1.0_608_96.zip", "is_service": 0, "md5_hash": "18e37a01dfed710e75d9454b5ae55f72", "action": "add", "is_core_app": 0, "app": "facebook", "boot": False, "application_file": "main.py"}]
        if ability_list:
            json_data = {"source": "", "protocol": "", "type": "install_ability_device"}
            for ab in ability_list:
                if ab['is_local'] == 1 and ab['is_core_app'] == 0:
                    print "install local app ...."

                    ab['action'] = "add"
                    ab['silent'] = True

                    json_data['data'] = ab
                    print "send sensor instal app to brain ..."
                    send_json(json_data)

                    time.sleep(3)

        return Setup.return_data(status=1)

    def check_version(self, data=None):
        return Setup.return_data(1, "", Help.get_os_version())

    def ip_address(self, data=None):
        return Setup.return_data(1, "", str(Util.get_ip_address2()))

    def platform(self, data=None):
        return Setup.return_data(1, "", DEVICE_TYPE)

    def update_firmware(self, data=None):
        RunUpdate.update_firmware(self.source)
        return Setup.return_data()

    def factory_reset(self, data=None):
        package = {"type": "phone_control", "source": self.source,
                   "data": {"action": "factory_reset", "from": "product_control",
                            "data": {"message": "", "status": 1, "data": {}}}}
        send_json(package)
        time.sleep(3)
        Util.factory_reset()

    def wifi_update(self, data=None):
        package = {"type": "phone_control", "source": self.source,
                   "data": {"action": "wifi_update", "from": "product_control",
                            "data": {"message": "", "status": 1, "data": {}}}}
        send_json(package)
        time.sleep(3)
        Util.wifi_update()

    # mine action:
    def mining(self, data=None):
        print "fw data for mine apps ..."        
        json_data = {"source": "", "protocol": "", "type": "restart_firebase", "data": data}
        send_json(json_data)    

    # -----------------------------------------END ACTION FUNCTION ------------------------------------

    @staticmethod
    def restart_brain():
        print "call restart brain again new config"
        json_data = {"source": "", "protocol": "", "type": "restart_brain", "data": {}}
        send_json(json_data)

    @staticmethod
    def restart_firebase():
        print "call restart brain again new config"
        json_data = {"source": "", "protocol": "", "type": "restart_firebase", "data": {}}
        send_json(json_data)

    @staticmethod
    def stop_firebase():
        time.sleep(3)
        print "call stop firebase"
        json_data = {"source": "", "protocol": "", "type": "restart_firebase", "data": {}}
        send_json(json_data)

    @staticmethod
    def broadcast(sensor):
        print "broadcasting sensor %s ..." % sensor
        json_data = {"source": "", "protocol": "", "type": sensor, "data": {}}
        send_json(json_data)

    @staticmethod
    def gen_update_firebase_id(product_id, user_hash, token):
        endpoint = '/get-firebase-id'
        from aos.system.libs.request_api import RequestApi
        response = RequestApi(token).get_json(endpoint, query_parameters={"product_id": product_id})
        print "gen_update_firebase_id=>", response
        if response and 'data' in response and response['data']:
            localId = response['data']
            Util.update_pr_device_id(product_id, localId)

            Setup.restart_firebase()
            print "update firebase success!"
        else:
            print "update firebase fail"



    @staticmethod
    def gen_update_firebase_id1(product_id, user_hash):

        # hardcode pass:
        fb_pass = "at9XafdcJ7TVHzGa"

        # create firebase uid:
        print "gen firebase_uid:"
        from aos.system.libs.firebase import Firebase
        firebase = Firebase()
        if firebase.get_firebase_uid(product_id + __EMAIL_FIX__, fb_pass):
            print "update product_id cho pr_device config"
            Util.update_pr_device_id(product_id, firebase.localId)

            Setup.restart_firebase()

    @staticmethod
    def get_current_address():
        save_desk_address = Util.get_product_address_config()
        if save_desk_address is None:
            # Setup.remove_all_config_check_out()
            save_desk_address = {}
        else:
            if 'address_long' not in save_desk_address or 'address_lat' not in save_desk_address or "address" not in save_desk_address or "time_zone" not in save_desk_address:
                save_desk_address = {}
            elif not save_desk_address['address_long'] and save_desk_address['address_lat'] and \
                    save_desk_address["address"] and save_desk_address["time_zone"]:
                save_desk_address = {}

        return save_desk_address            
