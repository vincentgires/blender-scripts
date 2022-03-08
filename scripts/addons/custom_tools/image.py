from .colorspace import SetInputTransform


class SetImageInputTransform(SetInputTransform):
    bl_idname = 'scene.set_image_input_transform'
    bl_label = 'Set image input transform'

    @classmethod
    def poll(cls, context):
        return context.space_data.image

    def get_datablocks(self, context):
        return [context.space_data.image]
