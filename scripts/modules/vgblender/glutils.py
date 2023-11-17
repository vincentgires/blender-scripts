import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader


shader_uniform_color = (
    gpu.shader.from_builtin('UNIFORM_COLOR')
    if not bpy.app.background else None)
shader_polyline_uniform_color = (
    gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    if not bpy.app.background else None)


def draw_poly(coords, color, width=1):
    shader = shader_polyline_uniform_color
    if shader is not None:
        batch = batch_for_shader(shader, 'LINE_STRIP', {'pos': coords})
        shader.bind()
        shader.uniform_float('lineWidth', width)
        shader.uniform_float('viewportSize', gpu.state.viewport_get()[2:])
        shader.uniform_float('color', color)
        batch.draw(shader)


def draw_line(v1, v2, color, width=1):
    shader = shader_polyline_uniform_color
    if shader is not None:
        coords = [(v1[0], v1[1]), (v2[0], v2[1])]
        batch = batch_for_shader(shader, 'LINES', {'pos': coords})
        shader.bind()
        shader.uniform_float('lineWidth', width)
        shader.uniform_float('viewportSize', gpu.state.viewport_get()[2:])
        shader.uniform_float('color', color)
        batch.draw(shader)


def draw_rectangle(v1, v2, color):
    """v1, v2 are corners: bottom left, top right"""
    shader = shader_uniform_color
    if shader is not None:
        vertices = (
            (v1[0], v1[1]), (v2[0], v1[1]),  # bottom left, bottom right
            (v1[0], v2[1]), (v2[0], v2[1]))  # top left, top right
        indices = ((0, 1, 2), (2, 1, 3))
        batch = batch_for_shader(
            shader, 'TRIS', {'pos': vertices}, indices=indices)
        shader.bind()
        shader.uniform_float('color', color)
        batch.draw(shader)


def draw_text(text, position, color, size, font_id):
    blf.size(font_id, int(size))
    blf.position(font_id, *position)
    blf.color(font_id, *color)
    blf.draw(font_id, text)


def draw_text_line(packed_strings, x, y, size, font_id):
    blf.size(font_id, size)
    x_offset = 0
    for pstr, pcol in packed_strings:
        text_width, text_height = blf.dimensions(font_id, pstr)
        position = (x + x_offset, y, 0)
        draw_text(pstr, position, pcol, size, font_id)
        x_offset += text_width
