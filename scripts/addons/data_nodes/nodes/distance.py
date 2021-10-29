import bpy
import bgl
import math
from bpy.types import Node, SpaceView3D
from ..utils import send_value
import gpu
from gpu_extras.batch import batch_for_shader

shader_3d_uniform = (
    gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    if not bpy.app.background else None)
draw_handler = {}


def draw_line(v1, v2, color, width=2):
    if shader_3d_uniform is None:
        return
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(width)
    coords = [(v1[0], v1[1], v1[2]), (v2[0], v2[1], v2[2])]
    batch = batch_for_shader(shader_3d_uniform, 'LINES', {'pos': coords})
    shader_3d_uniform.bind()
    shader_3d_uniform.uniform_float('color', color)
    batch.draw(shader_3d_uniform)
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)


def draw_distance_opengl(node, context):
    a = tuple(node.inputs['VectorA'].default_value)
    b = tuple(node.inputs['VectorB'].default_value)
    draw_line(a, b, (1.0, 1.0, 1.0))


def _force_redraw_view3d():
    for area in bpy.context.screen.areas:
        if area.type in 'VIEW_3D':
            area.tag_redraw()


class DistanceNode(Node):
    """Distance node"""
    bl_idname = 'DistanceNodeType'
    bl_label = 'Distance'

    def _set_draw_handler(self):
        # Use memory address to get unique key used in draw handler
        if self.as_pointer() in draw_handler:
            return
        draw_handler[self.as_pointer()] = SpaceView3D.draw_handler_add(
            draw_distance_opengl, (self, bpy.context), 'WINDOW', 'POST_VIEW')

    def init(self, context):
        self.inputs.new('NodeSocketVector', 'VectorA')
        self.inputs.new('NodeSocketVector', 'VectorB')
        self.outputs.new('NodeSocketFloat', 'Distance')
        self._set_draw_handler()

    def update(self):
        self._set_draw_handler()
        if len(self.inputs) >= 2:
            a = self.inputs['VectorA'].default_value
            b = self.inputs['VectorB'].default_value
            distance = math.sqrt(
                (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)
            send_value(self.outputs, distance)
            _force_redraw_view3d()

    def copy(self, node):
        self._set_draw_handler()

    def free(self):
        SpaceView3D.draw_handler_remove(
            draw_handler[self.as_pointer()], 'WINDOW')
        _force_redraw_view3d()

    def draw_label(self):
        return 'Distance'
