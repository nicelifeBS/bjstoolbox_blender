"""Assign a random material to each object in the selection"""

import bpy
import bmesh

import random
from collections import Counter


def apply_random_material():
    """Apply each selected object a random material color if it has none assigned."""
    for obj in bpy.context.selected_objects:
        if obj.type != "MESH":
            continue
        obj_mats = obj.data.materials
        if len(obj_mats) == 0:    
            new_material = bpy.data.materials.new(name="{}_material".format(obj.name))
            new_material.diffuse_color = (random.random(), random.random(), random.random(), 1.0)
            obj_mats.append(new_material)
            print("added material: {}".format(new_material))


def smart_uv():
    """Smart UV all selected objects and do a pack islands."""
    selection = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode = 'OBJECT')
    objects = []
    for obj in selection:
        if obj.type == "MESH":
            objects.append(obj)
    # deselect objects for speed reasons
    bpy.ops.object.select_all(action='DESELECT')
    for idx, obj in enumerate(objects):    
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action= 'SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.uv.pack_islands(margin=0.001)
        print("Processed: {} of {}: {}".format(idx + 1, len(bpy.context.selected_objects), obj.name))
        bpy.ops.object.mode_set(mode = 'OBJECT')
    print("DONE!")
    # reselect objects
    for obj in selection:
        obj.select_set(True)


def auto_align_uvs():
    """Align uvs and do a follow object unwrap"""
    obj = bpy.context.active_object
    data = obj.data
    bm = bmesh.from_edit_mesh(data)
    uv_layer = bm.loops.layers.uv.verify()

    face_ids = []
    edges = []
    verts = {}
    for face in bm.faces:
        for loop in face.loops:
            uv = loop[uv_layer]
            if uv.select:
                face_ids.append(loop.face.index)
                if loop.vert in verts:
                    verts[loop.vert].append(uv)
                else:
                    verts[loop.vert] = [uv]
                edges.append(loop.edge)
    
    # find the index of the selected face of the UVs
    counted = dict(Counter(face_ids))
    face_id = None
    for id, c in counted.items():
        if c == 4:
            face_id = id
            break
    # filter edges which only belong to selected face id
    new_edges = []
    for edge in edges:
        for face in edge.link_faces:
            if face.index == face_id:
                new_edges.append(edge)
    new_edges = list(set(new_edges))

    # clear selection and align uvs
    bpy.ops.uv.select_all(action='DESELECT')
    processed_uvs = []
    for edge in new_edges:
        v1, v2 = edge.verts
        uv1, uv2 = verts[v1][0], verts[v2][0]
        x = abs(uv1.uv[0] - uv2.uv[0])
        y = abs(uv1.uv[1] - uv2.uv[1])
        for uv in verts[v1]:
            uv.select = True
        for uv in verts[v2]:
            uv.select = True
        if x < y:
            bpy.ops.uv.align(axis='ALIGN_X')
        else:
            bpy.ops.uv.align(axis='ALIGN_Y')
        processed_uvs.append(uv1)
        processed_uvs.append(uv2)
        bpy.ops.uv.select_all(action='DESELECT')
    # select island and run follow active quads
    for uv in processed_uvs:
        uv.select = True
        bpy.ops.uv.select_linked()
    bpy.ops.uv.follow_active_quads()


class AutoFollowActiveQuads(bpy.types.Operator):
    bl_idname = "object.auto_follow_quads"
    bl_label = "Auto follow quads"

    def execute(self, context):
        auto_align_uvs()
        return {'FINISHED'}


class AutoSmartUV(bpy.types.Operator):
    bl_idname = "object.auto_smart_uv"
    bl_label = "Create smart UVs on selected Objects"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        smart_uv()
        return {'FINISHED'}


class AssignRandomMaterial(bpy.types.Operator):
    bl_idname = "object.assign_random_material"
    bl_label = "Assign Random Material"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        apply_random_material()
        return {'FINISHED'}


def uv_menu(self, context):
    self.layout.separator()
    self.layout.operator("object.auto_follow_quads")


def register():
    bpy.utils.register_class(AssignRandomMaterial)    
    bpy.utils.register_class(AutoSmartUV)    
    bpy.utils.register_class(AutoFollowActiveQuads)
    bpy.types.IMAGE_MT_uvs_context_menu.append(uv_menu)  


def unregister():
    bpy.utils.unregister_class(AssignRandomMaterial)
    bpy.utils.unregister_class(AutoSmartUV)
    bpy.utils.unregister_class(AutoFollowActiveQuads)
    bpy.types.IMAGE_MT_uvs_context_menu.append(uv_menu)
