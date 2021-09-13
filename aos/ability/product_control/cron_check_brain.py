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

TIME_CHECK = 120

class CronCheckBrain(Thread):

    def __init__(self):        
        super(CronCheckBrain, self).__init__()
    
    
    def run(self):
        while True:            
            self.check_has_brain()
            time.sleep(TIME_CHECK)            

    def check_has_brain (self):
        if Util.cmd("ps ax | grep -v grep | grep 'system/MINER/brain'") == '':
            print "brain dead"
            # restart brain now:
            Util.cmd("tmux send-keys -t brain:brain 'cd $HOME/aos/ && ulimit -s 1024 && ulimit -r 0 && chmod +x system/MINER/brain && system/MINER/brain -b $HOME/aos/data/pr_device.json' C-m", False)
        else:
            print "brain still alive"            