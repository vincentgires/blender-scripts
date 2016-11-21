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
import math
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.functions import send_value

data_items = (
        ('actions', 'actions', ''),
        ('armatures', 'armatures', ''),
        ('brushes', 'brushes', ''),
        ('cameras', 'cameras', ''),
        ('curves', 'curves', ''),
        ('fonts', 'fonts', ''),
        ('groups', 'groups', ''),
        ('images', 'images', ''),
        ('lamps', 'lamps', ''),
        ('lattices', 'lattices', ''),
        ('linestyles', 'linestyles', ''),
        ('masks', 'masks', ''),
        ('materials', 'materials', ''),
        ('meshes', 'meshes', ''),
        ('metaballs', 'metaballs', ''),
        ('movieclips', 'movieclips', ''),
        ('node_groups', 'node_groups', ''),
        ('objects', 'objects', ''),
        ('particles', 'particles', ''),
        ('scenes', 'scenes', ''),
        ('shape_keys', 'shape_keys', ''),
        ('sounds', 'sounds', ''),
        ('speakers', 'speakers', ''),
        ('texts', 'texts', ''),
        ('textures', 'textures', ''),
        ('worlds', 'worlds', ''),
        
)



class DataOutputNode(Node):
    
    '''Data Input'''
    bl_idname = 'DataOutputNodeType'
    bl_label = 'Data Output'
    
    
    # === Callbacks ===
    
    def update_attribute(self, context):
        self.update()
        
    
    # === Custom Properties ===
    
    settings = bpy.props.BoolProperty(name = "Settings", default = True)
    
    data_enum = bpy.props.EnumProperty(name = "Data", items = data_items, default="objects")
    data_item = bpy.props.StringProperty(name = "Item")
    
    attributeProperty = bpy.props.StringProperty(name = "Attribute", update = update_attribute)


    # === Optional Functions ===
    def init(self, context):
        #self.inputs.new('NodeSocketFloat', "Value")
        pass
        
    
    def update(self):
        
        # set data value
        if self.data_item:
            data_path = "bpy.data."+self.data_enum + "['"+self.data_item+"']"
            data_path = eval(data_path)
            
            for input in self.inputs:
                for link in input.links:
                    if link.is_valid:
                        value = input.default_value
                        exec("data_path."+input.name+"=value")
                        #print (exec("data_path."+input.name))
                        #print (bpy.data.objects["Text"].data.body)
            
        

    
    
    
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        
        if self.settings:
            row = layout.row()
            row.prop(self, "settings", text="", icon="TRIA_DOWN", emboss=False)
            
            
            layout.prop(self, "data_enum")
            
            row = layout.row(align = True)
            row.prop_search(self, "data_item", bpy.data, self.data_enum, text="")
            row.operator("get_object_to_custom_node.btn", text = "", icon="EYEDROPPER")
            
            row = layout.row(align = True)
            row.prop(self, "attributeProperty", text="")
            row.operator("add_input_socket_to_custom_node.btn", text = "", icon="ZOOMIN")
            
            layout.operator("remove_input_sockets.btn", text="Clear", icon="X")
            
        else:
            row = layout.row()
            row.prop(self, "settings", text="", icon="TRIA_RIGHT", emboss=False)
            row.label(self.data_item)

    # Detail buttons in the sidebar.
    def draw_buttons_ext(self, context, layout):
        
        layout.prop(self, "data_enum")
        
        row = layout.row(align = True)
        row.prop_search(self, "data_item", bpy.data, self.data_enum, text="")
        row.operator("get_object_to_custom_node.btn", text = "", icon="EYEDROPPER")
        
        row = layout.row(align = True)
        row.prop(self, "attributeProperty", text="")
        row.operator("add_input_socket_to_custom_node.btn", text = "", icon="ZOOMIN")
        
        layout.operator("remove_input_sockets.btn", text="Clear", icon="X")
    
    def draw_label(self):
        return "Data Output"







def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
print ("---")