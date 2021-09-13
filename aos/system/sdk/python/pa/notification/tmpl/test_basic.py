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
    APP = 'smart_spotify'
    # varibles
    id = 1
    icon = 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png'
    title = "Set tasks"
    description = "Demo set tasks"
    timeout = 12
    
    # use tmpl
    basic = Basic(**{
      "id": id,
      "icon": icon,
      "title": title,
      "description": description,
      "timeout": timeout
    })
    # build expected
    expected = {
      "id": id,
      "icon": icon,
      "title": title,
      "desc": description,
      "tmpl": Basic.TMPL,
      "timeout": timeout,
      "priority": 0,
      "block": False,
      "buttons": []
    }
    self.assertEquals(basic.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
