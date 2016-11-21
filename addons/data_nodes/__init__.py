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
from bpy.app.handlers import persistent
from bpy.types import NodeTree, Node, NodeSocket



bl_info = {
    "name": "Data Nodes",
    "author": "Vincent Gires",
    "description": "Node utils for Cycles, the compositor and a custom Data Node Tree",
    "version": (0, 0, 2),
    "blender": (2, 7, 7),
    "location": "Node Editor",
    "warning": "",
    "wiki_url": "",
    "category": "Node"}


#########
#### TODO

'''

- /!\ pas oublier de retirer les bpy.app.handlers clear du script dans register
- connecter un output vector vers un value math node par exemple > bug. Checker le type?
    (ne pas permettre de le connecter?)
    (convertir vector to color / value r ou moyenne?)
- simplifier le code avec une methode get_object()?

'''


# NODES
from data_nodes.nodes import bool
from data_nodes.nodes import color_combine
from data_nodes.nodes import color_palette
from data_nodes.nodes import color_split
from data_nodes.nodes import color
from data_nodes.nodes import condition
from data_nodes.nodes import data_input
from data_nodes.nodes import data_output
from data_nodes.nodes import debug
from data_nodes.nodes import distance
from data_nodes.nodes import expression
from data_nodes.nodes import float_switch
from data_nodes.nodes import float_to_int
from data_nodes.nodes import float_to_string
from data_nodes.nodes import float
from data_nodes.nodes import int
from data_nodes.nodes import int_to_float
from data_nodes.nodes import note
from data_nodes.nodes import object_properties
from data_nodes.nodes import renderLayer
from data_nodes.nodes import render
from data_nodes.nodes import round
from data_nodes.nodes import time
from data_nodes.nodes import vector_split
from data_nodes.nodes import vector

# OPERATORS
from data_nodes import operators

# FUNCTIONS
from data_nodes.functions import *


## CUSTOM PROPERTIES ##
#######################
"""
class NODE_UTILS_properties(bpy.types.PropertyGroup):
    
    bpy.types.Scene.auto_update_scene = bpy.props.BoolProperty(
        name = "Auto update scene",
        description = "",
        default = 0,
    )
"""

class ColorPalette_ColorProperty(bpy.types.PropertyGroup):
    color = bpy.props.FloatVectorProperty(
                                            name = "Color",
                                            subtype = "COLOR",
                                            size = 4, # 4 = RGBA
                                            soft_min=0.0, soft_max=1.0,
                                            default = (0.5,0.5,0.5,1.0)
                                        )

# Color palette collection
class ColorPalette_collectionProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Color Palette name", default="Palette"),
    colorCollection = bpy.props.CollectionProperty(type=ColorPalette_ColorProperty)

## NODE TREE ##
###############

class NODE_EDITOR_data_tree(NodeTree):
    bl_idname = 'DataNodeTree'
    bl_label = 'Data Node Tree'
    bl_icon = 'NODETREE'
    
    


## PANEL ##
###########

class NODE_EDITOR_custom_nodes_panel(bpy.types.Panel):
    bl_label = "Tools"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Custom"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def draw(self, context):
        layout = self.layout
        layout.operator("update_custom_node.btn", icon="FILE_REFRESH")




### Node Categories ###

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class CustomNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree


# all categories in a list
node_categories = [
    # identifier, label, items list
    CustomNodeCategory("CUSTOM", "Custom", items=[
        # custom nodes
        NodeItem("ColorCombineNodeType"),
        NodeItem("BoolNodeType"),
        NodeItem("ColorPaletteNodeType"),
        NodeItem("ColorSplitNodeType"),
        NodeItem("ColorNodeType"),
        NodeItem("ConditionNodeType"),
        NodeItem("DataInputNodeType"),
        NodeItem("DataOutputNodeType"),
        NodeItem("DebugNodeType"),
        NodeItem("ExpressionNodeType"),
        NodeItem("DistanceNodeType"),
        NodeItem("FloatSwitchNodeType"),
        NodeItem("FloatToIntNodeType"),
        NodeItem("FloatToStringNodeType"),
        NodeItem("FloatNodeType"),
        NodeItem("IntNodeType"),
        NodeItem("IntToFloatNodeType"),
        NodeItem("NoteNodeType"),
        NodeItem("ObjectPropertiesNodeType"),
        NodeItem("RenderNodeType"),
        NodeItem("RenderLayersNodeType"),
        NodeItem("RoundNodeType"),
        NodeItem("TimeNodeType"),
        NodeItem("VectorSplitNodeType"),
        NodeItem("VectorNodeType"),
        ]),
    ]







def register():
    bpy.utils.register_module(__name__)
    
    try:
        nodeitems_utils.register_node_categories("NODE_UTILS", node_categories)
    except:
        pass

    bpy.types.Scene.ColorPalette_collection = \
        bpy.props.CollectionProperty(type=ColorPalette_collectionProperty)
    
    '''bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.render_pre.clear()
    bpy.app.handlers.render_post.clear()'''
    
    bpy.app.handlers.frame_change_post.append(frame_change)
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.app.handlers.render_pre.append(render_pre_update)
    bpy.app.handlers.render_post.append(render_post_update)
    
    

def unregister():
    
    bpy.utils.unregister_module(__name__)
    nodeitems_utils.unregister_node_categories("NODE_UTILS")
    del bpy.types.Scene.ColorPalette_collection
    
    bpy.app.handlers.frame_change_post.remove(frame_change)
    bpy.app.handlers.scene_update_post.remove(scene_update)
    bpy.app.handlers.render_pre.remove(render_pre_update)
    bpy.app.handlers.render_post.remove(render_post_update)

if __name__ == "__main__":
    register()


print ("---")
