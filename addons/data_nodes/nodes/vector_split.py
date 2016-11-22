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
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.functions import send_value_link


class VectorSplit(Node):
    
    '''Vector Split node'''
    bl_idname = 'VectorSplitNodeType'
    bl_label = 'Vector Split'
    
    
    def init(self, context):
        self.inputs.new('NodeSocketVector', "Vector")
        self.outputs.new('NodeSocketFloat', 'X')
        self.outputs.new('NodeSocketFloat', 'Y')
        self.outputs.new('NodeSocketFloat', 'Z')
    
    
    def update(self):
        
        # send data value to connected nodes
        for output in self.outputs:
            for link in output.links:
                if output.name == "X":
                    send_value_link(link, self.inputs["Vector"].default_value[0])
                elif output.name == "Y":
                    send_value_link(link, self.inputs["Vector"].default_value[1])
                elif output.name == "Z":
                    send_value_link(link, self.inputs["Vector"].default_value[2])
                    
        
    
                 
    # Additional buttons displayed on the node.
    #def draw_buttons(self, context, layout):
    #    pass
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Vector Split"


