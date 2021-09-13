#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from aos.ability.firmware_update.update_online import UpdateOnline
from aos.ability.install_ability_device.install_app import InstallUpdateAbility
from messages import MESSAGE
from help import Help
from aos.system.libs.ability import Ability
from aos.system.libs.fimware import Firmware
from aos.system.configs.channel import BASE_APP, CURRENT_PATH
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util


class RunUpdate(object):

    @staticmethod
    def update_firmware(source=""):

        list_ability_not_restart = ['product_control']

        Help.open_waiting_update_ability(MESSAGE.TITLE_UPDATE_OS, "Checking...", 0)

        Help.open_waiting_update_ability(MESSAGE.TITLE_UPDATE_OS, "Checking...", 0)

        Help.s2b_stop_check_update()

        user_id = Util.get_user_id()
        product_id = Util.get_product_id()

        update_product_control = False

        total_size = 0
        total_size_downloaded = 0

        list_ability_need_update = []
        firmware_data_update = None

        update_success = True

        if user_id != -1 and product_id != '':
            print "loading all ability ...."
            list_ability = Ability.list()
            if list_ability:
                print "checking local/core app ..."
                for ab in list_ability:
                    print "check ability for " + ab['app'], ", is_core_app:", ab['is_core_app'], "is_local: ", ab['is_local']
                    if ab['is_core_app'] and ab['is_local'] == 1:
                        new_version = Util.convert_version(ab['version'])
                        app_base_dir = BASE_APP + ab['app']
                        app_config = Util.read_file(app_base_dir + "/config.json")
                        current_version = -1
                        if app_config:
                            current_version = Util.convert_version(app_config['version'])
                        print "app_config: ", app_config, "current_version: ", current_version, " new_version: ", new_version
                        if current_version < new_version:
                            ab['action'] = "add"
                            list_ability_need_update.append(ab)
                            zip_size = Help.get_size(ab['link'])
                            total_size += zip_size
                            ab['size'] = zip_size
                            print "size->", zip_size

            print "checking new version firmware is available ..."
            new_firmware_data = Firmware.get_current()
            print 'new_version=>', new_firmware_data
            if new_firmware_data and 'status' in new_firmware_data and new_firmware_data['status'] == 1:
                if Util.get_version(CURRENT_PATH) < Util.convert_version(new_firmware_data['data']['version']):
                    firmware_data_update = new_firmware_data['data']
                    firmware_data_update['link'] = firmware_data_update['source']
                    zip_size = Help.get_size(firmware_data_update['link'])
                    total_size += zip_size
                    firmware_data_update['size'] = zip_size
                    print "os size->", zip_size
                else:
                    print "deo phai version moi"

        print ("total zip size: %d" % total_size)

        print ("starting install ability...")
        for ab in list_ability_need_update:

                if ab['app'] == 'product_control':
                    update_product_control = True

                ab['total_size'] = total_size
                ab['total_size_downloaded'] = total_size_downloaded

                result_installed = InstallUpdateAbility(ab, source).add()
                if result_installed:
                    total_size_downloaded += ab['size']
                else:
                    update_success = False
                print "install %s is %s" % (ab['app'], str(result_installed))

                Help.s2b_remove_updating(ab['app'])

                if ab['app'] not in list_ability_not_restart:
                    Help.s2b_result_install(result_installed, ab['app'], "", "add")

        if update_success:
            Help.up_os_version()

        if firmware_data_update:
            firmware_data_update['total_size'] = total_size
            firmware_data_update['total_size_downloaded'] = total_size_downloaded
            UpdateOnline(firmware_data_update, source=source).run()

        if update_product_control:
            print "call restart brain"
            json_data = {"source": "", "protocol": "", "type": "restart_brain", "data": {}}
            send_json(json_data)
            Util.cmd("sudo reboot")
        else:
            Help.s2b_continue_check_update()

