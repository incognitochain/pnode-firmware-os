"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Text(Tmpl):
  """Template # Text"""

  TMPL = "text" # Template name, for uses in PA

  def __init__(self, title, description = '', hint = '', action = {}, required = False, min = 0, max = 255, id = None, *args, **kwargs):
    """Initilize"""
    super(Text, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.tmpl = Text.TMPL
    self.hint = hint
    self.action = action
    self.required = required
    self.min = min
    self.max = max

#end
