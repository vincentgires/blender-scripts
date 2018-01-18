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


import bpy, bgl, blf
import math


## PROPERTIES ##
################

class CustomToolsNodeProperties(bpy.types.PropertyGroup):
    
    bpy.types.Node.custom_tools_viewer = bpy.props.BoolProperty(
        name='Use',
        description='Use this node in viewer list',
        default=0
        )
    
    bpy.types.Scene.color_picker_image = bpy.props.StringProperty(
        name='Image'
        )



## PANEL ##
###########


class NodeEditorCustomPanelTools(bpy.types.Panel):
    bl_label = 'Tools'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator('scene.customtools_copy_attributes')
        
        #box = layout.box()
        row = layout.row(align=True)
        
        left_btn = row.operator(
            'scene.customtools_move_nodes', text=' ', icon='TRIA_LEFT')
        left_btn.direction = 'left'
        right_btn = row.operator(
            'scene.customtools_move_nodes', text=' ', icon='TRIA_RIGHT')
        right_btn.direction = 'right'
        up_btn = row.operator(
            'scene.customtools_move_nodes', text=' ', icon='TRIA_UP')
        up_btn.direction = 'up'
        down_btn = row.operator(
            'scene.customtools_move_nodes', text=' ', icon='TRIA_DOWN')
        down_btn.direction = 'down'
        
        
class NodeEditorCustomPanelViewer(bpy.types.Panel):
    bl_label = 'Viewer'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'CompositorNodeTree')
    
    def draw(self, context):
        layout = self.layout
        
        active_node = context.active_node
        if active_node:
            if not active_node.custom_tools_viewer:
                layout.prop(
                    active_node,
                    'custom_tools_viewer',
                    text=active_node.name,
                    icon='ZOOMIN')
            else:
                layout.prop(
                    active_node,
                    'custom_tools_viewer',
                    text=active_node.name,
                    icon='ZOOMOUT')
        
        if context.scene.use_nodes:
            for node in context.scene.node_tree.nodes:
                if node.custom_tools_viewer:
                    box = layout.box()
                    row = box.row(align=True)
                    if node.label is not '':
                        node_name = node.label
                    else:
                        node_name = node.name
                    
                    button_name = row.operator(
                        'scene.customtools_viewer_connection',
                        emboss=False, text=node_name)
                    button_name.node_name = node.name
                    
                    button_remove = row.operator(
                        'scene.customtools_viewer_remove',
                        icon='PANEL_CLOSE', emboss=False, text='')
                    button_remove.node_name = node.name
                    
                    button_icon = row.operator(
                        'scene.customtools_viewer_connection',
                        icon='TRIA_RIGHT', emboss=False, text='')
                    button_icon.node_name = node.name


class ImageEditorCustomPanelDisplay(bpy.types.Panel):
    bl_label = 'Display'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator('scene.customtools_display_viewer_node')
        col.operator('scene.customtools_display_render_result')


class ImageEditorCustomPanelCompositorNode(bpy.types.Panel):
    bl_label = 'Compositor Node'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        if not scene.node_tree:
            return None
        
        if scene.node_tree.nodes.active:
            active_node = scene.node_tree.nodes.active
            
            layout.label(active_node.name)
            
            col = layout.column(align=True)
            col.operator('scene.customtools_get_mask_from_compositor_node')
            col.operator('scene.customtools_get_image_from_compositor_node')
            col.operator('scene.customtools_create_mask_node')
            
            box = layout.box()
            col = box.column(align=True)
            col.label('Color Picker')
            col.prop_search(context.scene, 'color_picker_image',
                            bpy.data, 'images', icon='IMAGE_DATA')
            for input in active_node.inputs:
                if not input.links:
                    op = col.operator(
                        'scene.customtools_compo_node_color_picker',
                        icon='EYEDROPPER', text=input.name)
                    op.input_name = input.name


