"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class CombatBurnout(Tmpl):
  """Template # CombatBurnout"""

  TMPL = "combat_burnout" # Template name, for uses in PA

  def __init__(self, icon, title, description, image, actions = [], timeout = 300, id = None, *args, **kwargs):
    """Initilize"""
    super(CombatBurnout, self).__init__(*args, **kwargs)
    self.id = id
    self.icon = icon
    self.title = title
    self.desc = description
    self.tmpl = CombatBurnout.TMPL
    self.image = image
    self.actions = self.force_array(actions)
    self.timeout = timeout
    #end
