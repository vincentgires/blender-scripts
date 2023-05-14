import bpy
import bgl
import math
from .colorspace import SetInputTransform


class GetMaskFromNode(bpy.types.Operator):
    bl_idname = 'scene.get_mask_from_compositor_node'
    bl_label = 'Get Mask'
    bl_description = 'Get mask from active node'

    @classmethod
    def poll(cls, context):
        active_node = context.scene.node_tree.nodes.active
        return active_node and active_node.type == 'MASK'

    def execute(self, context):
        target_mask = context.scene.node_tree.nodes.active.mask
        context.space_data.mask = target_mask
        context.space_data.mode = 'MASK'
        return {'FINISHED'}


class GetImageFromCompositorNode(bpy.types.Operator):
    bl_idname = 'scene.get_image_from_compositor_node'
    bl_label = 'Get Image'
    bl_description = 'Get image from active node'

    @classmethod
    def poll(cls, context):
        active_node = context.scene.node_tree.nodes.active
        return active_node and active_node.type == 'IMAGE'

    def execute(self, context):
        target_image = context.scene.node_tree.nodes.active.image
        context.space_data.image = target_image
        return {'FINISHED'}


class GetImageFromMaterialNode(bpy.types.Operator):
    bl_idname = 'scene.get_image_from_material_node'
    bl_label = 'Get Image'
    bl_description = 'Get image from active node'

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False

        active_material = context.object.active_material
        if context.object and active_material:
            if active_material.use_nodes:
                active_node = active_material.node_tree.nodes.active
                if active_node:
                    return active_node.type == 'TEX_IMAGE'

    def execute(self, context):
        active_material = context.object.active_material
        target_image = active_material.node_tree.nodes.active.image
        context.space_data.image = target_image
        return {'FINISHED'}


class CreateMaskNode(bpy.types.Operator):
    bl_idname = 'scene.create_mask_node'
    bl_label = 'Create Mask Node'
    bl_description = 'Create mask mode in the compositor'

    @classmethod
    def poll(cls, context):
        return (context.space_data.mode == 'MASK')

    def execute(self, context):
        mask_from_image_editor = context.area.spaces.active.mask
        node_tree = context.scene.node_tree
        mask_node = node_tree.nodes.new(type='CompositorNodeMask')
        mask_node.mask = mask_from_image_editor
        active_node = context.scene.node_tree.nodes.active
        if active_node:
            mask_node.location.x = active_node.location.x + 200
            mask_node.location.y = active_node.location.y - 100
        return {'FINISHED'}


class DoubleClick(bpy.types.Operator):
    bl_idname = 'node.double_click'
    bl_label = 'Node Double Click'
    bl_options = {'UNDO'}

    def execute(self, context):
        active_node = context.active_node
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        # Image
                        if active_node.type in ['IMAGE', 'TEX_IMAGE']:
                            space.image = active_node.image
                        # Mask
                        elif active_node.type == 'MASK':
                            space.mask = active_node.mask
                            space.mode = 'MASK'
                        # Viewer
                        elif active_node.type == 'VIEWER':
                            space.image = bpy.data.images['Viewer Node']
                        # Composite
                        elif active_node.type == 'COMPOSITE':
                            space.image = bpy.data.images['Render Result']
        return {'FINISHED'}


class CompostorNodeColorPicker(bpy.types.Operator):
    bl_idname = 'scene.compositor_node_color_picker'
    bl_label = 'Color Picker'
    bl_description = 'Pick the color and set the value to the selected node'

    input_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return (context.space_data.image)

    def modal(self, context, event):
        scene = context.scene
        area = context.area
        w = context.window_manager.windows[0]
        w.cursor_modal_set('EYEDROPPER')

        context.area.tag_redraw()

        if event.type == 'LEFTMOUSE':

            mouse_x = event.mouse_x - context.region.x
            mouse_y = event.mouse_y - context.region.y

            uv = area.regions[-1].view2d.region_to_view(mouse_x, mouse_y)

            if scene.color_picker_image:
                img = bpy.data.images[scene.color_picker_image]
            else:
                img = area.spaces[0].image

            size_x, size_y = img.size[:]

            x = int(size_x * uv[0]) % size_x
            y = int(size_y * uv[1]) % size_y

            offset = (y * size_x + x) * 4
            pixels = img.pixels[offset:offset + 4]
            pixels = [pixels[0], pixels[1], pixels[2]]

            selected_input = scene.node_tree.nodes.active.inputs

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
            self.report({'WARNING'},
                        'UV/Image Editor not found, cannot run operator')
            return {'CANCELLED'}


