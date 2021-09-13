"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Basic(Tmpl):
    """Template # Basic"""

    TMPL = "basic" # Template name, for uses in PA

    def __init__(self, id, title, description, app_action, background=None, color=None, active = False, app=None, *args, **kwargs):
        """Initilize"""
        super(Basic, self).__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.description = description
        self.tmpl = Basic.TMPL
        self.app_action = app_action
        self.app = app
        self.background = background
        self.color = color
        self.active = active
    #end
