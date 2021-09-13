
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

wifi_data = {

        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGhlbWluZXIuY29tIiwiZXhwIjoxNTY0MjE0NjM1LCJpZCI6MTQwMDg0fQ.jMN13oHoJu7W9jNGcI4QVoXxOnU9sn-qG4w-hzTZ9uk",
        "address": "ho chi minh viet nam",
        "address_lat": 0.325235345,
        "address_long": 0.2423432,
        "birth": "2016-12-31",
        "city": "xxxx",
        "code": "4cd6e1",
        "country": "xxxx",
        "created_at": "Thu, 27 Jun 2019 08:03:55 GMT",
        "credit": 0,        
        "email": "test@theminer.com",
        "fullname": "Phuong",
        "gender": "Male",
        "id": 1375,
        "user_id": 1375,
        "last_update_task": "Thu, 27 Jun 2019 08:03:55 GMT",
        "phone": "34554534345",
        "products": [],
        "ref_user_id": 140084,
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGhlbWluZXIuY29tIiwiZXhwIjoxODc2OTgyNjM1LCJpZCI6MTQwMDg0LCJzYWx0IjoiYzNhMjAyM2YtZDUyNS00NWEwLTk0YTMtZTVhYTc4YzZhMDM2In0.6KCjaBrbzo9IKz5GmpFxJPKhOzkpmSwS15Kb4QWhRaw",
        "role": [],
        "state_region": "dsfdfsdsf",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGhlbWluZXIuY29tIiwiZXhwIjoxNTY0MjE0NjM1LCJpZCI6MTQwMDg0fQ.jMN13oHoJu7W9jNGcI4QVoXxOnU9sn-qG4w-hzTZ9uk",
        "user_avatar": "",
        "user_code": "xxxx",
        "user_hash": "at9XafdcJ7TVHzGa",        
        "ssid": "Autonomous",
        "wpa": "@11235813", 
        "code": "7b9f13", 
        "verify_code": "phuongtestminer",
        "platform": "MINER",
        "product_name": "MINER",   
}

def return_data(status=1, message="", data=None):
        status = 1 if status else 0
        data = 1 if status == 1 and data is None else data
        return {"status": status, "message": message, "data": data}


def return_data_from_api(response):
    if response:
        if isinstance(response, dict) and "status" in response:
            if "message" not in response:
                response['message'] = ""
            if "data" not in response:
                response['data'] = None
            return response
        return return_data(0, MESSAGE.REQUEST_API_ERROR, None)
    return return_data(0, MESSAGE.PRODUCT_ID_NOT_FOUND, None)
    
def get_qr_image(data=None):

    # try:
    # Neu chua check_out thi ko duoc gen qr_image code:
    os_config = Util.get_product_config()
    product_id_info = Util.read_file(PATH_PRODUCT_ID_CONFIG)
    if os_config:
        if product_id_info and 'barcode_url' in product_id_info and data['user_id'] == product_id_info['is_used']:
            thread.start_new_thread(restart_firebase, ()) 
            return return_data(data=product_id_info)               

    # Neu da gen 1 lan thi ko gen nua:
    if product_id_info and data['user_id'] == product_id_info['is_used']:
        if 'barcode_url' in product_id_info:
            thread.start_new_thread(restart_firebase, ())                
    try:
        response = Device.get_qr_image()
    except Exception as e:
        print str(e)
        response = Device.get_qr_image()

    if response and 'status' in response and response['status'] == 1:
        print "save product_id data json->" + PATH_PRODUCT_ID_CONFIG
        Util.write_file(PATH_PRODUCT_ID_CONFIG, response['data'])

        thread.start_new_thread(gen_update_firebase_id, (response['data']['product_id'], "", data['token']))
    return return_data_from_api(response)

def gen_update_firebase_id(product_id, user_hash, token):
    endpoint = '/get-firebase-id'
    from aos.system.libs.request_api import RequestApi
    response = RequestApi(token).get_json(endpoint, query_parameters={"product_id": product_id})
    print "gen_update_firebase_id=>", response
    if response and 'data' in response and response['data']:
        localId = response['data']
        Util.update_pr_device_id(product_id, localId)

        restart_firebase()
        print "update firebase success!"
    else:
        print "update firebase fail"    

def restart_brain():
    print "call restart brain again new config"
    json_data = {"source": "", "protocol": "", "type": "restart_brain", "data": {}}
    send_json(json_data)

def restart_firebase():
    print "call restart brain again new config"
    json_data = {"source": "", "protocol": "", "type": "restart_firebase", "data": {}}
    send_json(json_data)

def add_product(data):

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

                    response['data']['user'] = user_data

                    return True    

if wifi_data:
    try:
        print "wifi connecting ..."
        ssid = wifi_data['ssid']
        wpa = wifi_data['wpa']
        
        print "wifi connected"
        print "1: save address:"
        
        print "2: check_in:"
        response = get_qr_image({"token": wifi_data['token'], 'user_id': wifi_data['user_id']})
        print "status get_qr_image =>", response['status']
        if response['status'] == 1:
            print "3: add_product"
            if add_product(wifi_data):
                Help.s2b_start_check_internet_connection()                        

    except Exception as e:
        print "data error => " + str(e)

    # self.start_hotspot()
    restart_brain()
