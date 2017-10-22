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


## PROPERTIES ##
################


class CustomToolsImageProperties(bpy.types.PropertyGroup):
    
    bpy.types.Scene.custom_tools_filepath_apply = bpy.props.EnumProperty(
        name='Apply',
        items=(
            ('CURRENT', 'Current', 'Current image'),
            ('ALL', 'All', 'All images')
            ),
        )
    
    bpy.types.Scene.custom_tools_find = bpy.props.StringProperty(
        name='Find',
        description='Find text',
        default=''
        )
    
    bpy.types.Scene.custom_tools_replace = bpy.props.StringProperty(
        name='Replace',
        description='Replace text',
        default=''
        )


## PANEL ##
###########


class ImageEditorCustomPanelFilepath(bpy.types.Panel):
    bl_label = 'Filepath'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene, 'custom_tools_filepath_apply')
        layout.prop(context.scene, 'custom_tools_find')
        layout.prop(context.scene, 'custom_tools_replace')
        
        layout.operator('scene.customtools_swap_search_and_replace')
        layout.operator('scene.customtools_filepath_search_and_replace')


class NodeEditorCustomPanelFilepath(bpy.types.Panel):
    bl_label = 'Filepath'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree')
    
    def draw(self, context):
        layout = self.layout
        
        selected_nodes = context.selected_nodes
        for node in selected_nodes:
            if node.type == 'IMAGE':
                image = node.image
                layout.label(image.filepath)
        
        layout.prop(context.scene, 'custom_tools_find')
        layout.prop(context.scene, 'custom_tools_replace')
        
        layout.operator('scene.customtools_swap_search_and_replace')
        layout.operator('scene.customtools_filepath_search_and_replace_nodes')


## OPERATOR ##
##############


class CustomToolsFilepathSearchAndReplace(bpy.types.Operator):
    bl_idname = 'scene.customtools_filepath_search_and_replace'
    bl_label = 'Search and replace'
    bl_description = 'Replace filepath'
    
    @classmethod
    def poll(cls, context):
        if context.scene.custom_tools_filepath_apply == 'ALL':
            return (True)
        else:
            return (context.space_data.image) 
    
    def execute(self, context):
        
        find = context.scene.custom_tools_find
        replace = context.scene.custom_tools_replace
        
        if context.scene.custom_tools_filepath_apply == 'ALL':
            for image in bpy.data.images:
                if image.filepath:
                    image.filepath = image.filepath.replace(find, replace)
                    
        elif context.scene.custom_tools_filepath_apply == 'CURRENT':
            current_image = context.space_data.image
            current_image.filepath = current_image.filepath.replace(find, replace)
        
        return{'FINISHED'}


class CustomToolsFilepathSearchAndReplaceNodes(bpy.types.Operator):
    bl_idname = 'scene.customtools_filepath_search_and_replace_nodes'
    bl_label = 'Search and replace'
    bl_description = 'Replace filepath'
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree')
    
    def execute(self, context):
        
        find = context.scene.custom_tools_find
        replace = context.scene.custom_tools_replace
        
        selected_nodes = context.selected_nodes
        active_node = context.active_node
        
        for node in selected_nodes:
            if node.type == 'IMAGE':
                image = node.image
                image.filepath = image.filepath.replace(find, replace)
        
        return{'FINISHED'}


class CustomToolsSwapSearchAndReplace(bpy.types.Operator):
    bl_idname = 'scene.customtools_swap_search_and_replace'
    bl_label = 'Swap'
    bl_description = 'Swap Find and replace text'
    
    def execute(self, context):
        
        find = context.scene.custom_tools_find
        replace = context.scene.custom_tools_replace
        
        context.scene.custom_tools_find = replace
        context.scene.custom_tools_replace = find
        
        return{'FINISHED'}

