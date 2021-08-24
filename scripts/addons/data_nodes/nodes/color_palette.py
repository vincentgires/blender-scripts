import bpy
from bpy.types import Node
from ..utils import send_value


class TemplateColorPaletteCollectionUL(bpy.types.UIList):
    bl_idname = 'DATANODES_UL_template_color_palette_collection'

    def draw_item(self, context, layout, data, item,
                  icon, active_data, active_propname, index):
        layout.prop(item, 'name', text='', emboss=False)
        row = layout.row(align=True)
        for color_item in item.color_collection:
            row.prop(color_item, 'color', text='')


class ColorPalette(Node):
    """Color Palette node"""
    bl_idname = 'ColorPaletteNodeType'
    bl_label = 'Color Palette'

    def update_props(self, context):
        self.update()

    settings: bpy.props.BoolProperty(
        name='Settings',
        default=True)

    palette_id: bpy.props.IntProperty(
        name='Palette ID',
        default=0,
        update=update_props)

    def init(self, context):
        self.outputs.new('NodeSocketColor', 'Color')
        self.outputs.new('NodeSocketColor', 'Color')
        self.outputs.new('NodeSocketColor', 'Color')
        for palette in bpy.context.scene.colorpalette_collection:
            for color in palette.color_collection:
                if len(self.outputs) <= len(palette.color_collection):
                    self.outputs.new('NodeSocketColor', 'Color')

    def update(self):
        scene = bpy.context.scene
        if scene.colorpalette_collection:
            palette = scene.colorpalette_collection[self.palette_id]
            palette_color = palette.color_collection

            # Send data value to connected nodes
            for index, output in enumerate(self.outputs):
                for link in output.links:
                    if link.is_valid:
                        if link.to_node.type == 'REROUTE':
                            reroute = link.to_node
                            send_value(self.outputs, palette_color[index].color)
                        if output.type == link.to_socket.type:
                            # Assign value to connected socket
                            link.to_socket.default_value = palette_color[index].color
                            # Update connected target nodes
                            link.to_node.update()

    def draw_buttons(self, context, layout):
        if self.settings:
            row = layout.row()
            row.prop(self, 'settings', text='', icon='TRIA_DOWN', emboss=False)
            row = layout.row()
            row.template_list(
                'TemplateColorPaletteCollectionUL', '',
                context.scene, 'colorpalette_collection', self, 'palette_id')
            col = row.column(align=True)
            col.operator(
                'color_palette_add_item.btn',
                icon='ADD',
                text='')
            col.operator(
                'color_palette_remove_item.btn',
                icon='REMOVE',
                text='')
        else:
            row = layout.row()
            row.prop(self, 'settings', text='', icon='TRIA_RIGHT', emboss=False)

        if context.scene.colorpalette_collection:
            palette = context.scene.colorpalette_collection[self.palette_id]
            row = layout.row(align=True)
            row.operator('color_palette_add_color.btn', text='', icon='ADD')
            for color_item in palette.color_collection:
                row.prop(color_item, 'color', text='')
            row.operator(
                'color_palette_remove_color.btn',
                text='',
                icon='REMOVE')
            row.operator(
                'color_palette_clear_color.btn',
                text='', icon='X')

    def draw_label(self):
        return 'Color Palette'


class CustomNodesAddPaletteItem(bpy.types.Operator):
    bl_idname = 'color_palette_add_item.btn'
    bl_label = 'Palette add item'

    @classmethod
    def poll(cls, context):
        try:
            tree_type = context.space_data.tree_type
            node_tree = [
                'ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
            return tree_type in node_tree
        except:
            return False

    def execute(self, context):
        node = context.node
        palette_collection = context.scene.colorpalette_collection
        p = palette_collection.add()
        p.name = str(len(palette_collection))
        p.color_collection.add()
        p.color_collection.add()
        p.color_collection.add()
        node.palette_id = len(palette_collection) - 1
        return {'FINISHED'}


class CustomNodesRemovePaletteItem(bpy.types.Operator):
    bl_idname = 'color_palette_remove_item.btn'
    bl_label = 'Palette remove item'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        palette_collection = context.scene.colorpalette_collection
        palette_collection.remove(node.palette_id)
        if node.palette_id > 0:
            node.palette_id -= 1
        return {'FINISHED'}


class CustomNodesAddPaletteColor(bpy.types.Operator):
    bl_idname = 'color_palette_add_color.btn'
    bl_label = 'Palette add color'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        palette = context.scene.colorpalette_collection[node.palette_id]
        palette.color_collection.add()
        # Sockets
        if (len(node.outputs) <= len(palette.color_collection) - 1):
            node.outputs.new('NodeSocketColor', 'Color')
        return {'FINISHED'}


class CustomNodesRemovePaletteColor(bpy.types.Operator):
    bl_idname = 'color_palette_remove_color.btn'
    bl_label = 'Palette remove color'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        palette = context.scene.colorpalette_collection[node.palette_id]
        palette.color_collection.remove(len(palette.color_collection) - 1)
        return {'FINISHED'}


class CustomNodesClearPaletteColor(bpy.types.Operator):
    bl_idname = 'color_palette_clear_color.btn'
    bl_label = 'Palette clear color'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        palette = context.scene.colorpalette_collection[node.palette_id]
        palette.color_collection.clear()
        return {'FINISHED'}
