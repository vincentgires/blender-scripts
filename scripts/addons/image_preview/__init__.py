import os
import bpy
from bpy.utils import previews
from image_preview import ui

bl_info = {
    'name': 'Image Preview',
    'author': 'Vincent Girès',
    'description': 'Data image preview',
    'version': (0, 0, 1),
    'blender': (2, 7, 8),
    'location': 'Property panel > Images',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Images'}

preview_images = {}


def update_image_preview(self, context):
    data = bpy.data
    scene = context.scene
    space = context.space_data
    wm = context.window_manager
    image_path = wm.image_preview
    image_path = os.path.normpath(image_path)

    if space.type == 'IMAGE_EDITOR':
        image = data.images.load(filepath=image_path, check_existing=True)
        space.image = image
    else:
        bpy.ops.image_viewer.qt_event_loop(
            'INVOKE_DEFAULT',
            filepath=image_path)


def get_enum_previews_from_file(self, context):
    '''EnumProperty callback'''

    enum_items = []
    if not context:
        return enum_items
    pcoll = preview_images['images']
    for index, image in enumerate(bpy.data.images):
        if image.type == 'IMAGE':
            enum_items.append(
                (image.filepath, image.filepath, '',
                 image.preview.icon_id, index))
    pcoll.my_previews = enum_items
    return pcoll.my_previews


def register():
    preview_images['images'] = previews.new()
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.image_preview = bpy.props.EnumProperty(
        items=get_enum_previews_from_file,
        name='Image preview',
        update=update_image_preview)


def unregister():
    for pcoll in preview_images.values():
        previews.remove(pcoll)
    preview_images.clear()
    bpy.utils.unregister_module(__name__)
    del bpy.types.WindowManager.image_preview


if __name__ == '__main__':
    register()
