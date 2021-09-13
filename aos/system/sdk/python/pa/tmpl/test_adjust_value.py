#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from adjust_value import AdjustValue

class TestAdjustValue(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestAdjustValue, self).__init__(*args, **kwargs)

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
    value = 23
    step = 1
    min = 20
    max = 70
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
    adjust_value = AdjustValue(**{
      "id": id,
      "title": title,
      "description": description,
      "app": APP,
      "changed_action": app_action,
      "value": value,
      "step": step,
      "min": min,
      "max": max,
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "tmpl": AdjustValue.TMPL,
      "changed_action": app_action,
      "app": APP,
      "value": value,
      "step": step,
      "min": min,
      "max": max,
      "suffix": '',
      "prefix": '',
      "active": False
    }
    self.assertEquals(adjust_value.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
