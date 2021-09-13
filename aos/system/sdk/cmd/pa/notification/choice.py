#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import Choice

parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=False)
args = parser.parse_args()

APP = 'smart_spotify'

data = {
  "title": 'Default',
  "description": 'Just is default.',
  "data": [
    {
      "title": "!23",
      "description": "def",
    },
    {
      "title": "!234",
      "description": "def123",
    },
    {
      "title": "!235",
      "description": "def456",
    },
    {
      "title": "aba",
      "description": "def",
    },
    {
      "title": "!aer",
      "description": "def123",
    },
    {
      "title": "!yui",
      "description": "def456",
    }
  ],
  "action": {
    "type":"product_control",
    "data": {
      "action":"test"
    },
    "source": "",
    "protocal": ""
  },
  "min": 1,
  "max": 1
}
if args.f == 'multichoice':
  dataNew = data.copy()
  dataNew['title'] = 'Multichoice'
  dataNew['min'] = 0
  dataNew['max'] = 5
  Notification.notify(APP, Choice(**dataNew).tojson())
elif args.f == 'multichoice13':
  dataNew = data.copy()
  dataNew['title'] = 'Multichoice'
  dataNew['min'] = 1
  dataNew['max'] = 3
  Notification.notify(APP, Choice(**dataNew).tojson())
elif args.f == 'special':
  dataNew = data.copy()
  dataNew['title'] = 'Multichoice'
  dataNew['min'] = 1
  dataNew['max'] = 3
  dataNew['data'] = [
    {
      "title": "Data 1",
      "description": "Data 1 - description",
      "price": 9.82,
      "rating": 4,
    },
    {
      "title": "Data 2",
      "description": "Data 2 - description",
      "price": 3.82,
      "rating": 3.5,
    },
    {
      "title": "Data 3",
      "description": "Data 3 - description",
      "price": 4.5,
      "rating": 4,
    },
    {
      "title": "Data 1",
      "description": "Data 4 - description",
      "price": 98,
      "rating": 2.3,
    }
  ]
  Notification.notify(APP, Choice(**dataNew).tojson())
else:
  Notification.notify(APP, Choice(**data).tojson())