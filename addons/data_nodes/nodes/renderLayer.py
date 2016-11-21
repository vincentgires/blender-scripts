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


class RenderLayersNode(Node):
    
    '''Render Layers'''
    bl_idname = 'RenderLayersNodeType'
    bl_label = 'Render Layers'
    
    def renderlayers_enum(self,context):
        items = [(layer.name, layer.name, "") for layer in bpy.context.scene.render.layers]
        return items

    # === Custom Properties ===
    render_layers = bpy.props.EnumProperty(items = renderlayers_enum, name = "Layer")

    # === Optional Functions ===
    def init(self, context):
        self.outputs.new('NodeSocketFloat', "is_active")
     
    def update(self):
        
        for output in self.outputs:
            if output.name == "is_active":
                if self.render_layers == bpy.context.scene.render.layers.active.name:
                    send_value(self.outputs, 1)
                else:
                    send_value(self.outputs, 0)
     
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "render_layers")

    def draw_label(self):
        return "Render Layers"







def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
