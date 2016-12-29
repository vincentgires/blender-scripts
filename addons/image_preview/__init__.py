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


bl_info = {
    "name": "Image Preview",
    "author": "Vincent Gires",
    "description": "---",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "location": "Property panel > Images",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Images"}


import sys, os, logging
import bpy, bpy.utils.previews
from image_preview import ui


def update_image_preview(self, context):
    data = bpy.data
    scene = context.scene
    space = context.space_data
    wm = context.window_manager
    
    if space.type == 'IMAGE_EDITOR':
        image_path = wm.image_preview
        image_path = os.path.normpath(image_path)
        image = data.images.load(filepath=image_path, check_existing=True)
        space.image = image
    
    else:
        bpy.ops.image_viewer.qt_event_loop('INVOKE_DEFAULT')


def get_enum_previews_from_file(self, context):
    '''EnumProperty callback'''
    
    enum_items = []

    if context is None:
        return enum_items
    
    pcoll = preview_images['images']
    for index, image in enumerate(bpy.data.images):
        enum_items.append((image.filepath, image.filepath, '', image.preview.icon_id, index))
    
    pcoll.my_previews = enum_items
    return pcoll.my_previews




# global variable to store icons in
preview_images = {}

def register():
    
    preview_images['images'] = bpy.utils.previews.new()
    
    bpy.utils.register_module(__name__)
    
    bpy.types.WindowManager.image_preview = bpy.props.EnumProperty(
        items = get_enum_previews_from_file,
        name = 'Image preview',
        update = update_image_preview
    )
    
def unregister():
    
    for pcoll in preview_images.values():
        bpy.utils.previews.remove(pcoll)
    preview_images.clear()
    
    bpy.utils.unregister_module(__name__)
    del bpy.types.WindowManager.image_preview
    

if __name__ == "__main__":
    register()