class ImageEditorCustomPanelMaterialNode(bpy.types.Panel):
    bl_label = 'Material Node'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        layout = self.layout
        layout.operator('scene.customtools_get_image_from_material_node')


## OPERATOR ##
##############


class CustomToolsShowNode(bpy.types.Operator):
    bl_idname = 'scene.customtools_copy_attributes'
    bl_label = 'Copy attributes'
    bl_description = 'Copy attributes from active node'
    
    def execute(self, context):
        selected_nodes = context.selected_nodes
        active_node = context.active_node
        scene = context.scene
        
        if context.space_data.tree_type == 'CompositorNodeTree':
            tree = scene.node_tree
        elif context.space_data.tree_type == 'ShaderNodeTree':
            if context.space_data.shader_type == 'OBJECT':
                tree = context.object.active_material.node_tree
            elif context.space_data.shader_type == 'WORLD':
                tree = context.scene.world.node_tree
        links = tree.links
        
        type = ['VALUE', 'VECTOR', 'RGBA']
        for index, input in enumerate(active_node.inputs):
            
            for node in selected_nodes:
                
                if input.type in type:
                    if input.type == node.inputs[index].type:
                        node.inputs[index].default_value = input.default_value
                
                if input.is_linked:
                    from_socket = input.links[-1].from_socket
                    links.new(from_socket, node.inputs[index])
        
        return{'FINISHED'}

class CustomToolsMoveNodes(bpy.types.Operator):
    bl_idname = 'scene.customtools_move_nodes'
    bl_label = 'Move nodes left'
    bl_description = 'Move selected nodes to the left'
    
    # custom Properties
    direction = bpy.props.StringProperty(name = 'direction')
    
    def execute(self, context):
        selected_nodes = context.selected_nodes
        
        step = 50
        for node in selected_nodes:
            if self.direction == 'left':
                node.location[0] -= step
            elif self.direction == 'right':
                node.location[0] += step
            elif self.direction == 'up':
                node.location[1] += step
            elif self.direction == 'down':
                node.location[1] -= step
            
        return{'FINISHED'}


class CustomToolsGetMaskFromNode(bpy.types.Operator):
    bl_idname = 'scene.customtools_get_mask_from_compositor_node'
    bl_label = 'Get mask'
    bl_description = 'Get mask from active node'
    
    @classmethod
    def poll(cls, context):
        return (context.scene.node_tree.nodes.active is not None and
                context.scene.node_tree.nodes.active.type == 'MASK')
    
    def execute(self, context):
        target_mask = context.scene.node_tree.nodes.active.mask
        context.space_data.mask = target_mask
        context.space_data.mode = 'MASK'
        
        return{'FINISHED'}


class CustomToolsGetImageFromCompositorNode(bpy.types.Operator):
    bl_idname = 'scene.customtools_get_image_from_compositor_node'
    bl_label = 'Get image'
    bl_description = 'Get image from active node'
    
    @classmethod
    def poll(cls, context):
        return (context.scene.node_tree.nodes.active is not None and
                context.scene.node_tree.nodes.active.type == 'IMAGE')
    
    def execute(self, context):
        target_image = context.scene.node_tree.nodes.active.image
        context.space_data.image = target_image
        
        return{'FINISHED'}


class CustomToolsGetImageFromMaterialNode(bpy.types.Operator):
    bl_idname = 'scene.customtools_get_image_from_material_node'
    bl_label = 'Get image'
    bl_description = 'Get image from active node'
    
    @classmethod
    def poll(cls, context):
        if (context.object is not None and context.object.active_material):
            if context.object.active_material.use_nodes:
                if context.object.active_material.node_tree.nodes.active:
                    if context.object.active_material.node_tree.nodes.active.type == 'TEX_IMAGE':
                        return True
        
    def execute(self, context):
        target_image = context.object.active_material.node_tree.nodes.active.image
        context.space_data.image = target_image
        
        return{'FINISHED'}


