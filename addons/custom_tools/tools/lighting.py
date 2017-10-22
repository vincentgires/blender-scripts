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
import mathutils
import math
from bpy_extras import view3d_utils


## PANEL ##
###########


class View3dCustomPanelLightingTools(bpy.types.Panel):
    bl_label = 'Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Lighting'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        object_aim_btn = col.operator('scene.customtools_aim_normal', icon='MAN_TRANS')
        object_aim_btn.object_name = context.scene.objects.active.name
        object_look_through_btn = col.operator('scene.customtools_look_through', icon='FORWARD')
        object_look_through_btn.object_name = context.scene.objects.active.name


class View3dCustomPanelLightingLights(bpy.types.Panel):
    bl_label = 'Lights'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Lighting'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        layout.operator('scene.customtools_select_all_lights')
        
        ### WORLD ###
        #############
        if scene.world:
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            
            row.label(scene.world.name)
            row.label('', icon='WORLD')
            
            if scene.world.use_nodes:
                for node in scene.world.node_tree.nodes:
                    if node.type == 'BACKGROUND':
                        row = col.row(align=True)
                        
                        ### COLOR ###
                        if not node.inputs['Color'].is_linked:
                            row.prop(node.inputs['Color'], 'default_value', text='')
                        else:
                            row.label('Connected')
                            
                        ### STRENGHT ###
                        if not node.inputs['Strength'].is_linked:
                            row.prop(node.inputs['Strength'], 'default_value', text='Strength')
                        else:
                            row.label('Connected')
            else:
                col.prop(context.scene.world, 'use_nodes')
                col.prop(scene.world, 'horizon_color', text='')
        
        ### LAMPS ###
        #############
        for obj in scene.objects:
            if obj.type == 'LAMP':
                box = layout.box()
                
                col = box.column(align=True)
                row = col.row(align=True)
                
                if obj == context.active_object:
                    row.label('', icon='TRIA_RIGHT')
                
                light_select_btn = row.operator('scene.customtools_select_light', text=obj.name)
                light_select_btn.light_name = obj.name
                light_aim_btn = row.operator('scene.customtools_aim_normal', text='', icon='MAN_TRANS')
                light_aim_btn.object_name = obj.name
                look_through_btn = row.operator('scene.customtools_look_through', text='', icon='FORWARD')
                look_through_btn.object_name = obj.name
                
                row.prop(obj.data, 'type', expand=False, icon='LAMP_'+obj.data.type, text='', icon_only=True)
                
                if obj.data.type == 'AREA':
                    row = col.row(align=True)
                    row.prop(obj.data, 'size', text='X')
                    row.prop(obj.data, 'size_y', text='Y')
                else:
                    col.prop(obj.data, 'shadow_soft_size', text='Size')
                
                if obj.data.type == 'SPOT':
                    row = col.row(align=True)
                    row.prop(obj.data, 'spot_size', text='Spot Size', slider=True)
                    row.prop(obj.data, 'spot_blend', text='Blend', slider=True)
                    
                
                if obj.data.use_nodes:
                    for node in obj.data.node_tree.nodes:
                        if node.type == 'EMISSION':
                            row = col.row(align=True)
                            
                            ### COLOR ###
                            if not node.inputs['Color'].is_linked:
                                row.prop(node.inputs['Color'], 'default_value', text='')
                            else:
                                row.label('Connected')
                                
                            ### STRENGHT ###
                            if not node.inputs['Strength'].is_linked:
                                row.prop(node.inputs['Strength'], 'default_value', text='')
                            else:
                                row.label('Connected')
                                
                else:
                    col.prop(obj.data, 'use_nodes')
                    col.prop(obj.data, 'color')
            
            
        ### EMISSION MATERIAL ###
        #########################
        
        # scan all material with emission shader
        emission_material = []
        for material in bpy.data.materials:
            if material.use_nodes:
                node_tree = material.node_tree
                for node in node_tree.nodes:
                    if node.type == 'EMISSION':
                        emission_material.append(material)
                        break
        
        # display in tool shelf
        for material in emission_material:
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(material.name)
            row.label('', icon='MATERIAL')
            
            node_tree = material.node_tree
            for node in node_tree.nodes:
                if node.type == 'EMISSION':
                    row = col.row(align=True)
                    
                    ### COLOR ###
                    if not node.inputs['Color'].is_linked:
                        row.prop(node.inputs['Color'], 'default_value', text='')
                    else:
                        row.label('Connected')
                        
                    ### STRENGHT ###
                    if not node.inputs['Strength'].is_linked:
                        row.prop(node.inputs['Strength'], 'default_value', text='')
                    else:
                        row.label('Connected')


## OPERATOR ##
##############


class CustomToolsSelectAllLights(bpy.types.Operator):
    bl_idname = 'scene.customtools_select_all_lights'
    bl_label = 'Select all lights'
    bl_description = 'Select all lights of the scene'
    
    
    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type == 'LAMP':
                obj.select = True
            else:
                obj.select = False
        
        return{'FINISHED'}


class CustomToolsSelectLight(bpy.types.Operator):
    bl_idname = 'scene.customtools_select_light'
    bl_label = 'Select light'
    bl_description = 'Select light from the tool shelf'
    
    # Properties
    light_name = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')
    
    def execute(self, context):
        for obj in context.scene.objects:
            if obj.name == self.light_name:
                obj.select = True
                context.scene.objects.active = obj
            else:
                obj.select = False
        
        return{'FINISHED'}


