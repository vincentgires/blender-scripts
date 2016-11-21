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


import bpy, mathutils
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.functions import send_value


class ColorCombine(Node):
    
    '''Color Split node'''
    bl_idname = 'ColorCombineNodeType'
    bl_label = 'Color Combine'
    
    
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'R')
        self.inputs.new('NodeSocketFloat', 'G')
        self.inputs.new('NodeSocketFloat', 'B')
        self.inputs.new('NodeSocketFloat', 'A')
        self.outputs.new('NodeSocketColor', "Color")
    
    
    def update(self):
        if len(self.inputs) >= 4:
            
            color = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
            color[0] = self.inputs[0].default_value
            color[1] = self.inputs[1].default_value
            color[2] = self.inputs[2].default_value
            color[3] = self.inputs[3].default_value
            """
            color = self.outputs["Color"].default_value
            color[0] = self.inputs[0].default_value
            color[1] = self.inputs[1].default_value
            color[2] = self.inputs[2].default_value
            color[3] = self.inputs[3].default_value
            """
            # send data value to connected nodes
            send_value(self.outputs, color)
            
                    
        
    
                 
    """# Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        pass
    
    # Detail buttons in the sidebar.
    def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Color Combine"








def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")