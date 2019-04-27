import bpy


class LookThroughSelected(bpy.types.Operator):
    bl_idname = 'scene.look_through_selected'
    bl_label = 'Look through selected'
    bl_description = 'Look Through selected light, camera or object'

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        context.space_data.lock_camera_and_layers = False  # Needs to be False
        # to active local camera
        bpy.ops.view3d.object_as_camera()
        context.scene.camera = active_camera  # restore render camera
        return{'FINISHED'}


class LookThroughRender(bpy.types.Operator):
    bl_idname = 'scene.look_through_render'
    bl_label = 'Look through render'
    bl_description = (
        'Look Through render camera, could be different than the local camera')

    def execute(self, context):
        active_camera = bpy.context.scene.camera
        context.space_data.camera = active_camera
        bpy.ops.view3d.viewnumpad(type='CAMERA')
        return{'FINISHED'}
