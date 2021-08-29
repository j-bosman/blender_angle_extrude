import bpy


class AngleExtrudeOp(bpy.types.Operator):

    bl_idname = "mesh.angle_extrude"
    bl_label = "Angle extrude"
    bl_space_type = "VIEW_3D"
    bl_options = {'REGISTER', 'UNDO'}

    distance: bpy.props.FloatProperty('distance', default=0.0)
    angle_x: bpy.props.FloatVectorProperty('angle_x', size=2, default=(0.0, 0.0))
    angle_y: bpy.props.FloatProperty('angle_y', default=0.0)

    @classmethod
    def poll(cls, context):
        print('polling')
        ob = context.active_object
        _, edge_mode, face_mode = context.scene.tool_settings.mesh_select_mode
        return ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH' and edge_mode ^ face_mode

    def invoke(self, context, event):
        print(__name__, 'invoke')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        print(__name__, 'modal')
        return {'FINISHED'}

    def execute(self, context):
        print(__name__, 'exec')
        return {'FINISHED'}


class ExtrudeManipulator(bpy.types.GizmoGroup):

    bl_idname =  'angle_extrude.manipulator'
    bl_label = 'extrude_manipulator'
    bl_space_type = "VIEW_3D"
    bl_options = {'3D', 'PERSISTENT'}
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        print(f'Active operator defined: {wm.operators is not None}')
        if wm.operators:
            print(f'Active operator name: {wm.operators[-1].bl_idname}')
        can_poll = len(wm.operators) > 0 and isinstance(wm.operators[-1], AngleExtrudeOp)
        print(f'gizmo can: {can_poll}')
        return can_poll

    def setup(self, context):
        print(__name__, 'setup')
        self._distance_gz = self.gizmos.new('GIZMO_GT_arrow_3d')
        # self._distance_gz.target_set_operator(AngleExtrudeOp.bl_idname).axis = 'Z'
        self._distance_gz.use_draw_modal = True
        self._x_axis_gz = self.gizmos.new('GIZMO_GT_dial_3d')
        self._y_axis_gz = self.gizmos.new('GIZMO_GT_dial_3d')

    def refresh(self, context):
        pass


def add_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator_context = 'INVOKE_DEFAULT'
    layout.operator(AngleExtrudeOp.bl_idname)


def register():
    bpy.utils.register_class(AngleExtrudeOp)
    bpy.utils.register_class(ExtrudeManipulator)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(add_menu)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(add_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(add_menu)


def unregister():
    bpy.utils.unregister_class(ExtrudeManipulator)
    bpy.utils.unregister_class(AngleExtrudeOp)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(add_menu)


if __name__ == '__main__':
    register()

