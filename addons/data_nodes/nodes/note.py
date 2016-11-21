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


class NoteNode(Node):

    '''Note node'''
    bl_idname = 'NoteNodeType'
    bl_label = 'Note'
    
    
    # === Callbacks ===
    def update_attribute(self, context):
        self.update()   
    
    # === Custom Properties ===
    note_prop = bpy.props.StringProperty(name = "Note", update=update_attribute)

    def init(self, context):
        self.outputs.new('NodeSocketString', "String")
    
    
    def update(self):
        
        # send data value to connected nodes
        send_value(self.outputs, self.note_prop)

    
    def draw_buttons(self, context, layout):
        layout.prop(self, "note_prop", text="")
    
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "note_prop")
        
    def draw_label(self):
        return "Note"






def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
