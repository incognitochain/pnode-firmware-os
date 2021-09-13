#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa import PA
from aos.system.sdk.python.pa.tmpl import Basic
APP = 'lifx'
ACTION = 'switch_light'
data = [
  {
      "id": 1,
      "title": "Set tasks",
      "description": "Demo set tasks",
      "app": APP,
      "app_action": {
          "type": APP,
          "source": "",
          "protocal": "",
          "data": {
              "action": "set_tasks",
              "from": "personal_assistant",
              "data": {
                  "status": 1,
                  "message": "",
                  "data": {
                      "id": 1
                  }
              }
          }
      }
  },
  {
      "id": 2,
      "title": "Update task",
      "description": "Demo update task",
      "app": APP,
      "app_action": {
          "type": APP,
          "source": "",
          "protocal": "",
          "data": {
              "action": "update_task",
              "from": "personal_assistant",
              "data": {
                  "status": 1,
                  "message": "",
                  "data": {
                      "id": 2
                  }
              }
          }
      }
  },
  {
      "id": 3,
      "title": "Add task",
      "description": "Demo add task",
      "app": APP,
      "app_action": {
          "type": APP,
          "source": "",
          "protocal": "",
          "data": {
              "action": "add_task",
              "from": "personal_assistant",
              "data": {
                  "status": 1,
                  "message": "",
                  "data": {
                      "id": 3
                  }
              }
          }
      }
  },
  {
      "id": 4,
      "title": "Remove task",
      "description": "Demo remove task",
      "app": APP,
      "app_action": {
          "type": APP,
          "source": "",
          "protocal": "",
          "data": {
              "action": "remove_task",
              "from": "personal_assistant",
              "data": {
                  "status": 1,
                  "message": "",
                  "data": {
                      "id": 4
                  }
              }
          }
      }
  }
]


parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=True)
args = parser.parse_args()

if args.f == 'set':
  tasks = []
  for item in data:
    tasks.append(Basic(**item).tojson())
  # call sdk to set task
  PA.set_tasks(APP, ACTION, tasks)
elif args.f == 'add':
  tasks = []
  rd = random.randint(0,999)
  for item in data:
    item['id'] = item['id'] + rd
    item['title'] = item['title'] + ' - ' + str(rd)
    item['description'] = item['description'] + ' - ' + str(rd)
    tasks.append(Basic(**item).tojson())
  # call sdk to add task
  PA.add_task(APP, ACTION, tasks)
elif args.f == 'update':
  tasks = []
  for item in data:
    item['title'] = item['title'] + ' - updated'
    item['description'] = item['description'] + ' - updated'
    tasks.append(Basic(**item).tojson())
  # call sdk to update task
  PA.update_task(APP, ACTION, tasks)
elif args.f == 'remove':
  tasks = []
  for item in data[:2]:
    tasks.append(Basic(**item).tojson())
  # call sdk to remove task
  PA.remove_task(APP, ACTION, tasks)
elif args.f == 'clear':
  # call sdk to remove task
  PA.clear_tasks(APP, ACTION)
else:
  print "nothing todo"
