#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from music_controller import MusicController

class TestMusicController(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestMusicController, self).__init__(*args, **kwargs)

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
    left_icon = 'prev'
    mid_icon = 'pause'
    right_icon = 'next'
    volume = 70
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
    mc = MusicController(**{
      "id": id,
      "title": title,
      "description": description,
      "app": APP,
      "left_icon": left_icon,
      "left_icon_action": app_action,
      "mid_icon": mid_icon,
      "mid_icon_action": app_action,
      "right_icon": right_icon,
      "right_icon_action": app_action,
      "volume": volume,
      "volume_changed_action": app_action,
    })
    # build expected
    expected = {
      "id": id,
      "title": title,
      "description": description,
      "tmpl": MusicController.TMPL,
      "app": APP,
      "left_icon": left_icon,
      "left_icon_action": app_action,
      "mid_icon": mid_icon,
      "mid_icon_action": app_action,
      "right_icon": right_icon,
      "right_icon_action": app_action,
      "volume": volume,
      "volume_changed_action": app_action,
      "active": False
    }
    self.assertEquals(mc.tojson(), expected)

if __name__ == '__main__':
  unittest.main()