class CustomToolsDisplayViewer(bpy.types.Operator):
    bl_idname = 'scene.customtools_display_viewer_node'
    bl_label = 'Display Viewer'
    bl_description = 'Display Viewer Node'
    
    @classmethod
    def poll(cls, context):
        for image in bpy.data.images:
            if image.name == 'Viewer Node':
                return True
    
    def execute(self, context):
        context.space_data.image = bpy.data.images['Viewer Node']
        return{'FINISHED'}


class CustomToolsDisplayRenderResult(bpy.types.Operator):
    bl_idname = 'scene.customtools_display_render_result'
    bl_label = 'Display Render Result'
    bl_description = 'Display Render Result from Composite Node'
    
    @classmethod
    def poll(cls, context):
        for image in bpy.data.images:
            if image.name == 'Render Result':
                return True
    
    def execute(self, context):
        context.space_data.image = bpy.data.images['Render Result']
        
        return{'FINISHED'}


class CustomToolsCreateMaskNode(bpy.types.Operator):
    bl_idname = 'scene.customtools_create_mask_node'
    bl_label = 'Create Mask node'
    bl_description = 'Create Mask node in the compositor'
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.mode == 'MASK')
    
    def execute(self, context):
        
        mask_from_image_editor = context.area.spaces.active.mask
        mask_node = context.scene.node_tree.nodes.new(type='CompositorNodeMask')
        mask_node.mask = mask_from_image_editor
        
        active_node = context.scene.node_tree.nodes.active
        if active_node:
            mask_node.location.x = active_node.location.x + 200
            mask_node.location.y = active_node.location.y - 100
        
        return{'FINISHED'}


class CustomToolsNodeDoubleClick(bpy.types.Operator):
    bl_idname = 'node.double_click'
    bl_label = 'Double Click on a node'
    bl_options = {'UNDO'}
    def execute(self, context):
        active_node = context.active_node
        
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        
                        # IMAGE
                        if active_node.type in ['IMAGE', 'TEX_IMAGE']:
                            space.image = active_node.image
                        
                        # MASK
                        elif active_node.type == 'MASK':
                            space.mask = active_node.mask
                            space.mode = 'MASK'
            
                        # VIEWER
                        elif active_node.type == 'VIEWER':
                            space.image = bpy.data.images['Viewer Node']
                            
                        # COMPOSITE
                        elif active_node.type == 'COMPOSITE':
                            space.image = bpy.data.images['Render Result']
        
        return {'FINISHED'}


class CustomToolsViewerConnection(bpy.types.Operator):
    bl_idname = 'scene.customtools_viewer_connection'
    bl_label = 'Viewer Connection'
    bl_description = 'Connect node to the viewer'
    
    # Properties
    node_name = bpy.props.StringProperty()
    
    def execute(self, context):
        context.scene.node_tree.nodes.active = context.scene.node_tree.nodes[self.node_name]
        bpy.ops.node.link_viewer()

        return{'FINISHED'}

class CustomToolsViewerRemove(bpy.types.Operator):
    bl_idname = 'scene.customtools_viewer_remove'
    bl_label = 'Remove'
    bl_description = 'Remove from list'
    
    # Properties
    node_name = bpy.props.StringProperty()
    
    def execute(self, context):
        context.scene.node_tree.nodes[self.node_name].custom_tools_viewer = False

        return{'FINISHED'}



