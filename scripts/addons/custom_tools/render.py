import bpy
import os
import shutil
import tempfile
from vgenc.convert import convert_to_gif


class RenderToGif(bpy.types.Operator):
    bl_idname = 'render.render_gif'
    bl_label = 'Render to GIF'

    depth: bpy.props.IntProperty(
        name='Depth',
        default=8)
    optimize: bpy.props.BoolProperty(
        name='Optimize',
        default=True)
    bounce: bpy.props.BoolProperty(
        name='Bounce',
        default=False)

    def execute(self, context):
        scene = context.scene
        output = bpy.path.abspath(scene.render.filepath)

        # Set image sequence
        render_tmp = tempfile.mkdtemp()
        scene.render.filepath = os.path.join(render_tmp, 'render.####.png')
        scene.render.image_settings.file_format = 'PNG'

        bpy.ops.render.render(animation=True)
        convert_to_gif(
            render_tmp, output, fps=scene.render.fps,
            optimize=self.optimize, depth=self.depth, bounce=self.bounce)

        # Set back settings and clean temporary files
        shutil.rmtree(render_tmp)
        scene.render.filepath = output
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
