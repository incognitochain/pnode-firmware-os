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
    # varibles
    id = 1
    title = "Set tasks"
    description = "Demo set tasks"
    value = 20
    action = {
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
      "value": value,
      "action": action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "value": value,
      "tmpl": AdjustValue.TMPL,
      "action": action,
      "min": 0,
      "max": 999,
      "increase": 1,
      "decrease": 1
    }
    self.assertEquals(adjust_value.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
