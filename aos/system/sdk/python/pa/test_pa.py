#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from mock_pa import MockPA
from pa import NOTIFY_TYPE, \
  NOTIFY_ACTION_TMPL_SET_TASKS, \
  NOTIFY_ACTION_TMPL_REMOVE_TASK, \
  NOTIFY_ACTION_TMPL_UPDATE_TASK, \
  NOTIFY_ACTION_TMPL_ADD_TASK, \
  NOTIFY_ACTION_TMPL_CLEAR_TASKS

APP = 'lifx'
APP_ACTION = 'switch_light'

array_data = [
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

single_data = {
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
}

class TestPA(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestPA, self).__init__(*args, **kwargs)

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_set_tasks(self):
    result = MockPA.set_tasks(APP, APP_ACTION, array_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_SET_TASKS,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": array_data,
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)

  def test_set_tasks_single(self):
    result = MockPA.set_tasks(APP, APP_ACTION, single_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_SET_TASKS,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": [single_data],
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)

  def test_add_task_single(self):
    result = MockPA.add_task(APP, APP_ACTION, single_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_ADD_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": [single_data],
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)
  
  def test_add_task_multi(self):
    result = MockPA.add_task(APP, APP_ACTION, array_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_ADD_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": array_data,
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)

  def test_add_task_prepend(self):
    result = MockPA.add_task(APP, APP_ACTION, array_data, True)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_ADD_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": array_data,
              "opts": {
                "prepend": True
              }
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)

  def test_update_task_single(self):
    result = MockPA.update_task(APP, APP_ACTION, single_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_UPDATE_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": [single_data],
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEqual(result, expected)
  
  def test_update_task_multi(self):
    result = MockPA.update_task(APP, APP_ACTION, array_data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_UPDATE_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": array_data,
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEqual(result, expected)
  
  def test_remove_task_single(self):
    id = 1
    result = MockPA.remove_task(APP, APP_ACTION, id)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_REMOVE_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": [id],
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEqual(result, expected)
  
  def test_remove_task_multi(self):
    ids = [1,2,3]
    result = MockPA.remove_task(APP, APP_ACTION, ids)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_REMOVE_TASK,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": ids,
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEqual(result, expected)

  def test_clear_tasks(self):
    result = MockPA.clear_tasks(APP, APP_ACTION)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
          "action": NOTIFY_ACTION_TMPL_CLEAR_TASKS,
          "data": {
              "app": APP,
              "action": APP_ACTION,
              "data": None
          },
          "from": APP
      },
      "protocal": ""
    }
    self.assertEqual(result, expected)

if __name__ == '__main__':
  unittest.main()
