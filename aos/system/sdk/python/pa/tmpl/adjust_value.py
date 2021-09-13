"""PA sdk # Template # AdjustValue"""
from __future__ import print_function
from . import Tmpl

#
class AdjustValue(Tmpl):
    """Template # AdjustValue"""

    TMPL = "adjust_value" # Template name, for uses in PA

    def __init__(self, id, title, description, value = 0, step = 1, min = None, max = None, changed_action = {}, suffix = '', prefix = '', active = False, app=None, *args, **kwargs):
        """Initilize"""
        super(AdjustValue, self).__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.description = description
        self.tmpl = AdjustValue.TMPL
        self.value = value
        self.step = step
        self.min = min
        self.max = max
        self.changed_action = changed_action
        self.suffix = suffix
        self.prefix = prefix
        self.active = active
        self.app = app
    #end
