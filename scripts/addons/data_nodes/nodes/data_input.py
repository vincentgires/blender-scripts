import bpy
from bpy.types import Node
from . import DATA_ITEMS
from ..utils import send_value_link
from operator import attrgetter


class DataInputNode(Node):
    """Data Input"""
    bl_idname = 'DataInputNodeType'
    bl_label = 'Data Input'

    def update_attribute(self, context):
        self.update()

    settings: bpy.props.BoolProperty(
        name='Settings', default=True)
    data: bpy.props.EnumProperty(
        name='Data', items=DATA_ITEMS, default='objects')
    item: bpy.props.StringProperty(
        name='Item')
    attribute: bpy.props.StringProperty(
        name='Attribute', update=update_attribute)

    def update(self):
        if not self.item:
            return
        data_collection = getattr(bpy.data, self.data)
        item = data_collection.get(self.item)
        if item is None:
            return
        for output in self.outputs:
            for link in output.links:
                value = attrgetter(output.name)(item)
                send_value_link(link, value)

    def draw_buttons(self, context, layout):

        if self.settings:
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(self, 'settings', text='', icon='TRIA_DOWN', emboss=False)
            row.prop(self, 'data', text='')
            row = col.row(align=True)
            row.prop_search(self, 'item', bpy.data, self.data, text='')
            row.operator(
                'scene.get_object_to_data_node', text='', icon='EYEDROPPER')
            row = col.row(align=True)
            row.prop(self, 'attribute', text='')
            add_socket = row.operator(
                'scene.add_socket_to_data_node', text='', icon='ADD')
            add_socket.socket_type = 'OUTPUT'
            remove_sockets = col.operator(
                'scene.remove_sockets', text='Clear', icon='X')
            remove_sockets.socket_type = 'OUTPUT'
        else:
            row = layout.row(align=True)
            row.prop(
                self, 'settings', text='', icon='TRIA_RIGHT', emboss=False)
            row.label(text=self.item)

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'data')
        row = layout.row(align=True)
        row.prop_search(self, 'item', bpy.data, self.data, text='')
        row.operator(
            'scene.get_object_to_data_node', text='', icon='EYEDROPPER')
        row = layout.row(align=True)
        row.prop(self, 'attribute', text='')
        add_socket = row.operator(
            'scene.add_socket_to_data_node', text='', icon='ADD')
        add_socket.socket_type = 'OUTPUT'
        remove_sockets = layout.operator(
            'scene.remove_sockets', text='Clear', icon='X')
        remove_sockets.socket_type = 'OUTPUT'

    def draw_label(self):
        return 'Data Input'
