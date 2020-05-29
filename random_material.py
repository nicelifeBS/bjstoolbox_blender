"""Assign a random material to each object in the selection"""

import bpy
import random


def apply_random_material():
    """Apply each selected object a random material color if it has none assigned."""
    for obj in bpy.context.selected_objects:
        if obj.type != "MESH":
            continue
        print(obj)
        obj_mats = obj.data.materials
        if len(obj_mats) == 0:    
            new_material = bpy.data.materials.new(name="{}_material".format(obj.name))
            new_material.diffuse_color = (random.random(), random.random(), random.random(), 1.0)
            obj_mats.append(new_material)
            print("added material: {}".format(new_material))


def smart_uv():
    """Smart UV all selected objects and do a pack islands."""
    bpy.ops.object.mode_set(mode = 'OBJECT')
    objects = []
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH":
            objects.append(obj)
    bpy.ops.object.select_all(action='DESELECT')
    for idx, obj in enumerate(objects):    
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action= 'SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.uv.pack_islands(margin=0.001)
        print("Processed: {} of {}: {}".format(idx + 1, len(bpy.context.selected_objects), obj.name))
        bpy.ops.object.mode_set(mode = 'OBJECT')
    print("DONE!")