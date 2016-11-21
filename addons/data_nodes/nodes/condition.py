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
from math import *
from bpy.types import NodeTree, Node, NodeSocket
import string
from data_nodes.functions import send_value

operation_items = (
        ('==', '==', ''),
        ('!=', '!=', ''),
        ('>', '>', ''),
        ('>=', '>=', ''),
        ('<', '<', ''),
        ('<=', '<=', ''),
        ('and', 'and', ''),
        ('or', 'or', ''),
        ('not', 'not', ''),
        
)


class Condition(Node):
    
    '''Expression node'''
    bl_idname = 'ConditionNodeType'
    bl_label = 'Condition'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    operation_enum = bpy.props.EnumProperty(name = "", items = operation_items, update = update_props)
    
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', "A")
        self.inputs.new('NodeSocketFloat', "B")
        self.outputs.new('NodeSocketFloat', "Value")
    
    
    def update(self):
        
        if len(self.inputs) >= 2:
            
            A = self.inputs["A"].default_value
            B = self.inputs["B"].default_value
            
            if self.operation_enum == "==":
                send_value(self.outputs, A == B)
                
            elif self.operation_enum == "!=":
                send_value(self.outputs, A != B)
                
            elif self.operation_enum == ">":
                send_value(self.outputs, A > B)
                
            elif self.operation_enum == ">=":
                send_value(self.outputs, A >= B)
                
            elif self.operation_enum == "<":
                send_value(self.outputs, A < B)
                
            elif self.operation_enum == "<=":
                send_value(self.outputs, A <= B)
                
            elif self.operation_enum == "and":
                send_value(self.outputs, A and B)
                
            elif self.operation_enum == "or":
                send_value(self.outputs, A or B)
                
            elif self.operation_enum == "not":
                send_value(self.outputs, not A)
                
            else:
                send_value(self.outputs, False)
            
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "operation_enum")
    
    # Detail buttons in the sidebar
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Condition"




def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")
