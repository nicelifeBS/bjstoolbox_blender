
import bpy


def origin_context_menu(self, context):
    """Context menu in mesh edit mode for SetOriginToSelection operator
    
    Args:
        self:
        context:
    """
    self.layout.separator()
    self.layout.operator("object.quick_set_origin")


def set_origin_to_selection(context):
    """Main execution function"""
    cursor_location = context.scene.cursor.location.copy()
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    # reset cursor to previous location
    context.scene.cursor.location = cursor_location
    

class SetOriginToSelection(bpy.types.Operator):
    """Set the origin to the selected"""
    bl_idname = "object.quick_set_origin"
    bl_label = "Set Origin to Selection"

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT"

    def execute(self, context):
        set_origin_to_selection(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SetOriginToSelection)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(origin_context_menu)


def unregister():
    bpy.utils.unregister_class(SetOriginToSelection)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(origin_context_menu)
