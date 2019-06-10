import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value_link


data_items = (
    ('actions', 'actions', ''),
    ('armatures', 'armatures', ''),
    ('brushes', 'brushes', ''),
    ('cameras', 'cameras', ''),
    ('curves', 'curves', ''),
    ('fonts', 'fonts', ''),
    ('groups', 'groups', ''),
    ('images', 'images', ''),
    ('lamps', 'lamps', ''),
    ('lattices', 'lattices', ''),
    ('linestyles', 'linestyles', ''),
    ('masks', 'masks', ''),
    ('materials', 'materials', ''),
    ('meshes', 'meshes', ''),
    ('metaballs', 'metaballs', ''),
    ('movieclips', 'movieclips', ''),
    ('node_groups', 'node_groups', ''),
    ('objects', 'objects', ''),
    ('particles', 'particles', ''),
    ('scenes', 'scenes', ''),
    ('shape_keys', 'shape_keys', ''),
    ('sounds', 'sounds', ''),
    ('speakers', 'speakers', ''),
    ('texts', 'texts', ''),
    ('textures', 'textures', ''),
    ('worlds', 'worlds', '')
    )


class DataInputNode(Node):
    '''Data Input'''
    bl_idname = 'DataInputNodeType'
    bl_label = 'Data Input'

    def update_attribute(self, context):
        self.update()

    settings = bpy.props.BoolProperty(
        name='Settings', default=True)
    data_enum = bpy.props.EnumProperty(
        name='Data',items=data_items, default='objects')
    data_item = bpy.props.StringProperty(
        name='Item')
    attribute_property = bpy.props.StringProperty(
        name='Attribute',update=update_attribute)

    def update(self):
        # find data value
        if self.data_item:
            data_path = "bpy.data."+self.data_enum + "['"+self.data_item+"']"
            data_path = eval(data_path)

            # send data value to connected nodes
            for output in self.outputs:
                for link in output.links:

                    # set value
                    try:
                        value = eval('data_path'+'.'+output.name)
                    except:
                        value = None

                    if value:
                        send_value_link(link, value)


    def draw_buttons(self, context, layout):

        if self.settings:
            row = layout.row()
            row.prop(self, 'settings', text='',
                     icon='TRIA_DOWN', emboss=False)

            layout.prop(self, 'data_enum')

            row = layout.row(align=True)
            row.prop_search(self, 'data_item', bpy.data, self.data_enum, text='')
            row.operator('get_object_to_data_node.btn', text = '', icon='EYEDROPPER')

            row = layout.row(align=True)
            row.prop(self, 'attribute_property', text='')
            row.operator('add_output_socket_to_data_node.btn', text='', icon='ADD')

            layout.operator('remove_output_sockets.btn', text='Clear', icon='X')

        else:
            row = layout.row()
            row.prop(self, 'settings', text='', icon='TRIA_RIGHT', emboss=False)
            row.label(self.data_item)

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'data_enum')

        row = layout.row(align=True)
        row.prop_search(self, 'data_item', bpy.data, self.data_enum, text='')
        row.operator('get_object_to_data_node.btn', text='', icon='EYEDROPPER')

        row = layout.row(align=True)
        row.prop(self, 'attribute_property', text='')
        row.operator('add_output_socket_to_data_node.btn', text='', icon='ADD')

        layout.operator('remove_output_sockets.btn', text='Clear', icon='X')

    def draw_label(self):
        return 'Data Input'



