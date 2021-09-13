"""PA sdk # Template # Basic"""
from __future__ import print_function
from . import Tmpl

#
class Delivery(Tmpl):
    """Template # Delivery"""

    TMPL = "delivery" # 

    def __init__(self, id, title, description, price, app_action, background = None, color = None, active = False, app=None, *args, **kwargs):
        super(Delivery, self).__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.tmpl = Delivery.TMPL
        self.app_action = app_action
        self.app = app
        self.background = background
        self.color = color
        self.active = active
    #end