def aim_normal(context, event, object_name, ray_max=1000.0, offset=-1):
    '''Run this function on left mouse, execute the ray cast'''
    
    object = context.scene.objects[object_name]
    
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + (view_vector * ray_max)
    
    def visible_objects_and_duplis():
        '''Loop over (object, matrix) pairs (mesh only)'''

        for obj in context.visible_objects:
            if obj.type == 'MESH':
                yield (obj, obj.matrix_world.copy())

            if obj.dupli_type != 'NONE':
                obj.dupli_list_create(scene)
                for dob in obj.dupli_list:
                    obj_dupli = dob.object
                    if obj_dupli.type == 'MESH':
                        yield (obj_dupli, dob.matrix.copy())

            obj.dupli_list_clear()

    def obj_ray_cast(obj, matrix):
        '''Wrapper for ray casting that moves the ray into object space'''

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv * ray_origin
        ray_target_obj = matrix_inv * ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj
        '''# cast the ray
        hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)

        if face_index != -1:
            return hit, normal, face_index
        else:
            return None, None, None'''
        # cast the ray
        success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

        if success:
            return location, normal, face_index
        else:
            return None, None, None

    # cast rays and find the closest object
    #best_length_squared = ray_max * ray_max
    best_length_squared = -1.0
    best_obj = None

    for obj, matrix in visible_objects_and_duplis():
        
        if obj.type == 'MESH':
            hit, normal, face_index = obj_ray_cast(obj, matrix)
            if hit is not None:
                hit_world = matrix * hit
                length_squared = (hit_world - ray_origin).length_squared
                if best_obj is None or length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj
                    
                    #object = context.scene.objects.active
                    origin_scale = object.scale.copy()
                    
                    # apply target local coordinate
                    normal = best_obj.matrix_world.to_3x3() * normal
                    normal = normal * -1
                    normal = normal.copy()
                    
                    # rotation
                    
                    vect_x = 1
                    vect_y = 1
                    vect_z = 1
                                    
                    y_vect_x = (normal.y*vect_z)-(normal.z*vect_y)
                    y_vect_y = (normal.z*vect_x)-(normal.x*vect_z)
                    y_vect_z = (normal.x*vect_y)-(normal.y*vect_x)
                    
                    x_vect_x = (normal.y*y_vect_z)-(normal.z*y_vect_y)
                    x_vect_y = (normal.z*y_vect_x)-(normal.x*y_vect_z)
                    x_vect_z = (normal.x*y_vect_y)-(normal.y*y_vect_x)
                    
                    y_vect_normalize = math.sqrt((y_vect_x * y_vect_x) + (y_vect_y * y_vect_y) + (y_vect_z * y_vect_z))
                    x_vect_normalize = math.sqrt((x_vect_x * x_vect_x) + (x_vect_y * x_vect_y) + (x_vect_z * x_vect_z))
                    
                    matrix = mathutils.Matrix().to_3x3()
                    matrix.row[0] = ((x_vect_x/x_vect_normalize, y_vect_x/y_vect_normalize, normal.x))
                    matrix.row[1] = ((x_vect_y/x_vect_normalize, y_vect_y/y_vect_normalize, normal.y))
                    matrix.row[2] = ((x_vect_z/x_vect_normalize, y_vect_z/y_vect_normalize, normal.z))
                    
                    object.matrix_world = matrix.to_4x4()
                    
                    
                    # position
                    object.location = hit_world
                    for i in range(0, 3):
                        object.location[i] = object.location[i] + (offset * normal[i])
                    
                    # scale
                    object.scale = origin_scale


def set_header(context, offset):
    context.area.header_text_set(
        'Aim tool | Move the mouse to align to the normal | Offset with Wheel Up-Down : '+str(offset))


class CustomToolsAimNormal(bpy.types.Operator):
    bl_idname = 'scene.customtools_aim_normal'
    bl_label = 'Aim'
    
    # Properties
    object_name = bpy.props.StringProperty()
    matrix_save = None
    offset = -5
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')
    
    def modal(self, context, event):
        
        w = context.window_manager.windows[0]
        w.cursor_modal_set('CROSSHAIR')
        
        context.area.tag_redraw()
        
        object = context.scene.objects.active
        
        if event.type == 'MOUSEMOVE':
            aim_normal(context, event, self.object_name, offset = self.offset)
            set_header(context, self.offset)
        
        elif event.type == 'WHEELUPMOUSE':
            self.offset += 0.5
            aim_normal(context, event, self.object_name, offset = self.offset)
            set_header(context, self.offset)
        
        elif event.type == 'WHEELDOWNMOUSE':
            self.offset -= 0.5
            aim_normal(context, event, self.object_name, offset = self.offset)
            set_header(context, self.offset)
        
        elif event.type in ('LEFTMOUSE', 'RET', 'NUMPAD_ENTER'):
            
            w.cursor_modal_restore()
            context.area.header_text_set()
            
            return {'FINISHED'}
        
        
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            object.matrix_world = self.matrix_save
            w.cursor_modal_restore()
            context.area.header_text_set()
            
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    
    def invoke(self, context, event):
        
        self.matrix_save = context.scene.objects[self.object_name].matrix_world.copy()
        
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, 'VIEW_3D Editor not found, cannot run operator')
            return {'CANCELLED'}


class CustomToolsLookThrough(bpy.types.Operator):
    bl_idname = 'scene.customtools_look_through'
    bl_label = 'Look through'
    bl_description = 'Look Through selected light, camera or object'
    
    object_name = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def execute(self, context):
        context.space_data.lock_camera_and_layers = False # needs to be False to active local camera
        
        active_scene = context.scene
        active_camera = context.scene.camera
        
        context.space_data.camera = bpy.data.objects[self.object_name]
        bpy.ops.view3d.viewnumpad(type='CAMERA')
        
        return{'FINISHED'}

