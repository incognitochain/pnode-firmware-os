"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Basic(Tmpl):
  """Template # Basic"""

  TMPL = "basic" # Template name, for uses in PA

  def __init__(self, icon, title, description, timeout = 10, priority = 0, block = False, buttons = [], id = None, *args, **kwargs):
    """Initilize"""
    super(Basic, self).__init__(*args, **kwargs)
    self.id = id
    self.icon = icon
    self.title = title
    self.desc = description
    self.tmpl = Basic.TMPL
    self.timeout = timeout
    self.priority = priority
    self.block = block
    self.buttons = self.force_array(buttons)
    #end
  
  def add_button(self, text, background, text_color, actions):
    self.buttons.append({
      "text": text,
      "background": background,
      "textColor": text_color,
      "actions": self.force_array(actions)
    })

