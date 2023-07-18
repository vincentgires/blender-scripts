from bpy.types import Panel


def draw_color_management_display(layout, context):
    layout.use_property_split = True
    layout.use_property_decorate = False
    scene = context.scene
    view = scene.view_settings
    flow = layout.grid_flow(
        row_major=True,
        columns=0,
        even_columns=False,
        even_rows=False,
        align=True)
    col = flow.column(align=True)
    col.prop(scene.display_settings, 'display_device')
    col.separator()
    col.prop(view, 'view_transform')
    col.prop(view, 'look')
    col = flow.column(align=True)
    col.prop(view, 'exposure')
    col.prop(view, 'gamma')


class ImageEditorColorManagement():
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'View'
    bl_label = 'Color Management'


class SequencerColorManagement():
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'View'
    bl_label = 'Color Management'


class SequencerColorManagementDisplay(SequencerColorManagement, Panel):
    bl_idname = 'SEQUENCER_PT_color_management_display'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        draw_color_management_display(layout, context)
        layout.prop(
            scene.sequencer_colorspace_settings, 'name', text='Sequencer')


class ImageEditorColorManagementDisplay(ImageEditorColorManagement, Panel):
    bl_idname = 'IMAGE_EDITOR_PT_color_management_display'

    def draw(self, context):
        draw_color_management_display(self.layout, context)


class ColorManagementCurves():
    bl_label = 'Use Curves'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        scene = context.scene
        view = scene.view_settings
        self.layout.prop(view, 'use_curve_mapping', text='')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        view = scene.view_settings
        layout.use_property_split = False
        layout.use_property_decorate = False
        layout.enabled = view.use_curve_mapping
        layout.template_curve_mapping(
            view,
            'curve_mapping',
            type='COLOR',
            levels=True)


class SequencerColorManagementCurves(
        ColorManagementCurves, SequencerColorManagement, Panel):
    bl_idname = 'SEQUENCER_PT_color_management_curves'
    bl_parent_id = 'SEQUENCER_PT_color_management_display'


class ImageEditorColorManagementCurves(
        ColorManagementCurves, ImageEditorColorManagement, Panel):
    bl_idname = 'IMAGE_EDITOR_PT_color_management_curves'
    bl_parent_id = 'IMAGE_EDITOR_PT_color_management_display'
