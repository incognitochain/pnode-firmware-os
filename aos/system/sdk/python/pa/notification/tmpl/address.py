"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Address(Tmpl):
  """Template # Text"""

  TMPL = "address" # Template name, for uses in PA

  def __init__(self, title, description = '', hint = '', action = {}, required = False, id = None, *args, **kwargs):
    """Initilize"""
    super(Address, self).__init__(*args, **kwargs)
    self.id = id
    self.title = title
    self.description = description
    self.tmpl = Address.TMPL
    self.hint = hint
    self.action = action
    self.required = required
#end
