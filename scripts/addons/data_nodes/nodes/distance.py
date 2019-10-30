import bpy
import bgl
import math
from bpy.types import NodeTree, Node, NodeSocket
from ..utils import send_value


def draw_distance_opengl(self, context):
    bgl.glPointSize(10)
    bgl.glColor3f(1.0, 0.0, 0.0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex3f(1.0, 1.0, 1.0)
    bgl.glEnd()
    bgl.glPointSize(50)
    bgl.glColor3f(0.0, 0.0, 1.0)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex3f(-1.0, 0.0, 2.0)
    bgl.glEnd()

    # Restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class DistanceNode(Node):
    """Distance node"""
    bl_idname = 'DistanceNodeType'
    bl_label = 'Distance'

    display = bpy.props.BoolProperty(name='display', default=True)
    opengl_handle = [None]

    def init(self, context):
        self.inputs.new('NodeSocketVector', 'VectorA')
        self.inputs.new('NodeSocketVector', 'VectorB')
        self.outputs.new('NodeSocketFloat', 'Distance')
        self.opengl_handle[0] = bpy.types.SpaceView3D.draw_handler_add(
            draw_distance_opengl, (self, context), 'WINDOW', 'POST_VIEW')

    def update(self):
        if len(self.inputs) >= 2:
            a = self.inputs['VectorA'].default_value
            b = self.inputs['VectorB'].default_value
            distance = math.sqrt(
                (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)
            send_value(self.outputs, distance)

    def free(self):
        bpy.types.SpaceView3D.draw_handler_remove(
            self.opengl_handle[0], 'WINDOW')

    def draw_label(self):
        return 'Distance'
