"""PA sdk # Template # Switcher"""
from __future__ import print_function
from . import Tmpl

#
class Switcher(Tmpl):
    """Template # Switcher"""

    TMPL = "switcher" # Template name, for uses in PA

    def __init__(self, id, title, description, prev_action, next_action, active = False, app=None, *args, **kwargs):
        """Initilize"""
        super(Switcher, self).__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.description = description
        self.tmpl = Switcher.TMPL
        self.prev_action = prev_action
        self.next_action = next_action
        self.active = active
        self.app = app
    #end
