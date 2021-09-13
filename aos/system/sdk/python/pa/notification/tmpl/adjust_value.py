"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class AdjustValue(Tmpl):
  """Template # Text"""

  TMPL = "adjust_value" # Template name, for uses in PA

  def __init__(self, title, description = '', value = 0, action = {}, min = 0, max = 999, increase = 1, decrease = 1, id = None, *args, **kwargs):
    """Initilize"""
    super(AdjustValue, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.tmpl = AdjustValue.TMPL
    self.value = value
    self.action = action
    self.min = min
    self.max = max
    self.increase = increase
    self.decrease = decrease
#end
