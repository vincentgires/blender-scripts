import bpy


class PoseToEmpty(bpy.types.Operator):
    bl_idname = 'scene.pose_to_empty'
    bl_label = 'Pose To Empty'

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

        empty_object = bpy.data.objects.new('Empty', None)
        context.scene.collection.objects.link(empty_object)
        empty_object.location = empty_location
        empty_object.rotation_euler = bone_rotation

        return {'FINISHED'}
