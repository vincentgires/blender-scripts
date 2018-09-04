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

# Author : Vincent Gires
# www.vincentgires.com

import bpy


class View3dCustomPanelTools(bpy.types.Panel):
    bl_label = 'Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator('scene.customtools_reset_objects')

        row = col.row(align=True)
        row.label('Name')
        row.operator('scene.customtools_hide_name', text='Hide')
        row.operator('scene.customtools_show_name', text='Show')

        row = col.row(align=True)
        row.label('Wire')
        row.operator('scene.customtools_hide_wire', text='Hide')
        row.operator('scene.customtools_show_wire', text='Show')

        layout.operator('scene.customtools_reset_view')


class CustomToolsResetObjects(bpy.types.Operator):
    bl_idname = 'scene.customtools_reset_objects'
    bl_label = 'Reset objects'
    bl_description = 'Reset location/rotation/scale properties'

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')

    def execute(self, context):
        for obj in context.selected_objects:
            obj.location = (0.0, 0.0, 0.0)
            obj.rotation_euler = (0.0, 0.0, 0.0)
            obj.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            obj.rotation_axis_angle = (1.0, 0.0, 0.0, 0.0)
            obj.scale = (1.0, 1.0, 1.0)

        return{'FINISHED'}


class CustomToolsShowName(bpy.types.Operator):
    bl_idname = 'scene.customtools_show_name'
    bl_label = 'Show name'
    bl_description = 'Show name'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_name = True

        return{'FINISHED'}


class CustomToolsHideName(bpy.types.Operator):
    bl_idname = 'scene.customtools_hide_name'
    bl_label = 'Hide name'
    bl_description = 'Hide name'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_name = False

        return{'FINISHED'}


class CustomToolsShowWire(bpy.types.Operator):
    bl_idname = 'scene.customtools_show_wire'
    bl_label = 'Show wire'
    bl_description = 'Show wire'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_wire = True
            obj.show_all_edges = True

        return{'FINISHED'}


class CustomToolsHideWire(bpy.types.Operator):
    bl_idname = 'scene.customtools_hide_wire'
    bl_label = 'Hide wire'
    bl_description = 'Hide wire'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_wire = False
            obj.show_all_edges = False

        return{'FINISHED'}


class CustomToolsResetView(bpy.types.Operator):
    bl_idname = 'scene.customtools_reset_view'
    bl_label = 'Reset view'

    def execute(self, context):
        # TODO
        print(dir(context.space_data.region_3d))
        print(context.space_data.region_3d.view_rotation)
        print(context.space_data.region_3d.perspective_matrix)

        return{'FINISHED'}
