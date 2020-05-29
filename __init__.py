
import bpy

bl_info = {
    "name": "BJsTools",
    "author": "Bjoern Siegert",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Bjoern's custom tools",
    "warning": "",
    "category": "",
}


from . import model_prep
from . import origin_module
from . import pie_menu

import importlib
importlib.reload(model_prep)
importlib.reload(origin_module)
importlib.reload(pie_menu)


def register():
    origin_module.register()
    model_prep.register()
    pie_menu.register()


def unregister():
    origin_module.unregister()
    model_prep.unregister()
    pie_menu.unregister()


if __name__ == "__main__":
    register()