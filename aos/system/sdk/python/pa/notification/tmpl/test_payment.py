#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from payment import Payment

class TestPayment(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestPayment, self).__init__(*args, **kwargs)

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_generate_json_data(self):
    # constant
    APP = 'lifx'
    # varibles
    id = 1
    summary = {
      'items': [{
        'name': 'Baking Soda',
        'price': 10
      },
      {
        'name': 'Baking Soda 2',
        'price': 12
      }],
      'extra_fees': [],
      'tax': 9.3,
      'delivery': 5.2,
    }
    tips = 20
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
    payment = Payment(**{
      "id": id,
      "summary": summary,
      "tips": tips,
      "action": action
    })
    # build expected
    expected = {
      "id": id,
      "summary": summary,
      "tips": tips,
      "tmpl": Payment.TMPL,
      "action": action,
      "address": ''
    }

    self.assertEquals(payment.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
