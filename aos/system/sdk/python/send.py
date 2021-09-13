#!/usr/bin/env python
import os
import time
import zmq


def send_json(json_data):
    if not ('ENV' in os.environ and os.environ['ENV'] == 'TRAVIS'):
        c = zmq.Context()
        s = c.socket(zmq.PUSH)
        s.connect("ipc:///tmp/brain_zmq_sensor")

        s.send_json(json_data)

        time.sleep(1)
