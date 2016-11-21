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


class Color(Node):
    
    '''Color node'''
    bl_idname = 'ColorNodeType'
    bl_label = 'Color'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    color_prop = bpy.props.FloatVectorProperty(name = "Color",
                                                                subtype = "COLOR",
                                                                size = 4, # 4 = RGBA
                                                                soft_min=0.0, soft_max=1.0,
                                                                default = (1,1,1,1),
                                                                update = update_props)
    
    
    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color")
    
    
    def update(self):
        
        # send data value to connected nodes
        send_value(self.outputs, self.color_prop)
                    
        
    
                 
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "color_prop")
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Color"








def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")