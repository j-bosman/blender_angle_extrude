import bpy
import bmesh

from mathutils import Vector


class AngleExtrudeOp(bpy.types.Operator):

    bl_idname = "mesh.angle_extrude"
    bl_label = "Angle extrude"
    bl_space_type = "VIEW_3D"
    bl_options = {'REGISTER', 'UNDO'}

    distance: bpy.props.FloatProperty('distance', default=0.0, options={'HIDDEN'})
    angle_x: bpy.props.FloatProperty('angle_x', default=0.0, options={'HIDDEN'})
    angle_y: bpy.props.FloatProperty('angle_y', default=0.0, options={'HIDDEN'})
    center: bpy.props.FloatVectorProperty('center', size=3, default=(.0, .0, .0), options={'HIDDEN'})

    _OP_PROP_NAME = 'angle_extrude_op'

    @staticmethod
    def _get_selected(items):
        """
        Returns selected primitives.

        :param items: items being queried.
        :type items: Iterable[Union[BMVert, BMEdge, BMFace]]
        :return: the selected primitives.
        :rtype: Iterable[Union[BMVert, BMEdge, BMFace]]
        """
        return list(filter(lambda item: item.select, items))

    @classmethod
    def poll(cls, context):
        # print('polling')
        ob = context.active_object
        _, edge_mode, face_mode = context.scene.tool_settings.mesh_select_mode
        return ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH' and edge_mode ^ face_mode

    def invoke(self, context, event):
        print(__name__, 'invoke')
        bpy.types.Scene.angle_extrude_op = bpy.props.PointerProperty(type=bpy.types.Object,
                                                                     name=AngleExtrudeOp._OP_PROP_NAME)
        bpy.types.Scene.angle_extrude_op = self

        wm = context.window_manager
        wm.gizmo_group_type_ensure(ExtrudeManipulator.bl_idname)

        context.window_manager.modal_handler_add(self)
        self._bm = bmesh.from_edit_mesh(context.active_object.data)

        selected_vtx = AngleExtrudeOp._get_selected(self._bm.verts)
        self.center = sum([v.co for v in selected_vtx], start=Vector([0.0]*3)) / len(selected_vtx)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        print(__name__, 'modal')

        if event.type == 'ESC' and event.value == 'RELEASE':
            wm = context.window_manager
            wm.gizmo_group_type_unlink_delayed(ExtrudeManipulator.bl_idname)

            if hasattr(bpy.types.Scene, AngleExtrudeOp._OP_PROP_NAME):
                del bpy.types.Scene.angle_extrude_op
            return {'FINISHED'}

        if event.type == 'SPACE' and event.value == 'RELEASE':
            # start a new segment
            pass

        return {'PASS_THROUGH'}

    def execute(self, context):
        print('AngleExtrudeOp.execute()')
        return {'FINISHED'}


class ExtrudeManipulator(bpy.types.GizmoGroup):

    bl_idname = 'angle_extrude.manipulator'
    bl_label = 'extrude_manipulator'
    bl_space_type = "VIEW_3D"
    bl_options = {'3D'}
    bl_region_type = 'WINDOW'

    @staticmethod
    def get_operator(context):
        if hasattr(bpy.types.Scene, 'angle_extrude_op'):
            return context.Scene.angle_extrude_op

        return None

    @classmethod
    def poll(cls, context):
        op = getattr(bpy.types.Scene, 'angle_extrude_op', None)
        print(f'gizmo can: {op is not None}')
        if op is None:
            wm = context.window_manager
            wm.gizmo_group_type_ensure(cls.bl_idname)
            return False
        return True

    def setup(self, context):
        print(__name__, 'setup')
        self._distance_gz = self.gizmos.new('GIZMO_GT_arrow_3d')

        def get_distance():
            op = getattr(bpy.types.Scene, 'angle_extrude_op', None)
            return op.distance

        def set_distance(value):
            op = getattr(bpy.types.Scene, 'angle_extrude_op', None)
            op.distance = value
            op.execute(context)

        self._distance_gz.target_set_handler('offset', get=get_distance, set=set_distance)
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

