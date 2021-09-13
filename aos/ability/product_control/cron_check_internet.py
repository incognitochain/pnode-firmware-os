#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
# Write by Hoang Phuong
#
from threading import Thread

import time

from Commands import COMMANDS
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util


TIME_CHECK = 60
MAX_COUNT = 3


class CronCheckInternet(Thread):

    def __init__(self):
        self.stop = True
        self.count = 0
        super(CronCheckInternet, self).__init__()

    def stop_thread(self):
        self.stop = True
        self.count = 0

    def reset(self):
        self.stop = False
        self.count = 0

    def run(self):
        while True:

            if self.stop is False:
                IPS = ['10.42.0.1']
                ip = Util.get_ip_address()
                if ip not in IPS:
                    if not Util.internet_on2():
                        self.count += 1
                        print "count->", self.count
                        if self.count == MAX_COUNT:
                            self.send_PA()
                            self.count = 0
                            self.stop_thread()
                        else:
                            time.sleep(TIME_CHECK)
            else:
                break

    def send_PA(self):
        # try connect wifi:
        print "internet no connection, try connect ..."
        # Util.cmd('sudo ifup wlan0')
        if not Util.internet_on2():
            print "send sensor start hotspot to product_control"
            data = {"action": 'start_hotspot', "from": "phone_control",
                    "data": {"data": False}}

            s = {"source": "", "type": "product_control", "data": data, "protocol": ""}
            send_json(s)
        else:
            print "try connect internet success"
