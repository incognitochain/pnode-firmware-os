"""PA sdk # Template based class"""
from __future__ import print_function
from abc import ABCMeta, abstractmethod

#
NOTIFY_FROM = "lifx"

class Tmpl(object):
    """Template # Basic"""
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        """Initilize"""
        super(Tmpl, self).__init__()
    #end

    def tojson(self):
        """ Convert object template to json data for uses with templates. """
        return self.__dict__
    #end

from adjust_value import AdjustValue
from basic import Basic
from delivery import Delivery
from music_controller import MusicController
from switcher import Switcher