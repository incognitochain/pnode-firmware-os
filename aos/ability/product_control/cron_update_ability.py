#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
# Write by Hoang Phuong
#
from threading import Thread

from aos.system.libs.ability import Ability
from aos.system.configs.channel import BASE_APP
import time
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util


TIME_CHECK = 600


class CronUpdateAbility(Thread):

    def __init__(self):
        self.stop = False
        self.need_update_abilities = []
        self.updating = False
        self.json_data_install = {"source": "", "protocol": "", "type": "install_ability_device"}
        super(CronUpdateAbility, self).__init__()

    def get_need_update_abilities(self):
        try:
            list_app = Ability.list()
            self.need_update_abilities = []
            if list_app:
                for ab in list_app:
                    # only local and not core app:
                    if ab['is_core_app'] == 0 and ab['is_local'] == 1:
                        new_version = Util.convert_version(ab['version'])
                        app_base_dir = BASE_APP + ab['app']
                        app_config = Util.read_file(app_base_dir + "/config.json")
                        if not app_config or (app_config and Util.convert_version(app_config['version']) < new_version):
                            ab['action'] = "add"
                            ab['silent'] = True
                            self.need_update_abilities.append(ab)
                return True
        except Exception as e:
            print str(e)

        return False

    def do_update(self):
        self.updating = True
        if self.get_need_update_abilities():
            for ability in self.need_update_abilities:
                self.json_data_install['data'] = ability
                print "send sensor instal ability %s to brain ..." % ability['app']
                send_json(self.json_data_install)
                time.sleep(5)
        self.updating = False

    def run(self):
        while True:
            time.sleep(TIME_CHECK)
            if not self.stop and not self.updating:
                self.do_update()

    def force_run(self):
        if not self.updating:
            self.do_update()




