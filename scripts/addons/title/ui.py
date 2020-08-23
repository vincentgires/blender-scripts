import bpy


class TextsUL(bpy.types.UIList):
    bl_idname = 'TITLE_UL_TextsUL'

    def draw_item(
            self, context, layout, data,
            item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.25)
        row = split.row(align=True)
        row.prop(item, 'color', text='')
        split.prop(item, 'name', text='', icon_value=icon, emboss=False)
        layout.prop(item, 'display', text='')


class TitlePanel(bpy.types.Panel):
    bl_idname = 'TITLE_PT_TitlePanel'
    bl_label = 'Title'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Title'

    @classmethod
    def poll(cls, context):
        sequence_editor = context.scene.sequence_editor
        active_strip = sequence_editor.active_strip
        return active_strip

    def draw(self, context):
        scene = context.scene
        active_strip = scene.sequence_editor.active_strip
        layout = self.layout

        col = layout.column()
        col.label(text='Texts')
        sub = col.row()
        sub.template_list(
            TextsUL.bl_idname, '',
            active_strip, 'texts', active_strip, 'active_text_index')
        menu = sub.column()
        menu.operator(
            'scene.title_add_text',
            text='', icon='ADD')
        menu.operator(
            'scene.title_remove_text',
            text='', icon='REMOVE')

        active_text = active_strip.texts[active_strip.active_text_index]
        col = layout.column()
        col.prop(active_text, 'position')
        col.prop(active_text, 'size')
        # TODO
        # col.prop(active_text, 'font')
