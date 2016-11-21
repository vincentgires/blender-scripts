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

class VIEW3D_custom_panel_tools(bpy.types.Panel):
    bl_label = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Custom"
    
    
    def draw(self, context):
        layout = self.layout
        layout.operator("reset_object.btn")
        
        row = layout.row(align=True)
        row.label("Name")
        row.operator("hide_name.btn", text="Hide")
        row.operator("show_name.btn", text="Show")
        
        row = layout.row(align=True)
        row.label("Wire")
        row.operator("hide_wire.btn", text="Hide")
        row.operator("show_wire.btn", text="Show")
        
        layout.operator("reset_view.btn")


## OPERATOR ##
##############


class custom_tools_reset_object(bpy.types.Operator):
    bl_idname = "reset_object.btn"
    bl_label = "Reset object"
    bl_description = "Reset location/rotation/scale properties"
    
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


class custom_tools_show_name(bpy.types.Operator):
    bl_idname = "show_name.btn"
    bl_label = "Show name"
    bl_description = "Show name"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_name = True
        
        return{'FINISHED'}
    
class custom_tools_hide_name(bpy.types.Operator):
    bl_idname = "hide_name.btn"
    bl_label = "Hide name"
    bl_description = "Hide name"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_name = False
        
        return{'FINISHED'}

class custom_tools_show_wire(bpy.types.Operator):
    bl_idname = "show_wire.btn"
    bl_label = "Show wire"
    bl_description = "Show wire"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_wire = True
            obj.show_all_edges = True
        
        return{'FINISHED'}
    
class custom_tools_hide_wire(bpy.types.Operator):
    bl_idname = "hide_wire.btn"
    bl_label = "Hide wire"
    bl_description = "Hide wire"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.show_wire = False
            obj.show_all_edges = False
        
        return{'FINISHED'}


class custom_tools_reset_view(bpy.types.Operator):
    bl_idname = "reset_view.btn"
    bl_label = "Reset view"
    
    
    def execute(self, context):
        
        print (dir(context.space_data.region_3d))
        print (context.space_data.region_3d.view_rotation)
        print (context.space_data.region_3d.perspective_matrix)
        
        return{'FINISHED'}





## REGISTRATION ##
##################




def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
