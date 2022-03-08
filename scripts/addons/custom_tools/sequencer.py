import bpy
from bpy.types import Operator, Panel, OperatorFileListElement
from bpy.props import (
    StringProperty, CollectionProperty, BoolProperty, IntProperty)
from bpy_extras.io_utils import ImportHelper
import os
from vgblender.sequencer import (
    create_adjustment_strip, load_multiple_movie_strips,
    set_strip_proxy_quality)
from .colorspace import SetInputTransform


class SequencerCustomPanel(Panel):
    bl_idname = 'CUSTOMTOOLS_PT_sequencer_custom_panel'
    bl_label = 'Custom'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='Scene strips')
        row = col.row(align=True)
        row.operator('scene.disable_scene_strips', text='Mute').mute = True
        row.operator('scene.disable_scene_strips', text='Show').mute = False
        col.operator('scene.set_active_scene_from_strip', text='Set active')


class OpenStripAsMovieclip(Operator):
    bl_idname = 'scene.open_strip_as_movieclip'
    bl_label = 'Open strip as movieclip'

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


class AddStripAsCompositing(Operator):
    bl_idname = 'scene.add_strip_as_compositing'
    bl_label = 'Add strip as a compositing scene'

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            return scene.sequence_editor.active_strip.type == 'MOVIE'

    def execute(self, context):
        data = bpy.data
        sequence_editor = context.scene.sequence_editor
        strip = sequence_editor.active_strip

        movieclip = data.movieclips.load(filepath=strip.filepath)
        movieclip.colorspace_settings.name = strip.colorspace_settings.name
        x, y = movieclip.size
        scene = data.scenes.new(movieclip.name)
        scene.render.resolution_x = x
        scene.render.resolution_y = y
        scene.render.resolution_percentage = 100
        scene.frame_start = 1
        scene.frame_end = movieclip.frame_duration

        scene.use_nodes = True
        node_tree = scene.node_tree
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)
        movieclip_node = node_tree.nodes.new('CompositorNodeMovieClip')
        movieclip_node.clip = movieclip
        output_node = node_tree.nodes.new('CompositorNodeComposite')
        node_tree.links.new(movieclip_node.outputs[0], output_node.inputs[0])

        # Create scene on sequencer
        sequence_editor.sequences.new_scene(
            scene.name, scene, strip.channel + 1, strip.frame_start)

        return{'FINISHED'}


class DisableSceneStrips(Operator):
    bl_idname = 'scene.disable_scene_strips'
    bl_label = 'Disable scene strips'

    mute: BoolProperty(name='Mute', default=True)

    def execute(self, context):
        scene = context.scene
        for strip in scene.sequence_editor.sequences_all:
            if strip.type == 'SCENE':
                strip.mute = self.mute
        return{'FINISHED'}


class SetActiveSceneFromStrip(Operator):
    bl_idname = 'scene.set_active_scene_from_strip'
    bl_label = 'Set active scene from selectip strip'

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            return scene.sequence_editor.active_strip.type == 'SCENE'

    def execute(self, context):
        scene = context.scene
        strip = scene.sequence_editor.active_strip
        context.window.scene = strip.scene
        return{'FINISHED'}


class CreateAdjustmentStrip(Operator):
    bl_idname = 'sequencer.create_adjustment_strip'
    bl_label = 'Create adjustment effect with the active strip range'

    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor:
            return context.scene.sequence_editor.active_strip

    def execute(self, context):
        create_adjustment_strip(context.scene)
        return{'FINISHED'}


class AddMultipleMovies(Operator, ImportHelper):
    bl_idname = 'scene.add_multiple_movies'
    bl_label = 'Add multiple movies'

    filter_glob: StringProperty(default='*.mp4;*.mov;*.mkv;*.ogg;*.ogv')
    files: CollectionProperty(type=OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')
    content_file: BoolProperty(
        name='Content file', default=False,
        description='Using a text file that contains the paths of all videos')

    def execute(self, context):
        if self.content_file:
            with open(self.filepath, 'r') as f:
                filepaths = f.read().split('\n')
        else:
            filepaths = [
                os.path.join(self.directory, f.name) for f in self.files]
        load_multiple_movie_strips(context.scene, filepaths)
        return {'FINISHED'}


class SetStripInputTransform(SetInputTransform):
    bl_idname = 'scene.set_strip_input_transform'
    bl_label = 'Set strip input transform'

    @classmethod
    def poll(cls, context):
        sequences = context.scene.sequence_editor.sequences
        return [s for s in sequences if s.select]

    def get_datablocks(self, context):
        sequences = context.scene.sequence_editor.sequences
        selected_strips = [s for s in sequences if s.select]
        for strip in selected_strips:
            yield strip


class SetStripProxyQuality(Operator):
    bl_idname = 'scene.set_strip_proxy_quality'
    bl_label = 'Set strip proxy quality'

    quality: IntProperty(name='Quality', min=1, max=100, default=100)

    @classmethod
    def poll(cls, context):
        sequences = context.scene.sequence_editor.sequences
        return [s for s in sequences if s.select]

    def execute(self, context):
        sequences = context.scene.sequence_editor.sequences
        selected_strips = [s for s in sequences if s.select]
        for strip in selected_strips:
            set_strip_proxy_quality(strip, self.quality)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
