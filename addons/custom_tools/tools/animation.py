# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Author : Vincent Gires
# www.vincentgires.com


import bpy


## PANEL ##
###########


class View3dCustomPanelAnimation(bpy.types.Panel):
    bl_label = 'Animation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label('Pose')
        col.operator('scene.customtools_reset_pose')
        col.operator('scene.customtools_pose_to_empty')
        
        col = layout.column(align=True)
        col.label('Action')
        row = col.row(align=True)
        row.operator('scene.customtools_set_actions_fake')
        row.operator('scene.customtools_remove_actions_fake')
        col.operator('scene.customtools_delete_actions')
        

## OPERATOR ##
##############


class CustomToolsResetPose(bpy.types.Operator):
    bl_idname = 'scene.customtools_reset_pose'
    bl_label = 'Reset pose'
    bl_description = 'Reset location/rotation/scale properties'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'POSE')
    
    def execute(self, context):
        for pose_bone in context.selected_pose_bones:
            pose_bone.location = (0.0, 0.0, 0.0)
            pose_bone.rotation_euler = (0.0, 0.0, 0.0)
            pose_bone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            pose_bone.rotation_axis_angle = (1.0, 0.0, 0.0, 0.0)
            pose_bone.scale = (1.0, 1.0, 1.0)
        
        return{'FINISHED'}


class CustomToolsSetActionsFake(bpy.types.Operator):
    bl_idname = 'scene.customtools_set_actions_fake'
    bl_label = 'Fake actions'
    
    def execute(self, context):
        for action in bpy.data.actions:
            action.use_fake_user = True
        
        return{'FINISHED'}


class CustomToolsRemoveActionsFake(bpy.types.Operator):
    bl_idname = 'scene.customtools_remove_actions_fake'
    bl_label = 'Free actions'
    
    def execute(self, context):
        for action in bpy.data.actions:
            action.use_fake_user = False
        
        return{'FINISHED'}


class CustomToolsDeleteActions(bpy.types.Operator):
    bl_idname = 'scene.customtools_delete_actions'
    bl_label = 'Delete actions'
    bl_description = 'Delete actions with no users'
    
    def execute(self, context):
        for action in bpy.data.actions:
            if action.users == 0:
                bpy.data.actions.remove(action)
        
        return{'FINISHED'}


class CustomToolsPoseToEmpty(bpy.types.Operator):
    bl_idname = 'scene.customtools_pose_to_empty'
    bl_label = 'Pose to empty'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'POSE')
    
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

