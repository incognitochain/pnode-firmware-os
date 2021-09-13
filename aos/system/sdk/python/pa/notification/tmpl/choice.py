"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Choice(Tmpl):
  """Template # Text"""

  TMPL = "choice" # Template name, for uses in PA

  def __init__(self, title, description = '', data = [], action = {}, min = 0, max = 255, id = None, *args, **kwargs):
    """Initilize"""
    super(Choice, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.tmpl = Choice.TMPL
    self.data = self.force_array(data)
    self.action = action
    self.min = min
    self.max = max
#end
