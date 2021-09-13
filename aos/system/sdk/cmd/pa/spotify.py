#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa import PA
from aos.system.sdk.python.pa.tmpl.basic import Basic
from aos.system.sdk.python.pa.tmpl.music_controller import MusicController
APP = 'spotify'
ACTION = 'playlist'
data = [
  {
    "id": 1,
    "title": "LIST 1",
    "description": "Until you",
    "app": APP,
    "volume": 10,
    "volume_changed_action": {}
  },
  {
    "id": 2,
    "title": "LIST 2",
    "description": "Until you",
    "app": APP,
    "volume": 10
  },
  {
    "id": 3,
    "title": "LIST 3",
    "description": "Until you",
    "app": APP,
    "volume": 10
  },
  {
    "id": 4,
    "title": "LIST 4",
    "description": "Until you",
    "app": APP,
    "volume": 10
  },
]


parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=True)
args = parser.parse_args()

if args.f == 'set':
  tasks = []
  for item in data:
    tasks.append(MusicController(**item).tojson())
  # call sdk to set task
  PA.set_tasks(APP, ACTION, tasks)
elif args.f == 'add':
  tasks = []
  rd = random.randint(0,999)
  for item in data:
    item['id'] = item['id'] + rd
    item['title'] = item['title'] + ' - ' + str(rd)
    item['description'] = item['description'] + ' - ' + str(rd)
    tasks.append(MusicController(**item).tojson())
  # call sdk to add task
  PA.add_task(APP, ACTION, tasks)
elif args.f == 'update':
  tasks = []
  for item in data:
    item['title'] = item['title'] + ' - updated'
    item['description'] = item['description'] + ' - updated'
    item['volume'] = item['volume'] + 20
    tasks.append(MusicController(**item).tojson())
  # call sdk to update task
  PA.update_task(APP, ACTION, tasks)
elif args.f == 'remove':
  tasks = []
  for item in data[:2]:
    tasks.append(MusicController(**item).tojson())
  # call sdk to remove task
  PA.remove_task(APP, ACTION, tasks)
else:
  print "nothing todo"
