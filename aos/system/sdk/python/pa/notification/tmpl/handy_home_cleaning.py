"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class HandyHomeCleaning(Tmpl):
  """Template # Text"""

  TMPL = "handy_home_cleaning" # Template name, for uses in PA

  def __init__(self, title, description, beds = 1, baths = 1, time = '', note = '', action = {}, id = None, *args, **kwargs):
    """Initilize"""
    super(HandyHomeCleaning, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.beds = beds
    self.baths = baths
    self.time = time
    self.note = note
    self.tmpl = HandyHomeCleaning.TMPL
    self.action = action
#end
