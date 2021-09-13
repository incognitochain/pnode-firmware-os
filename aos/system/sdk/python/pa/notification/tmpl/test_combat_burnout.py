#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from combat_burnout import CombatBurnout

class TestCombatBurnout(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestCombatBurnout, self).__init__(*args, **kwargs)

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
    image = 'https://s3.amazonaws.com/robotbase-cloud/static/common_icon/' + APP + '.png'
    
    # use tmpl
    combat_burnout = CombatBurnout(**{
      "id": id,
      "icon": icon,
      "title": title,
      "description": description,
      "image": image,
    })
    # build expected
    expected = {
      "id": id,
      "icon": icon,
      "title": title,
      "desc": description,
      "image": image,
      "tmpl": CombatBurnout.TMPL,
      "actions": [],
      "timeout": 300,
    }
    self.assertEquals(combat_burnout.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
