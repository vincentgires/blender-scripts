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
from data_nodes.functions import send_value_link


class ObjectPropertiesNode(Node):
    
    '''Object Properties'''
    bl_idname = 'ObjectPropertiesNodeType'
    bl_label = 'Object Properties'
    
    
    def update_object_name(self, context):
        # update properties from the new selected object
        if self.data_item is not "":
            self.update_props_from_object()
            
        
        
        
    def update_object_location(self, context):
        if self.data_item is not "":
            context.scene.objects[self.data_item].location = self.locationProperty
            self.update()
    
    def update_object_rotation(self, context):
        if self.data_item is not "":
            #context.scene.objects[self.data_item].rotation_euler = self.rotationProperty
            context.scene.objects[self.data_item].rotation_euler[0] = math.radians(self.rotationProperty[0])
            context.scene.objects[self.data_item].rotation_euler[1] = math.radians(self.rotationProperty[1])
            context.scene.objects[self.data_item].rotation_euler[2] = math.radians(self.rotationProperty[2])
            self.update()
    
    def update_object_scale(self, context):
        if self.data_item is not "":
            context.scene.objects[self.data_item].scale = self.scaleProperty
            self.update()
    
    def update_invert_matrix(self, context):
        if self.data_item is not "":
            self.update()
    
    def update_matrix(self):
        if self.data_item is not "":
            object = bpy.context.scene.objects[self.data_item]
            matrix = object.matrix_world.to_3x3()
            if self.invertMatrixProperty:
                matrix = matrix.inverted()
            self.matrixRow1Property = matrix[0]
            self.matrixRow2Property = matrix[1]
            self.matrixRow3Property = matrix[2]
    
    
    def update_target_nodes(self):
        for output in self.outputs:
            for link in output.links:
                if link.is_valid:
                    # update connected target nodes
                    link.to_node.update()
        
        
    
    # === Custom Properties ===
    data_item = bpy.props.StringProperty(name = "Object", update = update_object_name)
    locationProperty = bpy.props.FloatVectorProperty(name = "Location", default = (0.0, 0.0, 0.0), update = update_object_location)
    rotationProperty = bpy.props.FloatVectorProperty(name = "Rotation", default = (0.0, 0.0, 0.0), update = update_object_rotation)
    scaleProperty = bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0), update = update_object_scale)
    invertMatrixProperty = bpy.props.BoolProperty(name = "Invert Matrix", default = False, update = update_invert_matrix)
    matrixRow1Property = bpy.props.FloatVectorProperty(name = "Matrix Row1", default = (1.0, 0.0, 0.0))
    matrixRow2Property = bpy.props.FloatVectorProperty(name = "Matrix Row2", default = (0.0, 1.0, 0.0))
    matrixRow3Property = bpy.props.FloatVectorProperty(name = "Matrix Row3", default = (0.0, 0.0, 1.0))
    displayProperty = bpy.props.BoolProperty(name = "display properties", default = False)



    # === Optional Functions ===
    def init(self, context):
        
        self.outputs.new('NodeSocketVector', "Location")
        self.outputs.new('NodeSocketVector', "Rotation")
        self.outputs.new('NodeSocketVector', "Scale")
        self.outputs.new('NodeSocketVector', "Matrix Row1")
        self.outputs.new('NodeSocketVector', "Matrix Row2")
        self.outputs.new('NodeSocketVector', "Matrix Row3")
        
    
    def update(self):
        
        self.update_matrix()
        
        for output in self.outputs:
            for link in output.links:
                
                if output.name == "Location":
                    output.default_value = self.locationProperty
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.locationProperty)
                    
                elif output.name == "Rotation":
                    output.default_value = self.rotationProperty
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.rotationProperty)
                    
                elif output.name == "Scale":
                    output.default_value = self.scaleProperty
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.scaleProperty)
                
                elif output.name == "Matrix Row1":
                    output.default_value = self.matrixRow1Property
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.matrixRow1Property)
                    
                elif output.name == "Matrix Row2":
                    output.default_value = self.matrixRow2Property
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.matrixRow2Property)
                    
                elif output.name == "Matrix Row3":
                    output.default_value = self.matrixRow3Property
                    if link.to_socket.type == "VECTOR":
                        send_value_link(link, self.matrixRow3Property)
        
        self.update_target_nodes()
    
    def update_props_from_object(self):
        self.locationProperty = bpy.context.scene.objects[self.data_item].location
        self.rotationProperty = bpy.context.scene.objects[self.data_item].rotation_euler
        self.rotationProperty[0] = math.degrees(self.rotationProperty[0])
        self.rotationProperty[1] = math.degrees(self.rotationProperty[1])
        self.rotationProperty[2] = math.degrees(self.rotationProperty[2])
        self.scaleProperty = bpy.context.scene.objects[self.data_item].scale
        
    
    
    
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        row = layout.row(align = True)
        row.prop_search(self, "data_item", bpy.data, "objects", icon='OBJECT_DATA', text="")
        row.operator("get_object_to_custom_node.btn", text = "", icon="EYEDROPPER")
        
        layout.prop(self, "displayProperty", "Properties")
        if self.displayProperty:
            layout.prop(self, "locationProperty")
            layout.prop(self, "rotationProperty")
            layout.prop(self, "scaleProperty")
        
        layout.prop(self, "invertMatrixProperty")

    # Detail buttons in the sidebar.
    def draw_buttons_ext(self, context, layout):
        row = layout.row(align = True)
        row.prop_search(self, "data_item", bpy.data, "objects", icon='OBJECT_DATA')
        row.operator("get_object_to_custom_node.btn", text = "", icon="EYEDROPPER")
        
        layout.prop(self, "locationProperty")
        layout.prop(self, "rotationProperty")
        layout.prop(self, "scaleProperty")
        
        box = layout.box()
        box.prop(self, "invertMatrixProperty")
        row = box.row()
        row.label(str(self.matrixRow1Property[0]))
        row.label(str(self.matrixRow1Property[1]))
        row.label(str(self.matrixRow1Property[2]))
        row = box.row()
        row.label(str(self.matrixRow2Property[0]))
        row.label(str(self.matrixRow2Property[1]))
        row.label(str(self.matrixRow2Property[2]))
        row = box.row()
        row.label(str(self.matrixRow3Property[0]))
        row.label(str(self.matrixRow3Property[1]))
        row.label(str(self.matrixRow3Property[2]))
    
    
    def draw_label(self):
        return "Object Properties"







def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
