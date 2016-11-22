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

class VIEW3D_custom_panel_cache(bpy.types.Panel):
    bl_label = "Cache"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Custom"
    
    
    def draw(self, context):
        layout = self.layout
        layout.operator("ptcache.bake_all", text="Bake All Dynamics").bake = True
        layout.operator("ptcache.free_bake_all", text="Free All Bakes")
        layout.operator("ptcache.bake_all", text="Update All To Frame").bake = False


