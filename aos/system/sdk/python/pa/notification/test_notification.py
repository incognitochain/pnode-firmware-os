#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from mock_notification import MockNotification
from pa.notification import NOTIFY_TYPE, \
  NOTIFY_ACTION, REMOVE_ACTION

APP = 'lifx'

data = {
  "id": 1,
  "title": "Set tasks",
  "description": "Demo set tasks",
}

class TestNotification(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestNotification, self).__init__(*args, **kwargs)

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_notify(self):
    result = MockNotification.notify(APP, data)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
        "action": NOTIFY_ACTION,
        "data": {
          "status": 1,
          "message": "",
          "data": data
        },
        "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)
  
  def test_remove(self):
    id = 123
    result = MockNotification.remove(APP, id)
    expected = {
      "source": "",
      "type": NOTIFY_TYPE,
      "data": {
        "action": REMOVE_ACTION,
        "data": {
          "status": 1,
          "message": "",
          "data": [id]
        },
        "from": APP
      },
      "protocal": ""
    }
    self.assertEquals(result, expected)

if __name__ == '__main__':
  unittest.main()
