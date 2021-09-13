#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import Address

APP = 'smart_spotify'

data = {
  "title": 'Default',
  "description": 'Just is default.',
  "hint": 'Just is default 123',
  "action": {
    "type":"product_control",
    "data": {
      "action": "test"
    },
    "source": "",
    "protocal": ""
  },
}

Notification.notify(APP, Address(**data).tojson())