class CustomToolsCompoNodeColorPicker(bpy.types.Operator):
    bl_idname = 'scene.customtools_compo_node_color_picker'
    bl_label = 'Color Picker'
    bl_description = 'Pick the color of the image and set the value to the selected node'
    
    # Properties
    input_name = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return (context.space_data.image)
    
    def modal(self, context, event):
        
        w = context.window_manager.windows[0]
        w.cursor_modal_set('EYEDROPPER')
        
        context.area.tag_redraw()

        if event.type == 'LEFTMOUSE':
            
            mouse_x = event.mouse_x - context.region.x
            mouse_y = event.mouse_y - context.region.y

            uv = context.area.regions[-1].view2d.region_to_view(mouse_x, mouse_y)
            
            if context.scene.color_picker_image:
                img = bpy.data.images[context.scene.color_picker_image]
            else:
                img = context.area.spaces[0].image
            
            size_x, size_y = img.size[:]
            
            x = int(size_x * uv[0]) % size_x
            y = int(size_y * uv[1]) % size_y
            
            offset = (y * size_x + x) * 4
            pixels = img.pixels[offset:offset+4]
            pixels = [pixels[0], pixels[1], pixels[2]]
            
            selected_input = context.scene.node_tree.nodes.active.inputs
            
            if selected_input[self.input_name].type == 'VECTOR':
                selected_input[self.input_name].default_value = pixels
                
            elif selected_input[self.input_name].type == 'VALUE':
                selected_input[self.input_name].default_value = pixels[0]
            
            elif selected_input[self.input_name].type == 'RGBA':
                selected_input[self.input_name].default_value[0] = pixels[0]
                selected_input[self.input_name].default_value[1] = pixels[1]
                selected_input[self.input_name].default_value[2] = pixels[2]
            
            w.cursor_modal_restore()
            return {'FINISHED'}


        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            w.cursor_modal_restore()
            return {'CANCELLED'}


        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        if context.area.type == 'IMAGE_EDITOR':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, 'UV/Image Editor not found, cannot run operator')
            return {'CANCELLED'}


def distance2d(A, B):
    distance = math.sqrt( (B[0]-A[0])**2 + (B[1]-A[1])**2 )
    return distance


