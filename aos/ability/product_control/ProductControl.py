#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import json
import os
import time

import sys

from messages import MESSAGE


class ProductControl(object):

    def __init__(self, setup, testing_mode=False):
        super(ProductControl, self).__init__()
        self.product_id = ""
        self.check_internet_connection = None
        self.testing_mode = testing_mode
        self.setup = setup

    def check_setup(self):
        self.setup.check_setup()

    def processing_data(self, data, source):

        start_time = time.time()

        action = "unknown"
        to_sensor = "phone_control"
        from_sensor = "product_control"

        self.setup.source = source

        status = 0

        try:
            if isinstance(data, dict) and 'action' in data:

                action = data.get('action', None)
                to_sensor = data.get("from", to_sensor) if data else to_sensor
                data = data.get('data', None)

                return_data = getattr(self.setup, action)(data)

                status, message, data = return_data["status"], return_data["message"], return_data["data"]

            else:
                message = MESSAGE.DATA_NOT_VALID

        except Exception as e:
            message = str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            from help import Help
            Help.fail_prints([exc_type, fname, exc_tb.tb_lineno])

        # create the package to send to brain:
        package = ProductControl.create_package(status, action, message, data, from_sensor, to_sensor, source)

        # send to brain (PA or phone):
        try:
            from help import Help
            Help.fail_print("--- ProductControl <%s> executed time: %s seconds ---" % (action, time.time() - start_time))
        except Exception as e:
            print str(e)
        return self.send_return_data_package(package)

    @staticmethod
    def current_timestamp():
        return int(round(time.time() * 1000))

    @staticmethod
    def generate_data(status, action, message, data, from_sensor):

        data = {"status": status, "data": data, "message": message}

        return {"action": action, "from": from_sensor, "data": data, "timestamp": ProductControl.current_timestamp()}

    @staticmethod
    def create_package(status, action, message, data, from_sensor, to_sensor, source):

        data = ProductControl.generate_data(status, action, message, data, from_sensor)

        return {"type": to_sensor, "source": source, "data": data, "protocol": ""}

    def send_return_data_package(self, package):

        if self.testing_mode:
            return package

        ProductControl.send_json_and_log(package) 
        return True

    @staticmethod
    def send_json_and_log(package):
        from aos.system.sdk.python.send import send_json
        send_json(package)
        try:
            from help import Help
            Help.success_print("SEND TO %s WITH DATA ==> %s" % (package['type'], json.dumps(package, indent=4, sort_keys=True)))
        except Exception as e:
            print str(e)

