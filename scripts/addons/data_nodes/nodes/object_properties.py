import bpy
import math
from bpy.types import NodeTree, Node, NodeSocket
from ..utils import send_value_link


class ObjectPropertiesNode(Node):
    """Object Properties node"""
    bl_idname = 'ObjectPropertiesNodeType'
    bl_label = 'Object Properties'

    def update_object_name(self, context):
        # Update properties from the new selected object
        if self.data_item is not '':
            self.update_props_from_object()

    def update_object_location(self, context):
        if self.data_item is not '':
            item = context.scene.objects[self.data_item]
            item.location = self.locationProperty
            self.update()

    def update_object_rotation(self, context):
        if self.data_item is not '':
            item = context.scene.objects[self.data_item]
            item.rotation_euler[0] = math.radians(self.rotationProperty[0])
            item.rotation_euler[1] = math.radians(self.rotationProperty[1])
            item.rotation_euler[2] = math.radians(self.rotationProperty[2])
            self.update()

    def update_object_scale(self, context):
        if self.data_item is not '':
            item = context.scene.objects[self.data_item]
            item.scale = self.scaleProperty
            self.update()

    def update_invert_matrix(self, context):
        if self.data_item is not '':
            self.update()

    def update_matrix(self):
        if self.data_item is not '':
            object = bpy.context.scene.objects[self.data_item]
            matrix = object.matrix_world.to_3x3()
            if self.invertMatrixProperty:
                matrix = matrix.inverted()
            self.matrixRow1Property = matrix[0]
            self.matrixRow2Property = matrix[1]
            self.matrixRow3Property = matrix[2]

    def update_target_nodes(self):
        for output in self.outputs:
            for link in output.links:
                if link.is_valid:
                    # Update connected target nodes
                    link.to_node.update()

    # Custom Properties
    data_item: bpy.props.StringProperty(
        name='Object', update=update_object_name)
    locationProperty: bpy.props.FloatVectorProperty(
        name='Location',
        default=(0.0, 0.0, 0.0),
        update=update_object_location)
    rotationProperty: bpy.props.FloatVectorProperty(
        name='Rotation',
        default=(0.0, 0.0, 0.0),
        update=update_object_rotation)
    scaleProperty: bpy.props.FloatVectorProperty(
        name='Scale',
        default=(1.0, 1.0, 1.0),
        update=update_object_scale)
    invertMatrixProperty: bpy.props.BoolProperty(
        name='Invert Matrix',
        default=False,
        update=update_invert_matrix)
    matrixRow1Property: bpy.props.FloatVectorProperty(
        name='Matrix Row1', default=(1.0, 0.0, 0.0))
    matrixRow2Property: bpy.props.FloatVectorProperty(
        name='Matrix Row2', default=(0.0, 1.0, 0.0))
    matrixRow3Property: bpy.props.FloatVectorProperty(
        name='Matrix Row3', default=(0.0, 0.0, 1.0))
    displayProperty: bpy.props.BoolProperty(
        name='display properties', default=False)

    def init(self, context):
        self.outputs.new('NodeSocketVector', 'Location')
        self.outputs.new('NodeSocketVector', 'Rotation')
        self.outputs.new('NodeSocketVector', 'Scale')
        self.outputs.new('NodeSocketVector', 'Matrix Row1')
        self.outputs.new('NodeSocketVector', 'Matrix Row2')
        self.outputs.new('NodeSocketVector', 'Matrix Row3')

    def update(self):
        self.update_matrix()
        for output in self.outputs:
            for link in output.links:
                if output.name == 'Location':
                    output.default_value = self.locationProperty
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.locationProperty)
                elif output.name == 'Rotation':
                    output.default_value = self.rotationProperty
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.rotationProperty)
                elif output.name == 'Scale':
                    output.default_value = self.scaleProperty
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.scaleProperty)
                elif output.name == 'Matrix Row1':
                    output.default_value = self.matrixRow1Property
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.matrixRow1Property)
                elif output.name == 'Matrix Row2':
                    output.default_value = self.matrixRow2Property
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.matrixRow2Property)
                elif output.name == 'Matrix Row3':
                    output.default_value = self.matrixRow3Property
                    if link.to_socket.type == 'VECTOR':
                        send_value_link(link, self.matrixRow3Property)
        self.update_target_nodes()

    def update_props_from_object(self):
        scene = bpy.context.scene
        self.locationProperty = scene.objects[self.data_item].location
        self.rotationProperty = scene.objects[self.data_item].rotation_euler
        self.rotationProperty[0] = math.degrees(self.rotationProperty[0])
        self.rotationProperty[1] = math.degrees(self.rotationProperty[1])
        self.rotationProperty[2] = math.degrees(self.rotationProperty[2])
        self.scaleProperty = scene.objects[self.data_item].scale

    def draw_buttons(self, context, layout):
        row = layout.row(align=True)
        row.prop_search(
            self, 'data_item', bpy.data, 'objects',
            icon='OBJECT_DATA', text='')
        row.operator('get_object_to_data_node.btn', text='', icon='EYEDROPPER')
        layout.prop(self, 'displayProperty', text='Properties')
        if self.displayProperty:
            layout.prop(self, 'locationProperty')
            layout.prop(self, 'rotationProperty')
            layout.prop(self, 'scaleProperty')
        layout.prop(self, 'invertMatrixProperty')

    def draw_buttons_ext(self, context, layout):
        row = layout.row(align=True)
        row.prop_search(
            self, 'data_item', bpy.data, 'objects',
            icon='OBJECT_DATA')
        row.operator('get_object_to_data_node.btn', text='', icon='EYEDROPPER')
        layout.prop(self, 'locationProperty')
        layout.prop(self, 'rotationProperty')
        layout.prop(self, 'scaleProperty')
        box = layout.box()
        box.prop(self, 'invertMatrixProperty')
        row = box.row()
        row.label(text=str(self.matrixRow1Property[0]))
        row.label(text=str(self.matrixRow1Property[1]))
        row.label(text=str(self.matrixRow1Property[2]))
        row = box.row()
        row.label(text=str(self.matrixRow2Property[0]))
        row.label(text=str(self.matrixRow2Property[1]))
        row.label(text=str(self.matrixRow2Property[2]))
        row = box.row()
        row.label(text=str(self.matrixRow3Property[0]))
        row.label(text=str(self.matrixRow3Property[1]))
        row.label(text=str(self.matrixRow3Property[2]))

    def draw_label(self):
        return 'Object Properties'
