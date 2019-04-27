import bpy


class DeleteActions(bpy.types.Operator):
    bl_idname = 'scene.customtools_delete_actions'
    bl_label = 'Delete actions'
    bl_description = 'Delete actions with no users'

    def execute(self, context):
        for action in bpy.data.actions:
            if not action.users:
                bpy.data.actions.remove(action)
        return{'FINISHED'}


class PoseToEmpty(bpy.types.Operator):
    bl_idname = 'scene.customtools_pose_to_empty'
    bl_label = 'Pose to empty'

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.mode == 'POSE'

    def execute(self, context):
        active_armature = context.active_object
        active_bone = context.active_pose_bone

        matrix = active_bone.matrix
        bone_rotation = matrix.to_euler()
        bone_location = matrix.translation
        object_location = active_armature.matrix_world.translation
        empty_location = bone_location + object_location

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.empty_add(
            type='PLAIN_AXES',
            radius=1,
            view_align=False,
            location=empty_location,
            rotation=bone_rotation)

        empty = context.object
        empty.select = False
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.objects.active = active_armature
        active_armature.select = True
        bpy.ops.object.mode_set(mode='POSE')

        return{'FINISHED'}
