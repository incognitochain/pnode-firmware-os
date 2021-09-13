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

  def force_array(self, data):
    """Force input data to array"""
    _type = type(data)
    data = [data] if not (_type is list) else data
    return data

from address import Address
from basic import Basic
from adjust_value import AdjustValue
from choice import Choice
from text import Text
from payment import Payment
from combat_burnout import CombatBurnout
from handy_choose_time import HandyChooseTime
from handy_home_cleaning import HandyHomeCleaning