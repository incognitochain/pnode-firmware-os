#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#


from aos.system.configs.channel import DEVICE_TYPE
from aos.system.libs.util import Util

from aos.system.libs.wifi import WifiHostpot, RasberryWifi
from aos.system.libs.util import Util  
from aos.system.configs.channel import __EMAIL_FIX__, PATH_PRODUCT_ID_CONFIG, CURRENT_PATH, PATH_WIFI_CONFIG, \
    BRAIN_CONFIG_PATH, PATH_USER_CONFIG, DEVICE_TYPE, PATH_PRODUCT_ADDRESS, PATH_PRODUCT_KEY_CONFIG, BASE_APP

import netifaces
import subprocess
import time 

class Hostpot:
    _ssid = "Autonomous"

    # init
    def __init__(self, ssid=None):
        if ssid is not None:
            self._ssid = ssid + "-" + Util.gen_id()

    def stop_hotspot(self):
        print "stop_hotspot.1.running stop hostpot..." 
        self.wifi_manager_on_always()
        # if wifi in hotpot mode ...
        stautsHotspot = Util.cmd("nmcli dev show wlp2s0 |  grep 'GENERAL.CONNECTION:' | perl -lane 'print $F[1]'",True)
        stautsHotspot = stautsHotspot.strip(' \t\n\r')
        print "check hostpot status: '" + stautsHotspot+ "' ...." #stautsHotspot
        if stautsHotspot == "Hotspot":
            print "stop_hotspot.2. stopping hostpot..."    
            Util.cmd("sudo nmcli c down Hotspot", True)    
              
        time.sleep(5)

    def wifi_manager_on_always(self):
        status = Util.cmd("sudo nmcli radio wifi", True)
        status =status.strip(' \t\n\r')
        print "checking wifi manager info status: " + status
        if status=="disabled" :
            Util.cmd("sudo nmcli radio wifi on", True)
            time.sleep(3)
            status = Util.cmd("sudo nmcli radio wifi", True)
            status =status.strip(' \t\n\r')
            print "checking 2 wifi manager info status: " + status
            return status     
        return status 

    def start_hotspot(self):
 
        self.wifi_manager_on_always()
        # check if its aready hotsport. dont on/off wifi again. 
        stautsHotspot = Util.cmd("nmcli dev show wlp2s0 |  grep 'GENERAL.CONNECTION:' | perl -lane 'print $F[1]'",True)
        stautsHotspot = stautsHotspot.strip(' \t\n\r')
        print "check hostpot status: '" + stautsHotspot+ "' ...." #stautsHotspot
        if stautsHotspot != "Hotspot":
            print "turnning on hostpot status: '" + self._ssid + "' ...."
            Util.cmd("sudo nmcli c up Hotspot", True)
        print "hotspot's running..."

    def stop_hotspot_and_connect_wifi(self, ssid, wpa):
        
        print "Stop hostpot and connecting wifi ssid: %s, wpa: %s ..." % (ssid.encode("UTF-8"), wpa.encode("UTF8"))
        
        self.wifi_manager_on_always()
        # check is hotpost on.... 
        stautsHotspot = Util.cmd("nmcli dev show wlp2s0 |  grep 'GENERAL.CONNECTION:' | perl -lane 'print $F[1]'",True)
        stautsHotspot = stautsHotspot.strip(' \t\n\r')
        print "check hostpot status: '" + stautsHotspot+ "' ...."
        if stautsHotspot == "Hotspot":
            Util.cmd("sudo nmcli c down Hotspot", True)                
            time.sleep(5)
        print "connecting wifi ..."
        
        Wifi.connect(ssid, wpa) 

        return Util.check_internet_connection2()


