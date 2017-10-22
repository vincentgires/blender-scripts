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


## PANEL ##
###########


class View3dCustomPanelMaterial(bpy.types.Panel):
    bl_label = 'Material'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        layout.operator('scene.customtools_set_material')


## OPERATOR ##
##############


class CustomToolsSetMeterial(bpy.types.Operator):
    bl_idname = 'scene.customtools_set_material'
    bl_label = 'Set material'
    
    apply = bpy.props.EnumProperty(
        items=(
            ('selected', 'Selected', 'Selected object'),
            ('active', 'Active', 'Active object'),
            ),
        name='Apply'
        )
    
    
    def item_cb(self, context):
        return [(mat.name, mat.name, '') for mat in self.material_item]
    
    material_enum = bpy.props.EnumProperty(items=item_cb, name='Material')
    material_item = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup, name='number')
    
    def execute(self, context):
        if len(self.material_item) > 0:
            material = bpy.data.materials[self.material_enum]
            print (material)
            
        return {'FINISHED'}

    def invoke(self, context, event):
        
        self.material_item.clear()
        for material in bpy.data.materials:
            self.material_item.add().name = material.name
            
        return context.window_manager.invoke_props_dialog(self)
        #return context.window_manager.invoke_search_popup(self)

