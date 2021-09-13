#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import urllib
from time import sleep
import base64
from aos.system.libs.util import Util


class DisplayImage(object):
    _IMAGE_PATH_ = "/home/pi/img/main2.jpg"
    _IMAGE_PATH_TEMP = "/home/pi/img/maintemp.jpg"
    _IMAGE_PATH_MAIN_ = "/home/pi/img/main.jpg"

    @staticmethod
    def download(url):
        try:
            resource = urllib.urlopen(url)
            output = open(DisplayImage._IMAGE_PATH_, "wb")
            output.write(resource.read())
            output.close()
            return True
        except Exception as e:
            print("Error download -> " + str(e))
        return False

    @staticmethod
    def convert_and_display():
        Util.cmd("convert %s  -resize 1080x1920^  -gravity center -extent 1080x1920 %s" % (
            DisplayImage._IMAGE_PATH_, DisplayImage._IMAGE_PATH_))
        sleep(1)
        Util.cmd("convert %s -resize 1080x1920 %s" % (DisplayImage._IMAGE_PATH_, DisplayImage._IMAGE_PATH_MAIN_))
        print("Changed image main.jpg")

    @staticmethod
    def save_image(base64_data):
        try:
            imgdata = base64.b64decode(base64_data)
            with open(DisplayImage._IMAGE_PATH_, 'wb') as f:
                f.write(imgdata)
            return True
        except Exception as e:
            print("Error save image -> " + str(e))
        return False

    @staticmethod
    def display_image(data, type):
        try:
            if type and type == 'base64':
                print("convert base64 to image")
                if DisplayImage.save_image(data):
                    DisplayImage.convert_and_display()
                    return 1
                else:
                    return 0
            else:
                # print ("Url:", data)
                if DisplayImage.download(data):
                    sleep(1)
                    DisplayImage.convert_and_display()
        except Exception as e:
            print("Error display_image -> " + str(e))

    @staticmethod
    def display_text(text):
        Util.cmd(
            "convert %s -gravity South -fill white -draw 'fill-opacity 0.3 rectangle 0,1800 1080,1920' -pointsize 30 -stroke black -strokewidth 3 -annotate +0+12 '%s' -stroke none -fill white -annotate +0+10 '%s' %s" % (
                DisplayImage._IMAGE_PATH_, text, text, DisplayImage._IMAGE_PATH_TEMP))
        sleep(1)
        Util.cmd("convert %s -resize 1080x1920 %s" % (DisplayImage._IMAGE_PATH_TEMP, DisplayImage._IMAGE_PATH_MAIN_))
        print("display text: " + str(text))