def _distance2d(A, B):
    distance = math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
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


class CompositorNodeTransformGrab(bpy.types.Operator):
    bl_idname = 'scene.compositor_node_transform_grab'
    bl_label = 'Transform Node Grab'

    region_x_init = None
    region_y_init = None
    value_x_init = None
    value_y_init = None

    @classmethod
    def poll(cls, context):
        scene = context.scene
        active_node = scene.node_tree.nodes.active
        return (scene.use_nodes and
                active_node.type in ['TRANSFORM', 'TRANSLATE'])

    def modal(self, context, event):
        active_node = context.scene.node_tree.nodes.active

        w = context.window_manager.windows[0]
        w.cursor_modal_set('SCROLL_XY')
        context.area.tag_redraw()

        self.mouse_pos_xy = (event.mouse_region_x, event.mouse_region_y)
        self.distance_x_axis = _distance2d(
            self.mouse_pos_xy, (self.mouse_pos_xy[0], self.init_pos_y))
        self.distance_y_axis = _distance2d(
            self.mouse_pos_xy, (self.init_pos_x, self.mouse_pos_xy[1]))

        # Move X
        if self.region_x_init:
            if not self.snap_axis_y:
                target_value_x = self.value_x_init \
                    + (event.mouse_region_x - self.region_x_init)
                active_node.inputs['X'].default_value = target_value_x
            else:
                active_node.inputs['X'].default_value = self.value_x_init
        else:
            self.region_x_init = event.mouse_region_x
            self.value_x_init = active_node.inputs['X'].default_value

        # Move Y
        if self.region_y_init:
            if not self.snap_axis_x:
                target_value_y = self.value_y_init \
                    + (event.mouse_region_y - self.region_y_init)
                active_node.inputs['Y'].default_value = target_value_y
            else:
                active_node.inputs['Y'].default_value = self.value_y_init
        else:
            self.region_y_init = event.mouse_region_y
            self.value_y_init = active_node.inputs['Y'].default_value

        # Snap axis
        if self.middlemouse:
            # X
            if self.distance_x_axis < self.distance_y_axis:
                self.snap_axis_x = True
                self.snap_axis_y = False
            # Y
            elif self.distance_y_axis < self.distance_x_axis:
                self.snap_axis_y = True
                self.snap_axis_x = False

        # Event
        if event.type in ('RET', 'NUMPAD_ENTER', 'LEFTMOUSE'):
            w.cursor_modal_restore()
            context.area.header_text_set()
            bpy.types.SpaceImageEditor.draw_handler_remove(
                self._handle_axes, 'WINDOW')

            return {'FINISHED'}

        elif event.type in ('RIGHTMOUSE', 'ESC'):
            active_node.inputs['X'].default_value = self.value_x_init
            active_node.inputs['Y'].default_value = self.value_y_init
            w.cursor_modal_restore()
            context.area.header_text_set()
            bpy.types.SpaceImageEditor.draw_handler_remove(
                self._handle_axes, 'WINDOW')

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
                if self.snap_axis_x:
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

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        active_node = context.scene.node_tree.nodes.active
        image_space = context.area.spaces.active
        img_size_x, img_size_y = image_space.image.size

        self.middlemouse = False
        self.x_key = False
        self.y_key = False

        view2d = context.region.view2d
        self.init_pos_x, self.init_pos_y = view2d.view_to_region(
            active_node.inputs['X'].default_value / img_size_x + 0.5,
            active_node.inputs['Y'].default_value / img_size_y + 0.5)

        self.snap_axis_x = False
        self.snap_axis_y = False

        args = (self, context)
        self._handle_axes = bpy.types.SpaceImageEditor.draw_handler_add(
            draw_callback_axis, args, 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SetImageNodeInputTransform(SetInputTransform):
    bl_idname = 'scene.set_image_node_input_transform'
    bl_label = 'Set Image Node Input Transform'

    @classmethod
    def poll(cls, context):
        return context.active_node

    def get_datablocks(self, context):
        return [context.active_node.image]
