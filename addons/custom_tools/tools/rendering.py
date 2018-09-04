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
import os
import shutil
import tempfile
from convert import sequence_to_gif


class View3dCustomPanelRendering(bpy.types.Panel):
    bl_label = 'Rendering'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator('scene.customtools_set_object_id')
        col.operator('scene.customtools_set_material_id')


class CustomToolsSetObjectId(bpy.types.Operator):
    bl_idname = 'scene.customtools_set_object_id'
    bl_label = 'Set object ID'
    bl_description = ('Set incremental object ID '
                      'on all mesh objects in the scene')

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')

    def execute(self, context):
        cpt = 1
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.pass_index = cpt
                cpt = cpt + 1

        return{'FINISHED'}


class CustomToolsSetMaterialId(bpy.types.Operator):
    bl_idname = 'scene.customtools_set_material_id'
    bl_label = 'Set material ID'
    bl_description = 'Set incremental material ID on all materials of the file'

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')

    def execute(self, context):
        cpt = 1
        for mat in bpy.data.materials:
            mat.pass_index = cpt
            cpt = cpt + 1

        return{'FINISHED'}


class RenderToGif(bpy.types.Operator):
    bl_idname = 'render.render_gif'
    bl_label = 'Render to GIF'

    def execute(self, context):
        scene = context.scene
        output = scene.render.filepath

        # Set image sequence
        render_tmp = tempfile.mkdtemp()
        scene.render.filepath = os.path.join(render_tmp, 'render.####.png')
        scene.render.image_settings.file_format = 'PNG'

        bpy.ops.render.render(animation=True)
        sequence_to_gif(render_tmp, output, fps=scene.render.fps)

        # Set back settings and clean temporary files
        shutil.rmtree(render_tmp)
        scene.render.filepath = output
        return{'FINISHED'}
