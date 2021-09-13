"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

default_summary = {
  'items': [],
  'extra_fees': [],
  'tax': 0,
  'delivery': 0,
}

#
class Payment(Tmpl):
  """Template # Text"""

  TMPL = "payment" # Template name, for uses in PA

  def __init__(self, summary = default_summary, tips = 10, address = "", action = {}, id = None, *args, **kwargs):
    """Initilize"""
    super(Payment, self).__init__(*args, **kwargs)
    self.id = id
    self.summary = summary
    self.tips = tips
    self.address = address
    self.tmpl = Payment.TMPL
    self.action = action
#end
