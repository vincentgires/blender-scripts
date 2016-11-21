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
from bpy.app.handlers import persistent
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.functions import send_value


class RenderNode(Node):
    
    '''Render'''
    bl_idname = 'RenderNodeType'
    bl_label = 'Render'
    
    on_render = bpy.props.FloatProperty(name = "On Render", default = 0)
    
    def init(self, context):
        self.outputs.new('NodeSocketFloat', "on_render")
     
    def update(self):
        send_value(self.outputs, self.on_render)
     
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        pass

    def draw_label(self):
        return "Render"





def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
