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


class DebugNode(Node):
    
    '''Debug node'''
    bl_idname = 'DebugNodeType'
    bl_label = 'Debug'
    
    
    
    def init(self, context):
        self.inputs.new('NodeSocketInt', "Integer")
        self.inputs.new('NodeSocketFloat', "Float")
        self.inputs.new('NodeSocketVector', "Vector")
        self.inputs.new('NodeSocketColor', "Color")
        self.inputs.new('NodeSocketString', "String")
        self.inputs.new('NodeSocketBool', "Boolean")
    
    
    def update(self):
        
        """for input in self.inputs:
            for link in input.links:
                if link.is_valid:
                    pass"""
        pass
    
                 
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        
        if self.inputs["Integer"].links:
            layout.label("Integer : " + str(self.inputs["Integer"].default_value))
        if self.inputs["Float"].links:
            layout.label("Float : " + str(self.inputs["Float"].default_value))
        if self.inputs["Vector"].links:
            layout.label("Vector X : " + str(self.inputs["Vector"].default_value[0]))
            layout.label("Vector Y : " + str(self.inputs["Vector"].default_value[1]))
            layout.label("Vector Z : " + str(self.inputs["Vector"].default_value[2]))
        if self.inputs["Color"].links:
            layout.label("Color R : " + str(self.inputs["Color"].default_value[0]))
            layout.label("Color G : " + str(self.inputs["Color"].default_value[1]))
            layout.label("Color B : " + str(self.inputs["Color"].default_value[2]))
            layout.label("Color A : " + str(self.inputs["Color"].default_value[3]))
        if self.inputs["String"].links:
            layout.label("String : " + self.inputs["String"].default_value)
        if self.inputs["Boolean"].links:
            layout.label("Boolean : " + str(self.inputs["Boolean"].default_value))
        
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Debug"








def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")