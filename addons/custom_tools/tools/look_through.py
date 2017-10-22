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


class View3dCustomPanelLookThrough(bpy.types.Panel):
    bl_label = 'Look Through'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.space_data, 'lock_camera', 'Lock to view')
        
        layout.operator('scene.customtools_look_through_selected')
        layout.operator('scene.customtools_look_through_render')
        
        layout.operator('scene.customtools_set_active_camera', icon='CAMERA_DATA')
        layout.operator('scene.customtools_remove_local_camera')
        
        row = layout.row(align=False)
        row.alignment = 'EXPAND'
        row.operator('scene.customtools_layers_to_view')
        row.operator('scene.customtools_view_to_layers')
        

class CustomToolsLookThroughSelected(bpy.types.Operator):
    bl_idname = 'scene.customtools_look_through_selected'
    bl_label = 'Look through selected'
    bl_description = 'Look Through selected light, camera or object'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        context.space_data.lock_camera_and_layers = False # needs to be False to active local camera
        
        active_scene = context.scene
        active_camera = context.scene.camera
        active_object = context.active_object
        
        bpy.ops.view3d.object_as_camera()
        context.scene.camera = active_camera # restore render camera
        
        return{'FINISHED'}


class CustomToolsLookThroughRender(bpy.types.Operator):
    bl_idname = 'scene.customtools_look_through_render'
    bl_label = 'Look through render'
    bl_description = 'Look Through render camera, could be different than the local camera'
    
    def execute(self, context):
        active_scene = bpy.context.scene
        active_camera = bpy.context.scene.camera
        context.space_data.camera = active_camera
        bpy.ops.view3d.viewnumpad(type='CAMERA')
        
        return{'FINISHED'}


class CustomToolsSetActiveCamera(bpy.types.Operator):
    bl_idname = 'scene.customtools_set_active_camera'
    bl_label = 'Set active camera'
    bl_description = 'Set selected to active camera for the rendering'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        
        active_object = context.active_object
        if context.space_data.type == 'VIEW_3D':
            store_lock_context = context.space_data.lock_camera_and_layers
        
        # unlock all camera and layers to avoid to change view if the render cam is set
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='VIEW_3D':
                        space.lock_camera_and_layers = False
        
        
        if context.space_data.type == 'VIEW_3D':
            context.space_data.lock_camera_and_layers = True # needs to be True to set the render camera... (?) by bpy.ops.view3d.object_as_camera() or bpy.context.scene.camera = active_object
        
        context.scene.camera = active_object
        
        if context.space_data.type == 'VIEW_3D':
            context.space_data.lock_camera_and_layers = store_lock_context # reset lock camera and layers like it was before the script
        
        return{'FINISHED'}


class CustomToolsLayersToView(bpy.types.Operator):
    bl_idname = 'scene.customtools_layers_to_view'
    bl_label = 'Layers to view'
    bl_description = 'Set visible layers from render visible layers'

    def execute(self, context):
        layer_cpt = 0
        for layer in context.scene.layers:
            context.space_data.layers[layer_cpt] = layer
            layer_cpt += 1
        
        return{'FINISHED'}


class CustomToolsViewToLayers(bpy.types.Operator):
    bl_idname = 'scene.customtools_view_to_layers'
    bl_label = 'View to layers'
    bl_description = 'Set visible layers to render visible layers'
    
    def execute(self, context):
        layer_cpt = 0
        for layer in context.space_data.layers:
            context.scene.layers[layer_cpt] = layer
            layer_cpt += 1
        
        return{'FINISHED'}


class CustomToolsRemoveLocalCamera(bpy.types.Operator):
    bl_idname = 'scene.customtools_remove_local_camera'
    bl_label = 'Remove local camera'
    bl_description = 'Remove local camera in the viewer'
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.camera is not None)
    
    def execute(self, context):
        context.space_data.camera = None
        return{'FINISHED'}

