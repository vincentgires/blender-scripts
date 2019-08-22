import bpy
import os
from .path import normpath

DEFAULT_CHANNEL = 1
DEFAULT_BLEND_TYPE = 'REPLACE'
DEFAULT_LENGTH = 24


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


def get_first_strip(scene):
    # TODO: add decorator for this check
    if not scene.sequence_editor:
        return
    sequences = scene.sequence_editor.sequences
    if not sequences:
        return
    # TODO ---
    sequences = scene.sequence_editor.sequences
    first_strip = sequences[0]
    for strip in sequences:
        if strip.frame_start < first_strip.frame_start:
            first_strip = strip
    return first_strip


def get_last_strip(scene):
    # TODO: add decorator for this check
    if not scene.sequence_editor:
        return
    sequences = scene.sequence_editor.sequences
    if not sequences:
        return
    # TODO ---
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
