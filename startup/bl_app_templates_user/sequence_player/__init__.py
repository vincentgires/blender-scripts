import bpy
import bpy.utils.previews
from bpy.app.handlers import persistent
import logging
import os
import sys

from .ui import *
from .operators import *

supported_extensions = ('.mov', '.mp4', '.png',
                        '.jpg', '.jpeg', '.exr', '.hdr')


def check_file_extension(file):
    if file.lower().endswith(supported_extensions):
        return True
    else:
        return False


def get_files_from_directory(dirpath):
    if os.path.exists(dirpath):
        paths = []
        for file in os.listdir(dirpath):
            if check_file_extension(file):
                path = os.path.join(dirpath, file)
                paths.append(path)
        paths.sort()
        return paths
    else:
        return None


def update_directory_preview(self, context):
    clip = context.space_data.clip
    if clip:
        clip.filepath = self.directory_image_preview
    else:
        sequence_path = self.directory_image_preview
        bpy.ops.scene.load_clip(filepath=sequence_path)


def get_enum_preview_from_directory_items(self, context):
    wm = context.window_manager
    directory = wm.sequence_player.directory_path
    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collections['directory_preview']

    if directory == pcoll.preview_directory:
        return pcoll.preview_items

    paths = get_files_from_directory(directory)
    if paths:
        for index, filepath in enumerate(paths):
            filename = os.path.basename(filepath)
            if filepath in pcoll:
                thumb = pcoll[filepath]
            else:
                thumb = pcoll.load(filepath, filepath, 'MOVIE')
            enum_items.append((filepath, filename, filename,
                               thumb.icon_id, index))

    pcoll.preview_items = enum_items
    pcoll.preview_directory = directory
    return pcoll.preview_items


class SequencePlayerProperties(bpy.types.PropertyGroup):
    directory_path = bpy.props.StringProperty(
        name='Directory',
        description='Directory',
        subtype='DIR_PATH')

    directory_image_preview = bpy.props.EnumProperty(
        items=get_enum_preview_from_directory_items,
        name='Image preview',
        update=update_directory_preview)

    show_folders = bpy.props.BoolProperty(
        name='Folders',
        description='Show folders',
        default=True)

    show_files = bpy.props.BoolProperty(
        name='Files',
        description='Show files',
        default=True)


@persistent
def scene_update(scene):
    context = bpy.context
    wm = context.window_manager
    data = bpy.data
    movieclips = data.movieclips

    if not movieclips.is_updated:
        return None

    logging.debug('movieclips is updated')
    for area in context.screen.areas:
        if area.type != 'CLIP_EDITOR':
            continue
        for space in area.spaces:
            if space.type != 'CLIP_EDITOR':
                continue
            clip = space.clip
            filename = os.path.basename(clip.filepath)
            file, ext = os.path.splitext(filename)
            ext = ext.lower()

            clip.name = filename
            context.scene.frame_end = clip.frame_duration

            # set browser
            folderpath = os.path.dirname(clip.filepath)
            wm.sequence_player.directory_path = folderpath

            # set colorspace
            if scene.display_settings.display_device == 'ACES':
                if ext in ['.exr']:
                    clip.colorspace_settings.name = 'ACES - ACEScg'
                else:
                    clip.colorspace_settings.name = 'Output - sRGB (D60 sim.)'
            else:
                if ext in ['.exr']:
                    clip.colorspace_settings.name = 'Linear'
                else:
                    clip.colorspace_settings.name = 'sRGB'


preview_collections = {}
keymaps = []
keep_panels = ['Footage Settings', 'Footage Information']

def register():
    # Unregister all defaults panels
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'CLIP_EDITOR':
            # check if we already removed!
            if 'bl_rna' in pt.__dict__:
                # keep some panels
                if pt.bl_label not in keep_panels:
                    bpy.utils.unregister_class(pt)

    bpy.utils.register_class(SequencePlayerProperties)
    bpy.utils.register_class(LoadClip)
    bpy.utils.register_class(UIBrowser)
    bpy.utils.register_class(UIDisplay)
    bpy.utils.register_class(UIColorManagement)
    bpy.utils.register_class(FolderNavigation)
    bpy.utils.register_class(UISettings)
    bpy.utils.register_class(InteractiveTimeline)

    # Keymaps
    kc = bpy.context.window_manager.keyconfigs.default
    km = bpy.context.window_manager.keyconfigs.default.keymaps['Clip']

    # Interactive timeline
    kmi = km.keymap_items.new('screen.interactive_timeline', 'S', 'PRESS')
    keymaps.append((km, kmi))

    bpy.app.handlers.scene_update_post.append(scene_update)

    pcoll = bpy.utils.previews.new()
    pcoll.preview_directory = ''
    pcoll.preview_items = ()
    preview_collections['directory_preview'] = pcoll
    bpy.types.WindowManager.sequence_player = \
        bpy.props.PointerProperty(type=SequencePlayerProperties)


def unregister():
    bpy.utils.unregister_class(SequencePlayerProperties)
    bpy.utils.unregister_class(LoadClip)
    bpy.utils.unregister_class(UIBrowser)
    bpy.utils.unregister_class(UIDisplay)
    bpy.utils.unregister_class(UIColorManagement)
    bpy.utils.unregister_class(FolderNavigation)
    bpy.utils.unregister_class(UISettings)
    bpy.utils.unregister_class(InteractiveTimeline)

    # Register all the defaults panels
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'CLIP_EDITOR':
            if pt.bl_label not in keep_panels:
                bpy.utils.register_class(pt)

    # Keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    bpy.app.handlers.scene_update_post.remove(scene_update)

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    del bpy.types.WindowManager.sequence_player
