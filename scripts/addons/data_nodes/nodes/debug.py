import bpy
from bpy.types import Node


class DebugNode(Node):
    """Debug node"""
    bl_idname = 'DebugNodeType'
    bl_label = 'Debug'

    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Integer')
        self.inputs.new('NodeSocketFloat', 'Float')
        self.inputs.new('NodeSocketVector', 'Vector')
        self.inputs.new('NodeSocketColor', 'Color')
        self.inputs.new('NodeSocketString', 'String')
        self.inputs.new('NodeSocketBool', 'Boolean')

    # def update(self):
    #     pass

    def draw_buttons(self, context, layout):
        if self.inputs['Integer'].links:
            layout.label(text='Integer : ' + str(self.inputs['Integer'].default_value))
        if self.inputs['Float'].links:
            layout.label(text='Float : ' + str(self.inputs['Float'].default_value))
        if self.inputs['Vector'].links:
            layout.label(text='Vector X : ' + str(self.inputs['Vector'].default_value[0]))
            layout.label(text='Vector Y : ' + str(self.inputs['Vector'].default_value[1]))
            layout.label(text='Vector Z : ' + str(self.inputs['Vector'].default_value[2]))
        if self.inputs['Color'].links:
            layout.label(text='Color R : ' + str(self.inputs['Color'].default_value[0]))
            layout.label(text='Color G : ' + str(self.inputs['Color'].default_value[1]))
            layout.label(text='Color B : ' + str(self.inputs['Color'].default_value[2]))
            layout.label(text='Color A : ' + str(self.inputs['Color'].default_value[3]))
        if self.inputs['String'].links:
            layout.label(text='String : ' + self.inputs['String'].default_value)
        if self.inputs['Boolean'].links:
            layout.label(text='Boolean : ' + str(self.inputs['Boolean'].default_value))

    def draw_label(self):
        return 'Debug'
