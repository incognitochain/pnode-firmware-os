#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa import PA
from aos.system.sdk.python.pa.tmpl import AdjustValue
APP = 'lifx'
ACTION = 'switch_light'
data = [
  {
    "id": 1,
    "title": "Task 1",
    "description": "Description 1",
    "value": 20,
    "min": 10,
    "max": 30
  },
  {
    "id": 2,
    "title": "Task 2",
    "description": "Description 2",
    "value": 30,
    "min": 40,
    "max": 70
  },
  {
    "id": 3,
    "title": "Task 3",
    "description": "Description 3",
    "value": 40,
    "min": 40,
    "max": 70
  },
  {
    "id": 4,
    "title": "Task 4",
    "description": "Description 4",
    "value": 50,
    "min": 10,
    "max": 40
  }
]


parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=True)
args = parser.parse_args()

if args.f == 'set':
  tasks = []
  for item in data:
    tasks.append(AdjustValue(**item).tojson())
  # call sdk to set task
  PA.set_tasks(APP, ACTION, tasks)
elif args.f == 'add':
  tasks = []
  rd = random.randint(0,999)
  for item in data:
    item['id'] = item['id'] + rd
    item['title'] = item['title'] + ' - ' + str(rd)
    tasks.append(AdjustValue(**item).tojson())
  # call sdk to add task
  PA.add_task(APP, ACTION, tasks)
elif args.f == 'update':
  tasks = []
  for item in data:
    item['title'] = item['title'] + ' - updated'
    tasks.append(AdjustValue(**item).tojson())
  # call sdk to update task
  PA.update_task(APP, ACTION, tasks)
elif args.f == 'remove':
  tasks = []
  for item in data[:2]:
    tasks.append(AdjustValue(**item).tojson())
  # call sdk to remove task
  PA.remove_task(APP, ACTION, tasks)
elif args.f == 'clear':
  # call sdk to remove task
  PA.clear_tasks(APP, ACTION)
else:
  print "nothing todo"
