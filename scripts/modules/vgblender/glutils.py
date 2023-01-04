import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader

FONT_SANS = '/usr/share/fonts/TTF/DejaVuSans.ttf'
DPI = 72
TEXT_MARGIN = 10

shader_2d_uniform = (
    gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    if not bpy.app.background else None)


def draw_poly(coords, color, width=1):
    if shader_2d_uniform is not None:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(width)
        batch = batch_for_shader(
            shader_2d_uniform, 'LINE_STRIP', {'pos': coords})
        shader_2d_uniform.bind()
        shader_2d_uniform.uniform_float('color', color)
        batch.draw(shader_2d_uniform)
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)


def draw_line(v1, v2, color, width=1):
    if shader_2d_uniform is not None:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(width)
        coords = [(v1[0], v1[1]), (v2[0], v2[1])]
        batch = batch_for_shader(shader_2d_uniform, 'LINES', {'pos': coords})
        shader_2d_uniform.bind()
        shader_2d_uniform.uniform_float('color', color)
        batch.draw(shader_2d_uniform)
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)


def draw_rectangle(v1, v2, color):
    """v1, v2 are corners: bottom left, top right"""
    if shader_2d_uniform is not None:
        bgl.glEnable(bgl.GL_BLEND)
        vertices = (
            (v1[0], v1[1]), (v2[0], v1[1]),  # bottom left, bottom right
            (v1[0], v2[1]), (v2[0], v2[1]))  # top left, top right
        indices = ((0, 1, 2), (2, 1, 3))
        batch = batch_for_shader(
            shader_2d_uniform, 'TRIS', {'pos': vertices}, indices=indices)
        shader_2d_uniform.bind()
        shader_2d_uniform.uniform_float('color', color)
        batch.draw(shader_2d_uniform)
        bgl.glDisable(bgl.GL_BLEND)


def draw_text(text, position, color, size, font_id):
    bgl.glEnable(bgl.GL_BLEND)
    blf.size(font_id, size, DPI)
    blf.position(font_id, *position)
    blf.color(font_id, *color)
    blf.draw(font_id, text)
    bgl.glDisable(bgl.GL_BLEND)


def draw_text_line(packed_strings, x, y, size, font_id):
    blf.size(font_id, size, DPI)
    x_offset = 0
    for pstr, pcol in packed_strings:
        text_width, text_height = blf.dimensions(font_id, pstr)
        position = (x + x_offset, y, 0)
        draw_text(pstr, position, pcol, size, font_id)
        x_offset += text_width
