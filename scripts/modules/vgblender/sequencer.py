import bpy
import os
from .path import normpath

DEFAULT_CHANNEL = 1
DEFAULT_BLEND_TYPE = 'REPLACE'
DEFAULT_LENGTH = 24


def is_available_sequences(scene):
    if not scene.sequence_editor:
        return False
    sequences = scene.sequence_editor.sequences
    if sequences:
        return True


def enable_sequence_editor(scene):
    if not scene.sequence_editor:
        scene.sequence_editor_create()


def clean_sequencer(scene):
    if not scene.sequence_editor:
        return
    sequences = scene.sequence_editor.sequences
    for seq in sequences:
        sequences.remove(seq)


def get_current_strip(scene):
    frame_current = scene.frame_current
    if not scene.sequence_editor:
        return None
    for strip in scene.sequence_editor.sequences:
        frame_end = strip.frame_start + strip.frame_final_duration
        if strip.frame_start <= frame_current < frame_end:
            if strip.channel == DEFAULT_CHANNEL:
                return strip


def get_current_strips(scene):
    def frame_end(strip):
        return strip.frame_start + strip.frame_final_duration
    frame_current = scene.frame_current
    if not scene.sequence_editor:
        return None
    strips = [
        strip for strip in scene.sequence_editor.sequences_all
        if strip.frame_start <= frame_current < frame_end(strip)]
    return strips


def get_first_strip(scene):
    if not is_available_sequences(scene):
        return
    sequences = scene.sequence_editor.sequences
    first_strip = sequences[0]
    for strip in sequences:
        if strip.frame_start < first_strip.frame_start:
            first_strip = strip
    return first_strip


def get_last_strip(scene):
    if not is_available_sequences(scene):
        return
    sequences = scene.sequence_editor.sequences
    last_strip = sequences[0]
    for strip in sequences:
        if strip.frame_start > last_strip.frame_start:
            last_strip = strip
    return last_strip


def set_frame_range(scene):
    first_strip = get_first_strip(scene)
    last_strip = get_last_strip(scene)
    if first_strip and last_strip:
        scene.frame_start = first_strip.frame_start
        scene.frame_end = last_strip.frame_final_end - 1


def _get_next_frame_start(scene):
    last_strip = get_last_strip(scene)
    frame_start = (
        last_strip.frame_start + last_strip.frame_final_duration
        if last_strip else 1)
    return frame_start


def load_image_strip(
        scene, image, channel=DEFAULT_CHANNEL,
        blend_type=DEFAULT_BLEND_TYPE, length=DEFAULT_LENGTH):
    sequences = scene.sequence_editor.sequences
    strip = sequences.new_image(
        name=os.path.basename(image),
        filepath=normpath(image),
        channel=channel,
        frame_start=_get_next_frame_start(scene))
    strip.select = False
    strip.blend_type = blend_type
    strip.frame_final_duration = length
    return strip


def load_image_sequence_strip(
        scene, images, channel=DEFAULT_CHANNEL, blend_type=DEFAULT_BLEND_TYPE):
    sequences = scene.sequence_editor.sequences
    first_frame = images[0]
    strip = sequences.new_image(
        name=os.path.basename(first_frame),
        filepath=normpath(first_frame),
        channel=channel,
        frame_start=_get_next_frame_start(scene))
    for image in images[1:]:
        name = os.path.basename(image)
        strip.elements.append(name)
    strip.select = False
    strip.blend_type = blend_type
    return strip


def load_movie_strip(
        scene, moviepath,
        channel=DEFAULT_CHANNEL, blend_type=DEFAULT_BLEND_TYPE):
    sequences = scene.sequence_editor.sequences
    strip = sequences.new_movie(
        name=os.path.basename(moviepath),
        filepath=normpath(moviepath),
        channel=channel,
        frame_start=_get_next_frame_start(scene))
    strip.select = False
    strip.blend_type = blend_type
    return strip


def load_sound_strip(
        scene, soundpath, channel=DEFAULT_CHANNEL, frame_start=None):
    sequences = scene.sequence_editor.sequences
    frame_start = frame_start or _get_next_frame_start(scene)
    strip = sequences.new_sound(
        name=os.path.basename(soundpath),
        filepath=normpath(soundpath),
        channel=channel,
        frame_start=frame_start)
    strip.select = False
    return strip


def load_multiple_movie_strips(scene, filepaths):
    for path in filepaths:
        if not os.path.exists(path):
            continue
        movie_strip = load_movie_strip(scene, path)
        sound_channel = movie_strip.channel + 1
        sound_frame_start = movie_strip.frame_start
        load_sound_strip(
            scene, path, channel=sound_channel, frame_start=sound_frame_start)


def create_adjustment_strip(scene):
    active_strip = scene.sequence_editor.active_strip
    if not active_strip:
        return
    sequences = scene.sequence_editor.sequences
    strip = sequences.new_effect(
        name='Adjustment',
        type='ADJUSTMENT',
        channel=active_strip.channel + 1,
        frame_start=active_strip.frame_start,
        frame_end=active_strip.frame_start + active_strip.frame_final_duration)
    strip.select = True
    scene.sequence_editor.active_strip = strip
    return strip


def set_strip_colorspace(strip, colorspace):
    colorspace_settings = getattr(strip, 'colorspace_settings', None)
    if colorspace_settings:
        colorspace_settings.name = colorspace


def set_strip_proxy_quality(strip, quality):
    if getattr(strip, 'proxy', None):
        strip.proxy.quality = quality


def view_zoom_preview(context):
    scene = context.scene
    for region in context.area.regions:
        if region.type == 'PREVIEW':
            width = region.width
            height = region.height
            rv1 = region.view2d.region_to_view(0, 0)
            rv2 = region.view2d.region_to_view(width - 1, height - 1)
            res_percentage = scene.render.resolution_percentage
            zoom = (1 / (width / (rv2[0] - rv1[0]))) / (res_percentage / 100)
            return zoom


def normalise_mouse_position(context, position):
    """Normalise coordinates between 0 and 1"""
    scene = context.scene
    region = context.region
    position_x, position_y = position
    mouse_x, mouse_y = region.view2d.region_to_view(
        position_x - region.x,
        position_y - region.y)
    mouse_x += (scene.render.resolution_x / 2)
    mouse_y += (scene.render.resolution_y / 2)
    x = mouse_x / scene.render.resolution_x
    y = mouse_y / scene.render.resolution_y
    return (x, y)
