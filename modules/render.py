import bpy
import os
import shutil
import tempfile
import subprocess


def render_gif(context, output=None):
    scene = context.scene
    if not output:
        output = scene.render.filepath

    # Set image sequence
    render_tmp = tempfile.mkdtemp()
    scene.render.filepath = os.path.join(render_tmp, 'render.####.png')
    scene.render.image_settings.file_format = 'PNG'

    # Render
    bpy.ops.render.render(animation=True)

    # Convert image sequence to gif
    fps = '1x{}'.format(scene.render.fps)
    command = [
        'magick',
        '-delay', fps,
        '-loop', '0']
    input_path = os.path.join(render_tmp, 'render.*.png')
    command.append(input_path)
    command.append(output)
    subprocess.call(command)

    # Remove temp folder
    shutil.rmtree(render_tmp)

    # Put settings back
    scene.render.filepath = output
