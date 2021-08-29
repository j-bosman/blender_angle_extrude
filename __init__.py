import bpy

from . import angle_extrude


bl_info = {
    "name": "Angle extrude",
    "description": "Extrude at an angle.",
    "version": (0, 1),
    "blender": (2, 93, 0),
    "warning": "",
    "category": "Mesh",
}


def register():
    bpy.utils.register_class(angle_extrude.AngleExtrudeOp)
    bpy.utils.register_class(angle_extrude.ExtrudeManipulator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(angle_extrude.add_menu)


def unregister():
    bpy.utils.unregister_class(angle_extrude.AngleExtrudeOp)
    bpy.utils.unregister_class(angle_extrude.ExtrudeManipulator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(angle_extrude.add_menu)
