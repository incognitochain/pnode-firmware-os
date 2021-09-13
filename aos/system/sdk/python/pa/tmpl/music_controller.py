"""PA sdk # Template # MusicController"""
from __future__ import print_function
from . import Tmpl

#
class MusicController(Tmpl):
    """Template # MusicController"""

    TMPL = "music_controller" # Template name, for uses in PA

    def __init__(self, id, title, description, left_icon = 'previous', left_icon_action={}, mid_icon='pause', mid_icon_action={}, right_icon='next', right_icon_action={}, volume=0, volume_changed_action={}, active = False, app=None, *args, **kwargs):
        """Initilize"""
        super(MusicController, self).__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.description = description
        self.tmpl = MusicController.TMPL
        self.left_icon = left_icon
        self.left_icon_action = left_icon_action
        self.mid_icon = mid_icon
        self.mid_icon_action = mid_icon_action
        self.right_icon = right_icon
        self.right_icon_action = right_icon_action
        self.volume = volume
        self.volume_changed_action = volume_changed_action
        self.active = active
        self.app = app
    #end