def draw_callback_axis(self, context):
    
    # X AXIS
    bgl.glEnable(bgl.GL_BLEND)
    if self.snap_axis_x:
        bgl.glColor4f(1.0, 0.0, 0.0, 0.7)
        bgl.glLineWidth(1)
    elif self.middlemouse:
        bgl.glColor4f(1.0, 0.0, 0.0, 0.3)
        bgl.glLineWidth(1)
    else:
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glLineWidth(0)
        
    bgl.glBegin(bgl.GL_LINE_STRIP)
    for x in range(context.area.width):
        bgl.glVertex2i(x, self.init_pos_y)
    bgl.glEnd()
    
    # Y AXIS
    bgl.glEnable(bgl.GL_BLEND)
    if self.snap_axis_y:
        bgl.glColor4f(0.0, 1.0, 0.0, 0.7)
        bgl.glLineWidth(1)
    elif self.middlemouse:
        bgl.glColor4f(0.0, 1.0, 0.0, 0.3)
        bgl.glLineWidth(1)
    else:
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glLineWidth(0)
        
    bgl.glBegin(bgl.GL_LINE_STRIP)
    for y in range(context.area.height):
        bgl.glVertex2i(self.init_pos_x, y)
    
    bgl.glEnd()
    
    
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class CustomToolsCompoNodeTransformGrab(bpy.types.Operator):
    bl_idname = 'compo_node_transform_grab.call'
    bl_label = 'Transform node grab modal'
    
    region_x_init = None
    region_y_init = None
    value_x_init = None
    value_y_init = None
    
    @classmethod
    def poll(cls, context):
        return (context.scene.use_nodes and
                    context.scene.node_tree.nodes.active.type in ['TRANSFORM', 'TRANSLATE'])
    
    def modal(self, context, event):
        active_node = context.scene.node_tree.nodes.active
        
        w = context.window_manager.windows[0]
        w.cursor_modal_set('SCROLL_XY')
        context.area.tag_redraw()
        
        self.mouse_pos_xy = (event.mouse_region_x, event.mouse_region_y)
        self.distance_x_axis = distance2d(self.mouse_pos_xy, (self.mouse_pos_xy[0], self.init_pos_y))
        self.distance_y_axis = distance2d(self.mouse_pos_xy, (self.init_pos_x, self.mouse_pos_xy[1]))
        
        
        ### MOVE #############
        ## X ##
        if self.region_x_init:
            if not self.snap_axis_y:
                target_value_x = self.value_x_init + (event.mouse_region_x - self.region_x_init)
                active_node.inputs['X'].default_value = target_value_x
            else:
                active_node.inputs['X'].default_value = self.value_x_init
        else:
            self.region_x_init = event.mouse_region_x
            self.value_x_init = active_node.inputs['X'].default_value
            
        ## Y ##
        if self.region_y_init:
            if not self.snap_axis_x:
                target_value_y = self.value_y_init + (event.mouse_region_y - self.region_y_init)
                active_node.inputs['Y'].default_value = target_value_y
            else:
                active_node.inputs['Y'].default_value = self.value_y_init
        else:
            self.region_y_init = event.mouse_region_y
            self.value_y_init = active_node.inputs['Y'].default_value
        #######################
        
        
        ### SNAP AXIS ###########
        if self.middlemouse:
            # X AXIS
            if self.distance_x_axis < self.distance_y_axis:
                self.snap_axis_x = True
                self.snap_axis_y = False
            # Y AXIS
            elif self.distance_y_axis < self.distance_x_axis:
                self.snap_axis_y = True
                self.snap_axis_x = False
        #########################
        
        
        
        
        ### EVENT ##############
        if event.type in ('RET', 'NUMPAD_ENTER', 'LEFTMOUSE'):
            w.cursor_modal_restore()
            context.area.header_text_set()
            bpy.types.SpaceImageEditor.draw_handler_remove(self._handle_axes, 'WINDOW')
            
            return {'FINISHED'}
        
        
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            active_node.inputs['X'].default_value = self.value_x_init
            active_node.inputs['Y'].default_value = self.value_y_init
            w.cursor_modal_restore()
            context.area.header_text_set()
            bpy.types.SpaceImageEditor.draw_handler_remove(self._handle_axes, 'WINDOW')
            
            return {'CANCELLED'}
        
        elif event.type == 'MIDDLEMOUSE':
            if self.middlemouse:
                self.middlemouse = False
            else:
                self.middlemouse = True
        
        elif event.type == 'X':
            if self.x_key:
                self.x_key = False
            else:
                self.x_key = True
                if self.snap_axis_x :
                    self.snap_axis_x = False
                    self.snap_axis_y = False
                else:
                    self.snap_axis_x = True
                    self.snap_axis_y = False
                    
                
        elif event.type == 'Y':
            if self.y_key:
                self.y_key = False
            else:
                self.y_key = True
                if self.snap_axis_y:
                    self.snap_axis_x = False
                    self.snap_axis_y = False
                else:
                    self.snap_axis_x = False
                    self.snap_axis_y = True
        #######################
        
        
        
        #print ('X',self.snap_axis_x)
        #print ('Y',self.snap_axis_y)
        
        return {'RUNNING_MODAL'}
    
    
    def invoke(self, context, event):
        active_node = context.scene.node_tree.nodes.active
        image_space = context.area.spaces.active
        img_size_x, img_size_y = image_space.image.size
        
        self.middlemouse = False
        self.x_key = False
        self.y_key = False
        
        #self.init_pos_x = 100
        #self.init_pos_y = 100
        #self.init_pos_x = int(context.area.width/2)
        #self.init_pos_y = int(context.area.height/2)
        self.init_pos_x, self.init_pos_y = bpy.context.region.view2d.view_to_region(active_node.inputs['X'].default_value/img_size_x + 0.5, active_node.inputs['Y'].default_value/img_size_y + 0.5)
        
        self.snap_axis_x = False
        self.snap_axis_y = False
        
        args = (self, context)
        self._handle_axes = bpy.types.SpaceImageEditor.draw_handler_add(draw_callback_axis, args, 'WINDOW', 'POST_PIXEL')
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

