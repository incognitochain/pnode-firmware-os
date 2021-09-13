#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import unittest
from notify import Notify


class TestNotify(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNotify, self).__init__(*args, **kwargs)

    def setUp(self):
        self.notify = Notify()

    def tearDown(self):
        pass

    def test_build_sensor_pa_notification_json_with_valid_data_return_right_format(self):
        actual = self.notify.build_sensor_pa_notification_json(source="1",
                                                               icon="http://google.com",
                                                               title="INFO",
                                                               notification_type="non-blocking",
                                                               timeout="10",
                                                               desc="Hello world")
        expected = {
            "source": "1",
            "type": "personal_assistant",
            "data": {
                "action": "notification",
                "data": {
                    "status": "1",
                    "message": "",
                    "data": {
                        "icon": "http://google.com",
                        "title": "INFO",
                        "type": "non-blocking",
                        "timeout": "10",
                        "desc": "Hello world",
                        "buttons": []
                    }
                },
                "from": ""
            },
            "protocal": ""
        }
        self.assertEquals(actual, expected)

        actual = self.notify.build_sensor_pa_notification_json(source="1",
                                                               icon="http://google.com",
                                                               title="INFO",
                                                               notification_type="non-blocking",
                                                               timeout="10",
                                                               desc="Hello world",
                                                               buttons=[{"background": "#1D7CF3", "textColor": "#FFFFFF", "text": "Stop", "actions": []}])
        expected = {
            "source": "1",
            "type": "personal_assistant",
            "data": {
                "action": "notification",
                "data": {
                    "status": "1",
                    "message": "",
                    "data": {
                        "icon": "http://google.com",
                        "title": "INFO",
                        "type": "non-blocking",
                        "timeout": "10",
                        "desc": "Hello world",
                        "buttons": [{"background": "#1D7CF3", "textColor": "#FFFFFF", "text": "Stop", "actions": []}]
                    }
                },
                "from": ""
            },
            "protocal": ""
        }
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
