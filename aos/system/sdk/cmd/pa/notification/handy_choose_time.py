#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import HandyChooseTime

APP = 'smart_spotify'

data = {
  "title": 'Default',
  "description": 'Just is default.',
  "action": {
    "type":"product_control",
    "data": {
      "action":"test"
    },
    "source": "",
    "protocal": ""
  },
}

Notification.notify(APP, HandyChooseTime(**data).tojson())