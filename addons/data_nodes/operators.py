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


import bpy
import math, mathutils

# FUNCTIONS
from data_nodes.functions import *


## OPERATOR ##
##############


class custom_nodes_update(bpy.types.Operator):
    bl_idname = "update_custom_node.btn"
    bl_label = "Update nodes"
    bl_description = "Force update custom nodes"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        
        selected_nodes = context.selected_nodes
        active_node = context.active_node
        
        update_nodes(context.scene)
        
        return{'FINISHED'}


class custom_nodes_get_object(bpy.types.Operator):
    bl_idname = "get_object_to_custom_node.btn"
    bl_label = "Get object"
    bl_description = "Get selected object from scene"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        node = context.node
        selected_object = context.object
        
        node.data_item = selected_object.name
        
        return{'FINISHED'}


class custom_nodes_remove_input_sockets(bpy.types.Operator):
    bl_idname = "remove_input_sockets.btn"
    bl_label = "Remove input sockets"
    bl_description = "Remove input sockets"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and node.inputs
    
    def execute(self, context):
        node = context.node
        selected_object = context.object
        
        node.inputs.clear()
            
        return{'FINISHED'}
    
class custom_nodes_remove_output_sockets(bpy.types.Operator):
    bl_idname = "remove_output_sockets.btn"
    bl_label = "Remove output sockets"
    bl_description = "Remove output sockets"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and node.outputs
    
    def execute(self, context):
        node = context.node
        selected_object = context.object
        
        node.outputs.clear()
            
        return{'FINISHED'}


class custom_nodes_add_output_socket(bpy.types.Operator):
    bl_idname = "add_output_socket_to_custom_node.btn"
    bl_label = "Add output socket"
    bl_description = "Add output socket to the node"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and context.node.attributeProperty
    
    def execute(self, context):
        node = context.node
        selected_object = context.object
        
        # get attribute value and type
        data_path = "bpy.data."+node.data_enum + "['"+node.data_item+"']"
        data_path = eval(data_path)
        try:
            attribute = eval("data_path"+"."+node.attributeProperty)
        except:
            attribute = None
        
        if attribute is not None:
            
            if isinstance(attribute, str):
                node.outputs.new('NodeSocketString', node.attributeProperty)
                
            elif isinstance(attribute, bool):
                node.outputs.new('NodeSocketBool', node.attributeProperty)
                
            elif isinstance(attribute, int):
                node.outputs.new('NodeSocketInt', node.attributeProperty)
                
            elif isinstance(attribute, float):
                node.outputs.new('NodeSocketFloat', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Color):
                node.outputs.new('NodeSocketColor', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Vector):
                node.outputs.new('NodeSocketVector', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Euler):
                node.outputs.new('NodeSocketVector', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Quaternion):
                node.outputs.new('NodeSocketVector', node.attributeProperty)
                
            elif len(attribute) == 4: # RGBA
                node.outputs.new('NodeSocketColor', node.attributeProperty)
                
        return{'FINISHED'}



class custom_nodes_add_input_socket(bpy.types.Operator):
    bl_idname = "add_input_socket_to_custom_node.btn"
    bl_label = "Add input socket"
    bl_description = "Add input socket to the node"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and context.node.attributeProperty
    
    def execute(self, context):
        node = context.node
        selected_object = context.object
        
        # get attribute value and type
        data_path = "bpy.data."+node.data_enum + "['"+node.data_item+"']"
        data_path = eval(data_path)
        try:
            attribute = eval("data_path"+"."+node.attributeProperty)
        except:
            attribute = None
        
        if attribute is not None:
            
            if isinstance(attribute, str):
                node.inputs.new('NodeSocketString', node.attributeProperty)
                
            elif isinstance(attribute, bool):
                node.inputs.new('NodeSocketBool', node.attributeProperty)
                
            elif isinstance(attribute, int):
                node.inputs.new('NodeSocketInt', node.attributeProperty)
                
            elif isinstance(attribute, float):
                node.inputs.new('NodeSocketFloat', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Color):
                node.inputs.new('NodeSocketColor', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Vector):
                node.inputs.new('NodeSocketVector', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Euler):
                node.inputs.new('NodeSocketVector', node.attributeProperty)
                
            elif isinstance(attribute, mathutils.Quaternion):
                node.inputs.new('NodeSocketVector', node.attributeProperty)
                
            elif len(attribute) == 4: # RGBA
                node.inputs.new('NodeSocketColor', node.attributeProperty)
            
        return{'FINISHED'}
    
    
