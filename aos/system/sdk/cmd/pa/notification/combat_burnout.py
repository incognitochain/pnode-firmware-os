#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.notification import Notification
from aos.system.sdk.python.pa.notification.tmpl import CombatBurnout

APP = 'smart_spotify'

parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=False)
args = parser.parse_args()

data = {
  "icon": 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png',
  "title": 'Default',
  "description": 'Just is default.',
  "image": 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png'
}

Notification.notify(APP, CombatBurnout(**data).tojson())