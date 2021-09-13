#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from switcher import Switcher

class TestSwitcher(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestSwitcher, self).__init__(*args, **kwargs)

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_generate_json_data(self):
    # constant
    APP = 'lifx'
    ACTION = 'switch_light'
    # varibles
    id = 1
    title = "Set tasks"
    description = "Demo set tasks"
    app_action = {
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
    # use tmpl
    switcher = Switcher(**{
      "id": id,
      "title": title,
      "description": description,
      "app": APP,
      "next_action": app_action,
      "prev_action": app_action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "tmpl": Switcher.TMPL,
      "next_action": app_action,
      "prev_action": app_action,
      "app": APP,
      "active": False
    }
    self.assertEquals(switcher.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
