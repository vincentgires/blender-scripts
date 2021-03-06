import os
import bpy
import tempfile
import shutil
import subprocess


def render_movie(scene, codec=None, qscale=None, metadatas=None):
    """Wrapper around bpy.ops.render.render()

    Always render as image sequence and convert the result with FFmpeg
    that gives more control (codecs and metadatas).
    """
    codec = codec or 'mjpeg'
    qscale = qscale or '1'

    TEMPORARY_FORMAT = 'JPEG'
    TEMPORARY_EXT = '.jpg'

    output = scene.render.filepath
    render_tmp = tempfile.mkdtemp()
    scene.render.filepath = os.path.join(
        render_tmp, 'render.####' + TEMPORARY_EXT)
    scene.render.image_settings.file_format = TEMPORARY_FORMAT
    scene.render.image_settings.quality = 100

    bpy.ops.render.render(animation=True)

    # Build command to convert image seq to movie
    command = [
        'ffmpeg',
        '-framerate', str(scene.render.fps),
        '-start_number', str(scene.frame_start),
        '-i', '{}/render.%04d'.format(render_tmp) + TEMPORARY_EXT,
        '-c:v', codec]
    if qscale:
        command.extend(['-q:v', qscale])
    if metadatas:
        for md in metadatas:
            command.extend(['-metadata', md])
    command.extend([output, '-y'])

    subprocess.call(command)

    # Remove temp folder
    shutil.rmtree(render_tmp)
    scene.render.filepath = output
