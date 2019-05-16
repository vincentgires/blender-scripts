# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader

bl_info = {
    'name': 'Point Cloud',
    'author': 'Vincent Girès',
    'description': 'Generate cloud of vertices based on the position pass',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'location': 'Tool shelves (3D View, Image Editor)',
    'category': '3D View'}

pointcloud = {
    'coords': [],  # reduced pixels for faster display
    'colors': [],
    'coords_full': [],  # full pixels from the image
    'colors_full': [],
    'shader': gpu.shader.from_builtin('3D_FLAT_COLOR'),
    'batch': None}

RGBA_STEP = 4  # image pixels gives 4 values for each pixel (r, g, b, a)
XYZ_STEP = 3  # mesh creation needs only position values (x, y, z)


def redraw_view_3d():
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def batch_pointcloud():
    pointcloud['batch'] = batch_for_shader(
        pointcloud['shader'], 'POINTS',
        {'pos': pointcloud['coords'], 'color': pointcloud['colors']})


def callback_point_detail(self, context):
    detail = self.point_detail
    length_full = len(pointcloud['coords_full'])
    length_detail = length_full * detail
    step = length_full / length_detail
    step = int(step)
    pointcloud['coords'] = pointcloud['coords_full'][::step]
    pointcloud['colors'] = pointcloud['colors_full'][::step]
    batch_pointcloud()


class PointCloudProperties(bpy.types.PropertyGroup):
    color_pass: bpy.props.StringProperty(
        name='Color pass')
    position_pass: bpy.props.StringProperty(
        name='Position pass')
    point_detail: bpy.props.FloatProperty(
        name='Detail',
        default=0.25,
        min=0.001,
        max=1.0,
        update=callback_point_detail)
    point_size: bpy.props.IntProperty(
        name='Size',
        default=1,
        min=1)


def draw_cloud():
    context = bpy.context
    scene = context.scene
    if pointcloud['batch']:
        pointcloud['shader'].bind()
        size = scene.point_cloud.point_size
        bgl.glPointSize(size)
        pointcloud['batch'].draw(pointcloud['shader'])


def get_positions(context):
    scene = context.scene
    data = bpy.data
    position_src = scene.point_cloud.position_pass
    position_data = data.images[position_src]
    position_pixels = list(position_data.pixels)

    context.window.cursor_set('WAIT')
    coordinates = []
    for i in range(0, len(position_pixels), RGBA_STEP):
        pixel_rgb = []
        for j in range(XYZ_STEP):
            pixel_rgb.append(position_pixels[i + j])
        coordinates.append(pixel_rgb)
    context.window.cursor_set('DEFAULT')

    return coordinates


def set_coordinates_and_colors(context):
    scene = context.scene
    data = bpy.data
    position_src = scene.point_cloud.position_pass
    color_src = scene.point_cloud.color_pass
    position_data = data.images[position_src]
    color_data = data.images[color_src]
    position_pixels = list(position_data.pixels)
    color_pixels = list(color_data.pixels)

    context.window.cursor_set('WAIT')
    pixels = list(zip(position_pixels, color_pixels))
    for i in range(0, len(pixels), RGBA_STEP):
        pixel_position = []
        pixel_color = []
        for j in range(RGBA_STEP):
            position, color = pixels[i + j]
            if j < XYZ_STEP:
                pixel_position.append(position)
            pixel_color.append(color)
        pointcloud['coords_full'].append(pixel_position)
        pointcloud['colors_full'].append(pixel_color)

    pointcloud['coords'] = pointcloud['coords_full']
    pointcloud['colors'] = pointcloud['colors_full']
    context.window.cursor_set('DEFAULT')

    redraw_view_3d()


def create_mesh(name, origin, verts, edges, faces):
    me = bpy.data.meshes.new(name + 'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    bpy.context.scene.collection.objects.link(ob)
    me.from_pydata(verts, edges, faces)
    me.update(calc_edges=True)
    return ob


class ScenePropertiesPanel(bpy.types.Panel):
    bl_idname = 'POINTCLOUD_PT_ScenePropertiesPanel'
    bl_label = 'Point Cloud'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        data = bpy.data
        layout = self.layout

        col = layout.column(align=True)
        col.prop_search(
            scene.point_cloud, 'position_pass',
            data, 'images', icon='FILE_IMAGE')
        col.prop_search(
            scene.point_cloud, 'color_pass',
            data, 'images', icon='FILE_IMAGE')

        col = layout.column(align=True)
        row = col.row(align=True)
        text = 'Update cloud' if pointcloud['coords'] else 'Generate cloud'
        row.operator('scene.pointcloud_generate', text=text)
        row.operator('scene.pointcloud_clear', text='', icon='PANEL_CLOSE')
        col.prop(scene.point_cloud, 'point_detail', slider=True)
        col.prop(scene.point_cloud, 'point_size')
        col.operator('scene.pointcloud_generate_mesh')


class PointCloudGenerateOpenGl(bpy.types.Operator):
    bl_idname = 'scene.pointcloud_generate'
    bl_label = 'Generate cloud'
    bl_description = 'Generate cloud of point based on the position pass'

    @classmethod
    def poll(cls, context):
        position = context.scene.point_cloud.position_pass
        color = context.scene.point_cloud.color_pass
        return position and color

    def execute(self, context):
        scene = context.scene
        set_coordinates_and_colors(context)
        batch_pointcloud()
        return{'FINISHED'}


class PointCloudClearOpenGl(bpy.types.Operator):
    bl_idname = 'scene.pointcloud_clear'
    bl_label = 'Clear'
    bl_description = 'Remove cloud from the viewport'

    @classmethod
    def poll(cls, context):
        return pointcloud['coords']

    def execute(self, context):
        pointcloud['coords'].clear()
        pointcloud['colors'].clear()
        pointcloud['batch'] = None
        redraw_view_3d()
        return{'FINISHED'}


class PointCloudGenerateMesh(bpy.types.Operator):
    bl_idname = 'scene.pointcloud_generate_mesh'
    bl_label = 'Create mesh'
    bl_description = 'Generate cloud of vertices based on the position pass'

    @classmethod
    def poll(cls, context):
        position = context.scene.point_cloud.position_pass
        return position

    def execute(self, context):
        scene = context.scene
        coordinates = get_positions(context)
        origin = (0, 0, 0)
        position_objects = create_mesh(
            'Position_Cloud', origin, coordinates, [], [])
        return{'FINISHED'}


draw_handler = {}
classes = (
    PointCloudProperties,
    ScenePropertiesPanel,
    PointCloudGenerateOpenGl,
    PointCloudClearOpenGl,
    PointCloudGenerateMesh)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.point_cloud = \
        bpy.props.PointerProperty(type=PointCloudProperties)
    draw_handler['cloud'] = bpy.types.SpaceView3D.draw_handler_add(
        draw_cloud, (), 'WINDOW', 'POST_VIEW')


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.point_cloud
    bpy.types.SpaceView3D.draw_handler_remove(
        draw_handler['cloud'], 'WINDOW')


if __name__ == '__main__':
    register()