class Wifi(object):

    @staticmethod
    def wpa_cli_scan_old():
        cmd = "sudo wpa_cli scan && sleep 2 && sudo wpa_cli scan_result"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return proc.stdout

    @staticmethod
    def wpa_cli_scan():
        cmd = "sudo wpa_cli scan && sleep 2 && sudo wpa_cli scan_result"
        data = Util.cmd(cmd)
        return data.split("\n")

    @staticmethod
    def lists():
        result = []
        header_name = ["bssid", "frequency", "signal_level", "flags", "ssid"]
        response = Wifi.wpa_cli_scan()
        for line in response:
            items = line.rstrip('\n').split("\t")
            if len(items) == 5:
                item = {header_name[0]: items[0], header_name[1]: items[1], header_name[2]: items[2],
                        header_name[3]: items[3], header_name[4]: items[4].decode("string-escape")}
                result.append(item)
        return result

    @staticmethod
    def connect(ssid, wpa):        
        print "wifi.connect.1. Connecting wifi ssid: %s, wpa: %s ..." % (ssid.encode("UTF-8"), wpa.encode("UTF8"))
        #check turn off hotspot 
        stautsHotspot = Util.cmd("nmcli dev show wlp2s0 |  grep 'GENERAL.CONNECTION:' | perl -lane 'print $F[1]'",True)
        stautsHotspot = stautsHotspot.strip(' \t\n\r')
        
        print "wifi.connect.2. check hostpot status: '" + stautsHotspot+ "' ...."
        if stautsHotspot == "Hotspot":
            Util.cmd("sudo nmcli c down Hotspot", True)     
            time.sleep(5)           
        #Util.cmd("sudo nmcli radio wifi on",True)
        status = Util.cmd("sudo nmcli radio wifi", True)
        status =status.strip(' \t\n\r')
        print "wifi.connect.3. checking wifi manager info status: " + status
        if status=="disabled" :
            Util.cmd("sudo nmcli radio wifi on",True)
            time.sleep(5)
            
        #check neu dang o hotspot => turn off hotspot 
        if wpa is not None and len(wpa) != 0:
            # Util.cmd("sudo sta " + ssid.encode("UTF8") + " " + wpa.encode("UTF8"))
            Util.cmd("sudo nmcli d wifi connect " + ssid.encode("UTF8") + " password " + wpa.encode("UTF8"),True)
        else:
            # Util.cmd("sudo sta " + ssid.encode("UTF8"))
            Util.cmd("sudo nmcli d wifi connect " + ssid.encode("UTF8"))
        
        try :
            data_wifi = {"ssid":ssid, "wpa":wpa}
            Util.write_file(CURRENT_PATH+'data/wifiInfo.json',data_wifi)   
        except:
            pass 
        return Util.check_internet_connection2()

    @staticmethod
    def check_wifi():
        return Util.check_internet_connection2(steps=2)

    @staticmethod
    def get_data_wifi_current():
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
            in_file = f.readlines()
            f.close()
        return in_file

    @staticmethod
    def get_current_wifi():
        try:
            data_wifi = Wifi.get_data_wifi_current()
            for line in data_wifi:
                if "ssid" in line:
                        return line.split("=")[1].replace('"', '').decode("string-escape")
        except Exception as e:
            print str(e)

        return ""

    @staticmethod
    def get_current_wifi_ssid_psk():
        try:
            ssid = ""
            wpa = ""
            data_wifi = Wifi.get_data_wifi_current()
            for line in data_wifi:
                if "ssid" in line:
                    ssid = line.split("=")[1].replace('"', '').decode("string-escape").rstrip()
                if "psk" in line:
                    wpa = line.split("=")[1].replace('"', '').decode("string-escape").rstrip()
        except Exception as e:
            print str(e)

        return (ssid, wpa) if ssid and wpa else None
    @staticmethod
    def reconnect():
        #wifi = Wifi.get_current_wifi_ssid_psk()
        try:
            data_wifi= Util.read_file(CURRENT_PATH+'data/wifiInfo.json')  
            print "wifi.reconnect.1. reconnect wifi "
            print data_wifi 
            return Wifi.connect(data_wifi["ssid"], data_wifi["wpa"])

        except:
            print "wifi.reconnect.2. reconnect wifi failed "
            return False
 

    # @staticmethod
    # def get_data_wifi_current():
    #     with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
    #         in_file = f.readlines()
    #         f.close()
    #     return in_file
    #
    # @staticmethod
    # def get_current_wifi():
    #     rasberry_wifi = RasberryWifi()
    #     return rasberry_wifi.active_network()

    @staticmethod
    def is_usb_wifi_connect():
        interfaces = netifaces.interfaces()
        if "wlan0" in interfaces:
            return True
        return False
