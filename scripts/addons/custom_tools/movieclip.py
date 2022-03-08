from .colorspace import SetInputTransform


class SetMovieClipInputTransform(SetInputTransform):
    bl_idname = 'scene.set_movieclip_input_transform'
    bl_label = 'Set movieclip input transform'

    @classmethod
    def poll(cls, context):
        return context.space_data.clip

    def get_datablocks(self, context):
        return [context.space_data.clip]
