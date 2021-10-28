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

    def draw_buttons(self, context, layout):
        if self.inputs['Integer'].links:
            layout.label(
                text=f"Integer : {self.inputs['Integer'].default_value}")
        if self.inputs['Float'].links:
            layout.label(text=f"Float : {self.inputs['Float'].default_value}")
        if self.inputs['Vector'].links:
            layout.label(
                text=f"Vector X : {self.inputs['Vector'].default_value[0]}")
            layout.label(
                text=f"Vector Y : {self.inputs['Vector'].default_value[1]}")
            layout.label(
                text=f"Vector Z : {self.inputs['Vector'].default_value[2]}")
        if self.inputs['Color'].links:
            layout.label(
                text=f"Color R : {self.inputs['Color'].default_value[0]}")
            layout.label(
                text=f"Color G : {self.inputs['Color'].default_value[1]}")
            layout.label(
                text=f"Color B : {self.inputs['Color'].default_value[2]}")
            layout.label(
                text=f"Color A : {self.inputs['Color'].default_value[3]}")
        if self.inputs['String'].links:
            layout.label(
                text=f"String : {self.inputs['String'].default_value}")
        if self.inputs['Boolean'].links:
            layout.label(
                text=f"Boolean : {self.inputs['Boolean'].default_value}")

    def draw_label(self):
        return 'Debug'
