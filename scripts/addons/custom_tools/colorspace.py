from bpy.types import Operator
from bpy.props import StringProperty
from vgblender.colorspace import set_input_transform


class SetInputTransform(Operator):
    bl_idname = 'scene.set_input_transform'
    bl_label = 'Set input transform'

    input_transform: StringProperty(name='Input transform')

    def get_datablocks(self, context):
        raise NotImplementedError

    def execute(self, context):
        for datablock in self.get_datablocks(context):
            set_input_transform(datablock, self.input_transform)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
