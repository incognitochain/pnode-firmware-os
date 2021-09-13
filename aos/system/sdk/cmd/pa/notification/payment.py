#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import Payment

APP = 'smart_spotify'

data = {
  "summary": {
    'items': [{
      'name': 'Baking Soda',
      'price': 10
    },
    {
      'name': 'Baking Soda 2',
      'price': 12
    }],
    'extra_fees': [],
    'tax': 9.3,
    'delivery': 5.2,
  },
  "action": {
    "type":"product_control",
    "data": {
      "action":"test"
    },
    "source": "",
    "protocal": ""
  },
}

Notification.notify(APP, Payment(**data).tojson())