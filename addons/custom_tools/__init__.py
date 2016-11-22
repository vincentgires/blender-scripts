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




### A FAIRE :
### - To EMPTY EN rotation object
### - trouver comment mettre les keymap du node editor dans fichier node.py et pas init.py



bl_info = {
    "name": "Custom tools",
    "author": "Vincent Gires",
    "description": "---",
    "version": (0, 0, 1),
    "blender": (2, 7, 6),
    "location": "Tool shelves (3D View, Image Editor)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}



import bpy


from custom_tools.tools import object
from custom_tools.tools import rendering
from custom_tools.tools import material
from custom_tools.tools import lighting
from custom_tools.tools import animation
from custom_tools.tools import look_through
from custom_tools.tools import node
from custom_tools.tools import image
from custom_tools.tools import cache
from custom_tools.tools import sequencer




## HEADER ##
############


def header_color_management(self, context):
    layout = self.layout
    layout.operator("reset_exposure.btn", emboss=False, text="Exposure")
    layout.prop(context.scene.view_settings, "exposure", emboss=False, text="")
    layout.operator("reset_gamma.btn", emboss=False, text="Gamma")
    layout.prop(context.scene.view_settings, "gamma", emboss=False, text="")


## OPERATOR ##
##############


class custom_tools_reset_exposure(bpy.types.Operator):
    bl_idname = "reset_exposure.btn"
    bl_label = "Reset Exposure"
    
    
    def execute(self, context):
        context.scene.view_settings.exposure = 0
        
        return{'FINISHED'}

class custom_tools_reset_gamma(bpy.types.Operator):
    bl_idname = "reset_gamma.btn"
    bl_label = "Reset Gamma"
    
    
    def execute(self, context):
        context.scene.view_settings.gamma = 1
        
        return{'FINISHED'}





## REGISTRATION ##
##################



KEYMAPS = list()

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_HT_header.append(header_color_management)
    
    ### KEYMAPS ###
    kc = bpy.context.window_manager.keyconfigs.addon
    
    km = kc.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
    kmi = km.keymap_items.new("node.double_click", "ACTIONMOUSE", "DOUBLE_CLICK")
    KEYMAPS.append((km, kmi))
    
    km = kc.keymaps.new(name="Window", space_type="EMPTY")
    kmi = km.keymap_items.new("compo_node_transform_grab.call", "G", "PRESS")
    KEYMAPS.append((km, kmi))
    
    
    
    
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_HT_header.remove(header_color_management)
    
    ### KEYMAPS ###
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()

if __name__ == "__main__":
    register()
