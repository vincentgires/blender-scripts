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


class Vector(Node):
    
    '''Vector node'''
    bl_idname = 'VectorNodeType'
    bl_label = 'Vector'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'X')
        self.inputs.new('NodeSocketFloat', 'Y')
        self.inputs.new('NodeSocketFloat', 'Z')
        self.outputs.new('NodeSocketVector', "Vector")
    
    
    def update(self):
        
        if len(self.inputs) >= 3:
            # send data value to connected nodes
            x = self.inputs["X"].default_value
            y = self.inputs["Y"].default_value
            z = self.inputs["Z"].default_value
            vector = mathutils.Vector((x,y,z))
            
            # assign value to connected socket
            send_value(self.outputs, vector)
                    
        
    
                 
    # Additional buttons displayed on the node.
    #def draw_buttons(self, context, layout):
    #    pass
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Vector"








def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")