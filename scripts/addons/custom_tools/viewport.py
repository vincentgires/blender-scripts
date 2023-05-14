import bpy
import mathutils
import math
from bpy_extras import view3d_utils


def aim_normal(context, event, active_object, ray_max=1000.0, offset=-1):
    """Run this function on left mouse, execute the ray cast"""

    # scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + (view_vector * ray_max)

    def visible_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""

        for obj in context.visible_objects:
            if obj.type == 'MESH':
                yield (obj, obj.matrix_world.copy())

            # TODO: update it for recent Blender API
            # if obj.dupli_type != 'NONE':
            #     obj.dupli_list_create(scene)
            #     for dob in obj.dupli_list:
            #         obj_dupli = dob.object
            #         if obj_dupli.type == 'MESH':
            #             yield (obj_dupli, dob.matrix.copy())
            # obj.dupli_list_clear()

    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv @ ray_origin
        ray_target_obj = matrix_inv @ ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj
        '''# cast the ray
        hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)

        if face_index != -1:
            return hit, normal, face_index
        else:
            return None, None, None'''
        # cast the ray
        success, location, normal, face_index = obj.ray_cast(
            ray_origin_obj, ray_direction_obj)

        if success:
            return location, normal, face_index
        else:
            return None, None, None

    # cast rays and find the closest object
    # best_length_squared = ray_max * ray_max
    best_length_squared = -1.0
    best_obj = None

    for obj, matrix in visible_objects_and_duplis():

        if obj.type != 'MESH':
            continue

        hit, normal, face_index = obj_ray_cast(obj, matrix)
        if not hit:
            continue

        hit_world = matrix @ hit
        length_squared = (hit_world - ray_origin).length_squared
        if not best_obj or length_squared < best_length_squared:
            best_length_squared = length_squared
            best_obj = obj

            origin_scale = active_object.scale.copy()

            # apply target local coordinate
            normal = best_obj.matrix_world.to_3x3() @ normal
            normal = normal * -1
            normal = normal.copy()

            # rotation
            vect_x = 1
            vect_y = 1
            vect_z = 1

            y_vect_x = (normal.y * vect_z) - (normal.z * vect_y)
            y_vect_y = (normal.z * vect_x) - (normal.x * vect_z)
            y_vect_z = (normal.x * vect_y) - (normal.y * vect_x)

            x_vect_x = (normal.y * y_vect_z) - (normal.z * y_vect_y)
            x_vect_y = (normal.z * y_vect_x) - (normal.x * y_vect_z)
            x_vect_z = (normal.x * y_vect_y) - (normal.y * y_vect_x)

            y_vect_normalize = math.sqrt(
                (y_vect_x * y_vect_x)
                + (y_vect_y * y_vect_y)
                + (y_vect_z * y_vect_z))
            x_vect_normalize = math.sqrt(
                (x_vect_x * x_vect_x)
                + (x_vect_y * x_vect_y)
                + (x_vect_z * x_vect_z))

            matrix = mathutils.Matrix().to_3x3()
            matrix.row[0] = (
                (x_vect_x / x_vect_normalize,
                 y_vect_x / y_vect_normalize,
                 normal.x))
            matrix.row[1] = (
                (x_vect_y / x_vect_normalize,
                 y_vect_y / y_vect_normalize,
                 normal.y))
            matrix.row[2] = (
                (x_vect_z / x_vect_normalize,
                 y_vect_z / y_vect_normalize,
                 normal.z))

            active_object.matrix_world = matrix.to_4x4()

            # position
            active_object.location = hit_world
            for i in range(0, 3):
                active_object.location[i] = active_object.location[i] \
                    + (offset * normal[i])

            # scale
            active_object.scale = origin_scale


class AimNormal(bpy.types.Operator):
    bl_idname = 'scene.aim_normal'
    bl_label = 'Aim Normal'

    @classmethod
    def poll(cls, context):
        return context.object

    def modal(self, context, event):

        w = context.window_manager.windows[0]
        w.cursor_modal_set('CROSSHAIR')

        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            aim_normal(context, event, context.object, offset=self.offset)
            self.set_header(context, self.offset)

        elif event.type == 'WHEELUPMOUSE':
            self.offset += 0.5
            aim_normal(context, event, context.object, offset=self.offset)
            self.set_header(context, self.offset)

        elif event.type == 'WHEELDOWNMOUSE':
            self.offset -= 0.5
            aim_normal(context, event, context.object, offset=self.offset)
            self.set_header(context, self.offset)

        elif event.type in ('LEFTMOUSE', 'RET', 'NUMPAD_ENTER'):
            w.cursor_modal_restore()
            return {'FINISHED'}

        elif event.type in ('RIGHTMOUSE', 'ESC'):
            context.object.matrix_world = self.matrix_save
            w.cursor_modal_restore()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.matrix_save = context.object.matrix_world.copy()
        self.offset = -5
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'},
                        'VIEW_3D Editor not found, cannot run operator')
            return {'CANCELLED'}

    def set_header(self, context, offset):
        context.area.header_text_set(
            text=('Aim tool | '
                  'Move the mouse to align to the normal | '
                  'Offset with Wheel Up-Down : {}').format(offset))


class LookThroughSelected(bpy.types.Operator):
    bl_idname = 'scene.look_through_selected'
    bl_label = 'Look Through Selected'
    bl_description = 'Look Through Selected'

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        context.space_data.use_local_camera = True
        context.space_data.camera = context.object
        bpy.ops.view3d.view_camera()
        return {'FINISHED'}
