import bpy
from bpy.types import Node
from ..utils import set_sockets, AVAILABLE_NTREES


class TemplateColorPaletteCollectionUL(bpy.types.UIList):
    bl_idname = 'DATANODES_UL_template_color_palette_collection'

    def draw_item(self, context, layout, data, item,
                  icon, active_data, active_propname, index):
        layout.prop(item, 'name', text='', emboss=False)
        row = layout.row(align=True)
        for color_item in item.colors:
            row.prop(color_item, 'color', text='')


def _find_maximum_length(items):
    list_len = [len(i) for i in items]
    return max(list_len)


class ColorPalette(Node):
    """Color Palette node"""
    bl_idname = 'ColorPaletteNodeType'
    bl_label = 'Color Palette'

    def update_props(self, context):
        self.update()

    settings: bpy.props.BoolProperty(
        name='Settings',
        default=True)
    palette_index: bpy.props.IntProperty(
        name='Palette Index',
        default=0,
        update=update_props)

    def add_outputs(self):
        items = [p.colors for p in bpy.context.scene.color_palettes]
        length = _find_maximum_length(items)
        for i in range(length):
            if len(self.outputs) >= length:
                break
            self.outputs.new('NodeSocketColor', 'Color')

    def init(self, context):
        self.add_outputs()

    def update(self):
        scene = bpy.context.scene
        if not scene.color_palettes:
            return
        palette = scene.color_palettes[self.palette_index]
        for index, output in enumerate(self.outputs):
            if index >= len(palette.colors):
                continue
            value = palette.colors[index].color
            set_sockets(output, value)

    def draw_buttons(self, context, layout):
        if self.settings:
            row = layout.row()
            row.prop(self, 'settings', text='', icon='TRIA_DOWN', emboss=False)
            row = layout.row()
            row.template_list(
                TemplateColorPaletteCollectionUL.bl_idname, '',
                context.scene, 'color_palettes', self, 'palette_index')
            col = row.column(align=True)
            col.operator('scene.add_color_palette', icon='ADD', text='')
            col.operator('scene.remove_color_palette', icon='REMOVE', text='')
        else:
            row = layout.row()
            row.prop(
                self, 'settings', text='', icon='TRIA_RIGHT', emboss=False)

        if context.scene.color_palettes:
            palette = context.scene.color_palettes[self.palette_index]
            row = layout.row(align=True)
            row.operator('scene.add_color_palette_color', text='', icon='ADD')
            for color_item in palette.colors:
                row.prop(color_item, 'color', text='')
            row.operator(
                'scene.remove_color_palette_color', text='', icon='REMOVE')

    def draw_label(self):
        return 'Color Palette'


class ColorPaletteAdd(bpy.types.Operator):
    bl_idname = 'scene.add_color_palette'
    bl_label = 'Add Color Palette'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.node
        color_palettes = context.scene.color_palettes
        p = color_palettes.add()
        p.name = str(len(color_palettes))
        for i in range(3):
            p.colors.add()
        node.palette_index = len(color_palettes) - 1
        node.add_outputs()
        return {'FINISHED'}


class ColorPaletteRemove(bpy.types.Operator):
    bl_idname = 'scene.remove_color_palette'
    bl_label = 'Remove Color Palette'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.node
        color_palettes = context.scene.color_palettes
        color_palettes.remove(node.palette_index)
        if node.palette_index > 0:
            node.palette_index -= 1
        return {'FINISHED'}


class ColorPaletteAddColor(bpy.types.Operator):
    bl_idname = 'scene.add_color_palette_color'
    bl_label = 'Add Color'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.node
        palette = context.scene.color_palettes[node.palette_index]
        palette.colors.add()
        # Sockets
        if (len(node.outputs) < len(palette.colors)):
            node.outputs.new('NodeSocketColor', 'Color')
        return {'FINISHED'}


class ColorPaletteRemoveColor(bpy.types.Operator):
    bl_idname = 'scene.remove_color_palette_color'
    bl_label = 'Remove Color'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.node
        palette = context.scene.color_palettes[node.palette_index]
        palette.colors.remove(len(palette.colors) - 1)
        return {'FINISHED'}
