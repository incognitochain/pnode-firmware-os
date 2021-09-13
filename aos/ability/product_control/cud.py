#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from aos.ability.product_control.help import Help
from aos.system.configs.channel import CURRENT_PATH, BASE_APP
from aos.system.libs.ability import Ability
from aos.system.libs.fimware import Firmware
from aos.system.libs.util import Util


class CheckFirmwareUpdate(object):

    def __init__(self):
        self.full_list_app = None

    def check_has_update(self):
        if self.full_list_app:
            for ab in self.full_list_app:
                Help.success_print(ab['app'] + ": is_local=>" + str(ab['is_local']) + ", is_core_app=>" + str(ab['is_core_app']))
                if ab['is_core_app'] and ab['is_local'] == 1:
                    new_version = Util.convert_version(ab['version'])
                    app_base_dir = BASE_APP + ab['app']
                    app_config = Util.read_file(app_base_dir + "/config.json")
                    if not app_config:
                        Help.response_print("need new install ==>" + ab['app'])
                    if app_config and Util.convert_version(app_config['version']) < new_version:
                        Help.response_print("need update ==>" + ab['app'] + ", current version: " + str(Util.convert_version(app_config['version'])) + ", new version: " + str(new_version))
        # check new version firmware is available:
        firmware_data = Firmware.get_current()
        if firmware_data and 'status' in firmware_data and firmware_data['status'] == 1 and 'version' in firmware_data['data']:
            if Util.get_version(CURRENT_PATH) < Util.convert_version(firmware_data['data']['version']):
                Help.response_print("need update  system, " + ", current version: " + str(Util.get_version(CURRENT_PATH)) + ", new version: " + str(Util.convert_version(firmware_data['data']['version'])))

    def run(self):

        print "start check update ..."
        user_id = Util.get_user_id()
        product_id = Util.get_product_id()

        if user_id != -1 and product_id != '':
            self.full_list_app = Ability.list()

cud = CheckFirmwareUpdate()
cud.run()
cud.check_has_update()