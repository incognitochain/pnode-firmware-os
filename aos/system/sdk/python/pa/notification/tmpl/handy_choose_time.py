"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class HandyChooseTime(Tmpl):
  """Template # Text"""

  TMPL = "handy_choose_time" # Template name, for uses in PA

  def __init__(self, title, description, hours = 2, time = '', note = '', action = {}, id = None, *args, **kwargs):
    """Initilize"""
    super(HandyChooseTime, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.hours = hours
    self.time = time
    self.note = note
    self.tmpl = HandyChooseTime.TMPL
    self.action = action
#end
