"""Utilities to manage keymaps in blender"""


class ShortCut:
    """Utility ShortCut class"""

    def __init__(self, idname, _type, value):
        self.idname = idname
        self.type = _type 
        self.value = value
        self.any = False
        self.shift = False
        self.ctrl = False
        self.alt = False
        self.oskey = False
        self.key_modifier = "NONE"
        