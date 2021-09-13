#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from choice import Choice

class TestChoice(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestChoice, self).__init__(*args, **kwargs)

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
    data = [
      {
        "title": "!23",
        "description": "def",
      },
      {
        "title": "!234",
        "description": "def123",
      },
      {
        "title": "!235",
        "description": "def456",
      },
    ]
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
    choice = Choice(**{
      "id": id,
      "title": title,
      "description": description,
      "data": data,
      "action": action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "data": data,
      "tmpl": Choice.TMPL,
      "action": action,
      "min": 0,
      "max": 255
    }
    self.assertEquals(choice.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
