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
from data_nodes.functions import send_value



class Int(Node):
    
    '''Float node'''
    bl_idname = 'IntNodeType'
    bl_label = 'Int'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    int_prop = bpy.props.IntProperty(name = "Int", default = 1, update = update_props)
    
    
    def init(self, context):
        self.outputs.new('NodeSocketInt', "Int")
    
    
    def update(self):
        
        # send data value to connected nodes
        send_value(self.outputs, self.int_prop)
                    
                    
        
    
                 
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "int_prop")
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Int"


