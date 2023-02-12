import os
import bpy
from bpy.utils import previews

bl_info = {
    'name': 'Image Preview',
    'author': 'Vincent Girès',
    'description': 'Data image preview',
    'version': (0, 0, 1),
    'blender': (3, 4, 0),
    'location': 'Property panel (Image Editor)',
    'category': 'Images'}

preview_images = {}


def update_image_preview(self, context):
    data = bpy.data
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
    """EnumProperty callback"""

    enum_items = []
    if not context:
        return enum_items
    pcoll = preview_images['images']
    images = [
        i for i in bpy.data.images
        if i.type == 'IMAGE' and i.preview is not None]
    for index, image in enumerate(images):
        enum_items.append((
            image.filepath,
            image.filepath,
            '',
            image.preview.icon_id,
            index))
    pcoll.my_previews = enum_items
    return pcoll.my_previews


class ImageEditorPanel(bpy.types.Panel):
    bl_idname = 'IMAGEPREVIEW_PT_ImageEditorPanel'
    bl_label = 'Images'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Images'

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        layout.template_icon_view(wm, 'image_preview', show_labels=False)


class SequencerPanel(bpy.types.Panel):
    bl_idname = 'IMAGEPREVIEW_PT_SequencerPanel'
    bl_label = 'Images'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Images'

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        layout.template_icon_view(wm, 'image_preview', show_labels=False)


class View3dPanel(bpy.types.Panel):
    bl_idname = 'IMAGEPREVIEW_PT_View3dPanel'
    bl_label = 'Images'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Images'

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        layout.template_icon_view(wm, 'image_preview', show_labels=False)


classes = (ImageEditorPanel, SequencerPanel, View3dPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    preview_images['images'] = previews.new()
    bpy.types.WindowManager.image_preview = bpy.props.EnumProperty(
        items=get_enum_previews_from_file,
        name='Image preview',
        update=update_image_preview)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    for pcoll in preview_images.values():
        previews.remove(pcoll)
    preview_images.clear()
    del bpy.types.WindowManager.image_preview
