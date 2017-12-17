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
    
    def draw_label(self):
        return "Debug"
