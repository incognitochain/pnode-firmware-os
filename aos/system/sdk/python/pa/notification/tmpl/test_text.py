#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from text import Text

class TestText(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestText, self).__init__(*args, **kwargs)

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
    text = Text(**{
      "id": id,
      "title": title,
      "description": description,
      "hint": description,
      "action": action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "hint": description,
      "tmpl": Text.TMPL,
      "action": action,
      "required": False,
      "min": 0,
      "max": 255
    }
    self.assertEquals(text.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
