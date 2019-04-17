import bpy
import os


class SequencerCustomPanel(bpy.types.Panel):
    bl_label = 'Custom'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout
        layout.operator('scene.customtools_open_strip_as_movie_clip')


class CustomToolsOpenStripAsMovieClip(bpy.types.Operator):
    bl_idname = 'scene.customtools_open_strip_as_movie_clip'
    bl_label = 'Open strip as movie clip'

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            return scene.sequence_editor.active_strip.type == 'MOVIE'

    def execute(self, context):
        scene = context.scene
        data = bpy.data
        strip = scene.sequence_editor.active_strip
        movie = data.movieclips.load(filepath=strip.filepath)
        movie.frame_start = strip.frame_start
        return{'FINISHED'}
