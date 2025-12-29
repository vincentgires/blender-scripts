import os
import bpy
import tempfile
import shutil
import subprocess


def set_render_settings(
        scene: bpy.types.Scene,
        look: str | None = None,
        display_view: tuple[str, str] | None = None,
        file_format: str | None = None,
        color_mode: str | None = None,
        color_depth: int | None = None,
        compression: int | None = None,
        quality: int | None = None,
        codec: str | None = None,
        additional_image_settings: dict | None = None,
        resolution: tuple[int, int] | None = None):
    codec_attributes = {
        'JPEG2000': 'jpeg2k_codec',
        'OPEN_EXR': 'exr_codec',
        'OPEN_EXR_MULTILAYER': 'exr_codec',
        'TIFF': 'tiff_codec'}
    if look is not None:
        scene.view_settings.look = look
    if display_view is not None:
        display, view = display_view
        scene.display_settings.display_device = display
        scene.view_settings.view_transform = view
    image_settings = scene.render.image_settings
    if file_format is not None:
        image_settings.file_format = file_format.upper()
    if color_mode is not None:
        image_settings.color_mode = color_mode.upper()
    if color_depth is not None:
        image_settings.color_depth = str(color_depth)
    if compression is not None:
        image_settings.compression = compression
    if quality is not None:
        image_settings.quality = quality
    if codec is not None:
        if codec_attribute := codec_attributes.get(
                image_settings.file_format):
            setattr(image_settings, codec_attribute, codec.upper())
    if additional_image_settings is not None:
        for k, v in additional_image_settings.items():
            setattr(image_settings, k, v)
    if resolution is not None:
        x, y = resolution
        scene.render.resolution_x = x
        scene.render.resolution_y = y
        scene.render.resolution_percentage = 100


def render_movie(scene, codec=None, qscale=None, metadata=None):
    """Wrapper around bpy.ops.render.render()

    Always render as image sequence and convert the result with FFmpeg
    that gives more control (codecs and metadata).
    """
    codec = codec or 'mjpeg'

    tmp_format = 'JPEG'
    tmp_ext = '.jpg'

    output = scene.render.filepath
    render_tmp = tempfile.mkdtemp()
    scene.render.filepath = os.path.join(
        render_tmp, 'render.####' + tmp_ext)
    scene.render.image_settings.file_format = tmp_format
    scene.render.image_settings.quality = 100

    bpy.ops.render.render(animation=True)

    # Build command to convert image seq to movie
    command = [
        'ffmpeg',
        '-framerate', str(scene.render.fps),
        '-start_number', str(scene.frame_start),
        '-i', '{}/render.%04d'.format(render_tmp) + tmp_ext,
        '-c:v', codec]
    if qscale is not None:
        command.extend(['-q:v', qscale])
    if metadata is not None:
        for md in metadata:
            command.extend(['-metadata', md])
    command.extend([output, '-y'])

    subprocess.call(command)

    # Remove temp folder
    shutil.rmtree(render_tmp)
    scene.render.filepath = output
