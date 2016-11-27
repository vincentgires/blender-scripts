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




bl_info = {
    "name": "Display Layers",
    "author": "Vincent Gires",
    "description": "---",
    "version": (0, 1, 2),
    "blender": (2, 7, 6),
    "location": "Tools > Layers",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Layers"}

import bpy




###############
## FUNCTIONS ##
###############

def apply_layer_settings(context):
    
    for obj in context.scene.objects:
        if obj.use_display_layer:
            
            layer = context.scene.display_layers_collection[obj.display_layer]
            
            if layer.display:
                obj.hide = False
            else:
                obj.hide = True
            
            if layer.select:
                obj.hide_select = False
            else:
                obj.hide_select = True
            
            if layer.render:
                obj.hide_render = False
            else:
                obj.hide_render = True
            
            if layer.wire:
                obj.show_wire = True
                obj.show_all_edges = True
            else:
                obj.show_wire = False
                obj.show_all_edges = False
            
            
def move_layer(context, layers_collection, index, direction):
    
    layers_collection.move(index, index+direction)
    context.scene.display_layers_collection_index = index+direction

    for obj in context.scene.objects:
        
        if obj.display_layer == index:
            obj.display_layer = index+direction
            
        elif obj.display_layer == index+direction:
            obj.display_layer = index
    




######### CALL BACK #########
#############################

def display_toggle_callback(self, context):
    apply_layer_settings(context)



#######################
## CUSTOM PROPERTIES ##
#######################


# Assign a collection
class property_collection_display_layers(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Layer name", default="Layer"),
    display = bpy.props.BoolProperty(name="Display", default=True, update=display_toggle_callback)
    select = bpy.props.BoolProperty(name="Select", default=True, update=display_toggle_callback)
    render = bpy.props.BoolProperty(name="Render", default=True, update=display_toggle_callback)
    wire = bpy.props.BoolProperty(name="Wire", default=False, update=display_toggle_callback)
    
    
class display_layers_properties(bpy.types.PropertyGroup):
    
    bpy.types.Object.display_layer = bpy.props.IntProperty(
        name = "Layer ID",
        default = 0,
        min = 0,
        update = display_toggle_callback
    )
    
    bpy.types.Object.use_display_layer = bpy.props.BoolProperty(
        name = "Use Layer",
        default = 0,
        update = display_toggle_callback
    )
    
    bpy.types.Scene.display_layers_collection_index = bpy.props.IntProperty(
        name = "Layer Scene Index",
        default = 0,
        min = 0,
    )
    
    


#############
## UI LIST ##
#############


class layers_collection_UL(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        layer = item
        
        layout.prop(layer, "name", text="", icon_value=icon, emboss=False)
        
        icon_render = 'RESTRICT_VIEW_OFF' if layer.display else 'RESTRICT_VIEW_ON'
        layout.prop(item, "display", text="", icon=icon_render, emboss=False)
        
        icon_render = 'RESTRICT_RENDER_OFF' if layer.render else 'RESTRICT_RENDER_ON'
        layout.prop(item, "render", text="", icon=icon_render, emboss=False)
        
        icon_render = 'MESH_UVSPHERE' if layer.wire else 'WIRE'
        layout.prop(item, "wire", text="", icon=icon_render, emboss=False)
        
        icon_select = 'UNLOCKED' if layer.select else 'LOCKED'
        layout.prop(item, "select", text="", icon=icon_select, emboss=False)


###########
## PANEL ##
###########


class VIEW3D_layers_panel(bpy.types.Panel):
    bl_label = "Display Layers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Layers"
    bl_context = "objectmode"
    
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        col = row.column()
        col.template_list("layers_collection_UL", "", context.scene, "display_layers_collection", context.scene, "display_layers_collection_index")
        
        col = row.column()
        sub = col.column(align=True)
        sub.operator("add_layer_from_collection.btn", icon='ZOOMIN', text="")
        sub.operator("remove_layer_from_collection.btn", icon='ZOOMOUT', text="")
        sub.operator("up_layer_from_collection.btn", icon='TRIA_UP', text="")
        sub.operator("down_layer_from_collection.btn", icon='TRIA_DOWN', text="")
        
        sub = col.column(align=True)
        sub.operator("assign_layer.btn", icon="DISCLOSURE_TRI_RIGHT", text="")
        sub.operator("remove_layer.btn", icon="DISCLOSURE_TRI_DOWN", text="")
        sub.operator("select_objects.btn", icon="RESTRICT_SELECT_OFF", text="")
        
        col.operator("clear_display_layers_collection.btn", icon="X", text="")
        
        
        layout.prop(context.scene, "display_layers_collection")
        
        """row =layout.row(align=True)
        row.operator("assign_layer.btn", icon="OBJECT_DATA")
        row.operator("remove_layer.btn", icon="X")"""
        
        
        
        
class layers_object_panel(bpy.types.Panel):
    bl_label = "Display Layers"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    @classmethod
    def poll(cls, context):
        return context.object
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.object, "use_display_layer")
        row.prop(context.object, "display_layer")
        
        layer_id = context.object.display_layer
        if layer_id < len(context.scene.display_layers_collection.items()):
            box = layout.box()
            box.label("Name : "+context.scene.display_layers_collection[layer_id].name)



##############
## OPERATOR ##
##############



class layers_add(bpy.types.Operator):
    bl_idname = "add_layer_from_collection.btn"
    bl_label = "Add"
    bl_description = "Add layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        my_item = context.scene.display_layers_collection.add()
        my_item.name = "Layer"+str(len(context.scene.display_layers_collection))
        
        context.scene.display_layers_collection_index = len(context.scene.display_layers_collection)-1
        
        return{'FINISHED'}

class layers_remove(bpy.types.Operator):
    bl_idname = "remove_layer_from_collection.btn"
    bl_label = "Remove"
    bl_description = "Remove layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        index = context.scene.display_layers_collection_index
        context.scene.display_layers_collection.remove(index)
        
        # change all index of object higher than removed index
        for obj in context.scene.objects:
            if obj.display_layer > index:
                obj.display_layer = obj.display_layer - 1
            
            elif obj.display_layer == index:
                obj.use_display_layer = False
            
            
        return{'FINISHED'}



class layers_up(bpy.types.Operator):
    bl_idname = "up_layer_from_collection.btn"
    bl_label = "Up"
    bl_description = "Up layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.scene.display_layers_collection_index > 0 and context.scene.display_layers_collection.items()
        
    def execute(self, context):
        
        layers_collection = context.scene.display_layers_collection
        index = context.scene.display_layers_collection_index
        direction = -1
        move_layer(context, layers_collection, index, direction)
            
            
        return{'FINISHED'}


class layers_down(bpy.types.Operator):
    bl_idname = "down_layer_from_collection.btn"
    bl_label = "Down"
    bl_description = "Down layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(bpy.context.scene.display_layers_collection) > context.scene.display_layers_collection_index+1
    
    def execute(self, context):
        
        layers_collection = context.scene.display_layers_collection
        index = context.scene.display_layers_collection_index
        direction = 1
        move_layer(context, layers_collection, index, direction)
            
        return{'FINISHED'}



class layers_assignSelectedObjects(bpy.types.Operator):
    bl_idname = "assign_layer.btn"
    bl_label = "Assign"
    bl_description = "Assign layer to selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.scene.display_layers_collection.items()
    
    def execute(self, context):
        selected_objects = context.selected_objects
        active_object = context.active_object
        active_layer_index = context.scene.display_layers_collection_index
        
        for obj in selected_objects:
            obj.display_layer = active_layer_index
            obj.use_display_layer = True
        
        apply_layer_settings(context)
        
        return{'FINISHED'}

class layers_removeSelectedObjects(bpy.types.Operator):
    bl_idname = "remove_layer.btn"
    bl_label = "Remove"
    bl_description = "Remove selected objects from layer"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.scene.display_layers_collection.items()
    
    def execute(self, context):
        selected_objects = context.selected_objects
        active_object = context.active_object
        active_layer_index = context.scene.display_layers_collection_index
        
        for obj in selected_objects:
            obj.use_display_layer = False
        
        apply_layer_settings(context)
        
        return{'FINISHED'}


      
class layers_select_objects(bpy.types.Operator):
    bl_idname = "select_objects.btn"
    bl_label = "Select"
    bl_description = "Select objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.scene.display_layers_collection.items()
    
    def execute(self, context):
        active_layer_index = context.scene.display_layers_collection_index
        
        for obj in context.scene.objects:
            if obj.use_display_layer and obj.display_layer == active_layer_index:
                obj.select = True
                obj.select = True
                
        return{'FINISHED'}


class layers_select_objects(bpy.types.Operator):
    bl_idname = "clear_display_layers_collection.btn"
    bl_label = "Clear"
    bl_description = "Clear layers"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.scene.display_layers_collection.items()
    
    def execute(self, context):
        context.scene.display_layers_collection.clear()
        return{'FINISHED'}

#########################
#########################



def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.display_layers_collection = \
        bpy.props.CollectionProperty(type=property_collection_display_layers)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.display_layers_collection

if __name__ == "__main__":
    register()


