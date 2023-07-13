import os
import sys
import bpy
from bpy.app.handlers import persistent
from vgblender.path import normpath
from vgblender.render import render_movie

filepath = normpath(sys.argv[-1])


class ExportMovie(bpy.types.Operator):
    bl_idname = 'render.export_movie'
    bl_label = 'Export movie'

    codec: bpy.props.StringProperty(
        name='codec',
        default='mjpeg')
    qscale: bpy.props.StringProperty(
        name='qscale',
        default='1')
    container: bpy.props.StringProperty(
        name='container',
        default='mkv')

    def execute(self, context):
        scene = context.scene
        dirpath = os.path.dirname(filepath)
        output = os.path.join(dirpath, f'export.{self.container}')
        scene.render.filepath = output
        render_movie(scene, codec=self.codec, qscale=self.qscale)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def render_menu_draw(self, context):
    self.layout.operator('render.export_movie')


def load_file_as_clip():
    if not os.path.exists(filepath):
        return
    scene = bpy.context.scene
    clip = bpy.data.movieclips.load(filepath)
    sequences = scene.sequence_editor.sequences
    sequences.new_clip(
        name=os.path.basename(filepath),
        clip=clip,
        channel=1,
        frame_start=1)
    scene.frame_start = 1
    scene.frame_end = clip.frame_duration
    x, y = clip.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100


@persistent
def load_handler(dummy):
    load_file_as_clip()


def register():
    bpy.utils.register_class(ExportMovie)
    bpy.app.handlers.load_factory_startup_post.append(load_handler)
    bpy.types.TOPBAR_MT_render.append(render_menu_draw)


def unregister():
    bpy.utils.unregister_class(ExportMovie)
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
    bpy.types.TOPBAR_MT_render.remove(render_menu_draw)
