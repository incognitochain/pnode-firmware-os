#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from basic import Basic

class TestBasic(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestBasic, self).__init__(*args, **kwargs)

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
    basic = Basic(**{
      "id": id,
      "title": title,
      "description": description,
      "app": APP,
      "app_action": app_action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "tmpl": Basic.TMPL,
      "app_action": app_action,
      "app": APP,
      "background": None,
      "color": None,
      "active": False
    }
    self.assertEquals(basic.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
