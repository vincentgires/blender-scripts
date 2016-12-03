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
    "name": "MovieAssembly",
    "author": "Vincent Gires",
    "description": "---",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "location": "Sequencer > Property",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"}


import sys, os, logging

if 'bpy' in locals():
    import importlib
    importlib.reload(addon_preferences)
    importlib.reload(panels)
    logging.debug('Reloaded files as modules')
else:
    from movie_assembly import addon_preferences, panels
    logging.debug('Imported files as modules')
    
import bpy
     


class MOVIE_ASSEMBLY_properties(bpy.types.PropertyGroup):
    
    # SEQUENCES
    project = bpy.props.StringProperty(
        name = "Project"
    )


'''
## CALL BACK ##
###############

def update_channel(self, context):
    context.space_data.display_channel = context.scene.movie_assembly_channel_update

def update_list_shots(self, context):
    collection = context.scene.movie_assembly_collection
    collection_index = context.scene.movie_assembly_collection_index
    
    context.scene.frame_current = collection[collection_index].frame_start


## CUSTOM PROPERTIES ##
#######################



# collection

class property_collection_movie_assembly(bpy.types.PropertyGroup):
    seq = bpy.props.IntProperty(name="Sequence", default=0)
    shot = bpy.props.IntProperty(name="Shot", default=0)
    frames = bpy.props.IntProperty(name="Frames", default=0)
    first_frame = bpy.props.IntProperty(name="First frame", default=0)
    resolution = bpy.props.IntVectorProperty(
        name = "Resolution",
        subtype = "XYZ",
        size = 2, # 32 = XY
        step = 10,
        default = (2578, 1080)
    )
    frame_start = bpy.props.IntProperty(name="Frame start", default=1)
    grading_frame = bpy.props.IntProperty(name="Grading frame", default=0)


class property_collection_annotation(bpy.types.PropertyGroup):
    seq = bpy.props.IntProperty(name="Sequence", default=0)
    shot = bpy.props.IntProperty(name="Shot", default=0)
    note = bpy.props.StringProperty(name="Note", default="Note")
    noteType = bpy.props.StringProperty(name="Note type", default="frame")
    color = bpy.props.FloatVectorProperty(
        name = "Color",
        subtype = "COLOR",
        size = 4, # 4 = RGBA
        soft_min=0.0, soft_max=1.0,
        default = (1.0, 0.0, 0.0, 1.0),
    )
    position = bpy.props.FloatVectorProperty(
        name = "Position",
        subtype = "XYZ",
        size = 2, # 32 = XY
        soft_min=0.0, soft_max=1.0,
        step = 0.25,
        default = (0.5, 0.5)
    )
    size = bpy.props.IntProperty(
        name = "Size",
        soft_min=0, soft_max=100,
        default = 35
    )
    size_zoom = bpy.props.BoolProperty(name="Zoom scale", default=True)
    display = bpy.props.BoolProperty(name="Display note", default=True)
    frame = bpy.props.IntProperty(name="Frame", default=0)
    line = bpy.props.StringProperty(name="Line", default="[]")
    line_size = bpy.props.IntProperty(
        name = "Line size",
        soft_min=1, soft_max=10,
        default = 2
    )


class check_sequence_properties(bpy.types.PropertyGroup):
    
    # SEQUENCES
    bpy.types.Scene.movie_assembly_sequences = bpy.props.StringProperty(
        name = "Sequences",
        description = "Sequences to load (separate by ,)"
    )
    
    # SHOTS
    bpy.types.Scene.movie_assembly_shots = bpy.props.StringProperty(
        name = "Shots",
        description = "Shots to load (separate by ,)"
    )
    
    # PRELOAD
    bpy.types.Scene.movie_assembly_preload = bpy.props.BoolProperty(
        name = "preload",
        description = "Preload first frame of each movies",
        default = False
    )
    
    # MOVIES
    bpy.types.Scene.movie_assembly_load_movies = bpy.props.BoolProperty(
        name = "movies",
        default = True
    )
    
    # GRADINGS
    bpy.types.Scene.movie_assembly_load_gradings = bpy.props.BoolProperty(
        name = "gradings",
        default = True
    )
    
    # FRAME DURATION
    bpy.types.Scene.movie_assembly_frame_duration = bpy.props.IntProperty(
        name = "Frame duration",
        description = "",
        default = 1
    )
   
    # TYPE
    bpy.types.Scene.movie_assembly_type = bpy.props.EnumProperty(
        items = (
            ('last', 'last state', 'last state'),
            ('precomp_lgt', 'precomp', 'precomp_lgt'),
            ('linetest', 'linetest', 'linetest'),
            ('final', 'final', 'final'),
            ('animation', 'animation', 'animation'),
            ('chr_fx', 'chr_fx', 'chr_fx'),
        ),
        name = "Type",
        description = "Select type",
        default = 'last'
    )

    # CAMERA
    bpy.types.Scene.movie_assembly_camera = bpy.props.EnumProperty(
        items = (
            ('l', 'l', 'L camera'),
            ('r', 'r', 'R camera'),
            ('ana', 'ana', 'Ana camera'),
        ),
        name = "Camera",
        description = "Select camera",
        default = 'l'
    )
    
    # SWITCH CHANNEL
    bpy.types.Scene.movie_assembly_channel_update = bpy.props.IntProperty(
        name = "Sequence",
        min = 1,
        max = 2,
        description = "",
        default = 1,
        update = update_channel
    )
    
    # COLLECTION INDEX
    bpy.types.Scene.movie_assembly_collection_index = bpy.props.IntProperty(
        name = "List shots index",
        description = "---",
        default = 0,
        min = 0,
        update = update_list_shots
    )
    
    bpy.types.Scene.movie_assembly_annotation_index = bpy.props.IntProperty(
        name = "List annotation",
        description = "---",
        default = 0,
        min = 0,
    )
    
    # NOTE PROPERTIES
    bpy.types.Scene.movie_assembly_note_properties = bpy.props.BoolProperty(
        name = "Properties",
        default = False
    )
    
    # NOTE DISPLAY
    bpy.types.Scene.movie_assembly_note_display = bpy.props.BoolProperty(
        name = "Display notes",
        default = True,
    )
    
    # NOTE EXPORT PATH
    bpy.types.Scene.movie_assembly_note_export_folder = bpy.props.StringProperty(
        name = "",
        description = "Export folder path",
        default = "",
        subtype = 'DIR_PATH',
    )
    
    
    # INFO DISPLAY
    bpy.types.Scene.movie_assembly_info_display = bpy.props.BoolProperty(
        name = "Display infomation",
        default = True,
    )
    
    
    bpy.types.Scene.movie_assembly_timeline_shot_display = bpy.props.BoolProperty(
        name = "Display shots",
        default = True,
    )
    
    bpy.types.Scene.movie_assembly_timeline_seq_display = bpy.props.BoolProperty(
        name = "Display sequences",
        default = True,
    )

    bpy.types.Scene.movie_assembly_timeline_hide_frames = bpy.props.BoolProperty(
        name = "Hide frames",
        default = True,
    )


    



#########################
#########################

# KEYMAPS
KEYMAPS = []


try:
    # if already exists, do nothing
    handle_draw_note
    handle_draw_information
    handle_draw_timeline
    handle_draw_timeline_post_view
except:
    handle_draw_note = [None]
    handle_draw_information = [None]
    handle_draw_timeline = [None]
    handle_draw_timeline_post_view = [None]
'''

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.movie_assembly = bpy.props.PointerProperty(type=MOVIE_ASSEMBLY_properties)
    
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.movie_assembly
    
if __name__ == "__main__":
    register()
    
