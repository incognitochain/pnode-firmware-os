#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl.basic import Basic

APP = 'smart_spotify'

parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=False)
args = parser.parse_args()

data = {
  "icon": 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png',
  "title": 'Default',
  "description": 'Just is default.',
  "timeout": 60 * 60
}

if args.f == 'priority':
  dataNew = data.copy()
  dataNew['title'] = 'Priority'
  dataNew['priority'] = 1
  Notification.notify(APP, Basic(**dataNew).tojson())
elif args.f == 'button':
  dataNew = data.copy()
  dataNew['title'] = 'Button'
  dataNew['buttons'] = {
    'background': '#AABBCC',
    'text_color': '#112233',
    'text': 'OK'
  }
  Notification.notify(APP, Basic(**dataNew).tojson())
elif args.f == 'buttons':
  dataNew = data.copy()
  dataNew['title'] = 'Buttons'
  dataNew['buttons'] = [
    {
      'background': '#AABBCC',
      'text_color': '#112233',
      'text': 'OK1',
    },
    {
      'background': '#AABBCC',
      'text_color': '#112233',
      'text': 'OK2',
    }
  ]
  Notification.notify(APP, Basic(**dataNew).tojson())
elif args.f == 'timeout':
  dataNew = data.copy()
  dataNew['title'] = 'Timeout'
  dataNew['timeout'] = 2
  Notification.notify(APP, Basic(**dataNew).tojson())
elif args.f == 'id':
  dataNew = data.copy()
  dataNew['id'] = 'testing'
  dataNew['title'] = 'Timeout'
  dataNew['timeout'] = 100
  Notification.notify(APP, Basic(**dataNew).tojson())
elif args.f == 'removeid':
  dataNew = data.copy()
  dataNew['id'] = 'testing'`
  dataNew['title'] = 'Timeout'
  dataNew['timeout'] = 100
  Notification.remove(APP, 'testing')
else:
  Notification.notify(APP, Basic(**data).tojson())

# from aos.system.sdk.python.pa.notification import Notification
# from aos.system.sdk.python.pa.notification.tmpl.basic import Basic

# APP = 'smart_spotify'
# data = {
#   "icon": 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png',
#   "title": 'Default',
#   "description": 'Just is default.',
#   "timeout": 60 * 60
# }
# Notification.notify(APP, Basic(**data).tojson())