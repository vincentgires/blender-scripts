import bpy


def set_metadata_overlay(scene, note=None, color=None, size=16):
    color = (0.5, 0.5, 0.5, 1) or None
    scene.render.use_stamp_date = False
    scene.render.use_stamp_time = False
    scene.render.use_stamp_render_time = False
    scene.render.use_stamp_frame = True
    scene.render.use_stamp_frame_range = True
    scene.render.use_stamp_memory = False
    scene.render.use_stamp_hostname = False
    scene.render.use_stamp_camera = False
    scene.render.use_stamp_lens = False
    scene.render.use_stamp_scene = False
    scene.render.use_stamp_marker = False
    scene.render.use_stamp_filename = False
    scene.render.use_stamp_sequencer_strip = False
    scene.render.use_stamp_strip_meta = False
    if note:
        scene.render.use_stamp_note = True
        scene.render.stamp_note_text = note
    scene.render.use_stamp = True
    scene.render.use_stamp_labels = False
    scene.render.stamp_foreground = color
    scene.render.stamp_font_size = size
