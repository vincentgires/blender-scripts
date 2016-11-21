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



class Float(Node):
    
    '''Float node'''
    bl_idname = 'FloatNodeType'
    bl_label = 'Float'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    float_prop = bpy.props.FloatProperty(name = "Float", default = 1.0, update = update_props)
    
    
    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Float")
    
    
    def update(self):
        
        # send data value to connected nodes
        send_value(self.outputs, self.float_prop)
                    
                    
        
    
                 
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "float_prop")
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Float"








def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")