#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

from __future__ import print_function

import time
from ProductControl import ProductControl
from Commands import COMMANDS
from aos.ability.product_control.setup import Setup
from help import Help
from cron_update_ability import CronUpdateAbility
from cron_check_internet import CronCheckInternet
from cron_check_brain import CronCheckBrain
from aos.system.sdk.python.service_wrapper import AutonomousService

setup = Setup()

productControl = ProductControl(setup)
cron_update_ability = CronUpdateAbility()
cron_check_internet = CronCheckInternet()
cron_check_brain = CronCheckBrain()


def main(json_data, error):
    if error:
        return print (error)

    data = json_data['data']
    sensor = json_data['type'] if 'type' in json_data else None

    if sensor == COMMANDS.CHECK_INTERNET_CONNECTION:
        print ("check_internet_connection->", productControl.check_internet_connection)
        if productControl.check_internet_connection is None:
            return
        if Help.smart_bool(data) is False:
            cron_check_internet.reset()
            cron_check_internet.run()
        else:
            cron_check_internet.stop_thread()
        return

    if sensor == COMMANDS.CHECK_IN:
        cron_update_ability.force_run()

    elif sensor == COMMANDS.STOP_CHECK_UPDATE:
        cron_update_ability.stop = True

    elif sensor == COMMANDS.CONTINUE_CHECK_UPDATE:
        cron_update_ability.stop = False

    elif sensor == COMMANDS.START_CHECK_INTERNET_CONNECTION:
        productControl.check_internet_connection = False

    else:
        productControl.processing_data(data, json_data['source'])


if __name__ == '__main__':

    # cron_update_ability.start()

    cron_check_brain.start()

    print ('sleep to wifi ready to connect ...')
    time.sleep (15)

    productControl.check_setup()

    AutonomousService().run(main)