import bpy
import os


class SequencerCustomPanel(bpy.types.Panel):
    bl_idname = 'BLENDERDEV_PT_sequencer_custom_panel'
    bl_label = 'Custom'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout
        layout.operator('scene.open_strip_as_movieclip')
        layout.operator('scene.open_strip_as_compositing')


class OpenStripAsMovieclip(bpy.types.Operator):
    bl_idname = 'BLENDERDEV_PT_open_strip_as_movieclip'
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


class OpenStripAsCompositing(bpy.types.Operator):
    bl_idname = 'BLENDERDEV_PT_open_strip_as_compositing'
    bl_idname = 'scene.open_strip_as_compositing'
    bl_label = 'Open strip as a compositing scene'

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

        return{'FINISHED'}
