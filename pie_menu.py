
import bpy
from collections import namedtuple


class VIEW3D_PIE_MT_bjstoolbox(bpy.types.Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "BJsToolBox"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        if context.mode == "EDIT":
            pie.operator("object.quick_set_origin")
        if context.mode == "OBJECT":
            pie.operator("object.auto_smart_uv")
            pie.operator("object.assign_random_material")

        
def register():
    bpy.utils.register_class(VIEW3D_PIE_MT_bjstoolbox)
    #bpy_extras.keyconfig_utils.addon_keymap_register(keymap_data)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PIE_MT_bjstoolbox)
