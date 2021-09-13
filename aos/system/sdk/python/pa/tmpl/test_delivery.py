#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from delivery import Delivery

class TestDelivery(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestDelivery, self).__init__(*args, **kwargs)

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
    price = 5.47
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
    delivery = Delivery(**{
      "id": id,
      "title": title,
      "description": description,
      "price": price,
      "app": APP,
      "app_action": app_action
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "price": price,
      "tmpl": Delivery.TMPL,
      "app_action": app_action,
      "app": APP,
      "background": None,
      "color": None,
      "active": False
    }
    self.assertEquals(delivery.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
