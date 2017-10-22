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

# Author : Vincent Gires
# www.vincentgires.com


import bpy
import os


## PANEL ##
###########


class SequencerCustomPanel(bpy.types.Panel):
    bl_label = 'Custom'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        layout.operator('scene.customtools_open_strip_as_movie_clip')


## OPERATOR ##
##############


class CustomToolsOpenStripAsMovieClip(bpy.types.Operator):
    bl_idname = 'scene.customtools_open_strip_as_movie_clip'
    bl_label = 'Open strip as movie clip'
    
    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            if context.scene.sequence_editor.active_strip.type == 'MOVIE':
                return True
        else:
            return False
    
    def execute(self, context):
        strip = context.scene.sequence_editor.active_strip
        movie = bpy.data.movieclips.load(filepath = strip.filepath)
        movie.frame_start = strip.frame_start
        
        return{'FINISHED'}
    
    
