#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import AdjustValue

APP = 'smart_spotify'

data = {
  "title": 'Default',
  "description": 'Just is default.',
  "value": 5,
  "action": {
    "type":"product_control",
    "data": {
      "action": "test"
    },
    "source": "",
    "protocal": ""
  },
}

Notification.notify(APP, AdjustValue(**data).tojson())