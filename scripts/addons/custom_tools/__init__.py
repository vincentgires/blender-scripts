import bpy
from bpy.types import Operator
from . import animation, image, movieclip, render, sequencer, node, viewport

bl_info = {
    'name': 'Custom tools',
    'author': 'Vincent Girès',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'category': '3D View'}


def header_color_management(self, context):
    if context.region.alignment == 'RIGHT':
        scene = context.scene
        layout = self.layout
        row = layout.row(align=True)
        row.operator('scene.reset_exposure', text='Exp')
        row.prop(scene.view_settings, 'exposure', text='')
        row = layout.row(align=True)
        row.operator('scene.reset_gamma', text='Y')
        row.prop(scene.view_settings, 'gamma', text='')


def image_image_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator('scene.set_image_input_transform')


def clip_clip_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator('scene.set_movieclip_input_transform')


def node_node_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator('scene.set_image_node_input_transform')


def render_menu_draw(self, context):
    self.layout.operator('render.render_gif')


def sequencer_add_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator('scene.add_multiple_movies')
    self.layout.operator(
        'sequencer.create_adjustment_strip',
        text='Ajustment Layer from active')


def sequencer_strip_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator('scene.open_strip_as_movieclip')
    self.layout.operator('scene.add_strip_as_compositing')
    self.layout.operator('scene.set_strip_input_transform')
    self.layout.operator('scene.set_strip_proxy_quality')


class ResetExposure(Operator):
    bl_idname = 'scene.reset_exposure'
    bl_label = 'Reset exposure'
    bl_description = 'Reset exposure to 0'

    def execute(self, context):
        context.scene.view_settings.exposure = 0
        return {'FINISHED'}


class ResetGamma(Operator):
    bl_idname = 'scene.reset_gamma'
    bl_label = 'Reset gamma'
    bl_description = 'Reset gamma to 1'

    def execute(self, context):
        context.scene.view_settings.gamma = 1
        return {'FINISHED'}


keymaps = list()
classes = (
    ResetExposure,
    ResetGamma,
    animation.PoseToEmpty,
    image.SetImageInputTransform,
    movieclip.SetMovieClipInputTransform,
    node.SetImageNodeInputTransform,
    render.RenderToGif,
    sequencer.SequencerCustomPanel,
    sequencer.OpenStripAsMovieclip,
    sequencer.AddStripAsCompositing,
    sequencer.DisableSceneStrips,
    sequencer.SetActiveSceneFromStrip,
    sequencer.CreateAdjustmentStrip,
    sequencer.AddMultipleMovies,
    sequencer.SetStripInputTransform,
    sequencer.SetStripProxyQuality,
    viewport.AimNormal,
    viewport.LookThroughSelected)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_HT_upper_bar.prepend(header_color_management)
    bpy.types.IMAGE_MT_image.append(image_image_menu_draw)
    bpy.types.CLIP_MT_clip.append(clip_clip_menu_draw)
    bpy.types.NODE_MT_node.append(node_node_menu_draw)
    bpy.types.TOPBAR_MT_render.append(render_menu_draw)
    bpy.types.SEQUENCER_MT_add.append(sequencer_add_menu_draw)
    bpy.types.SEQUENCER_MT_strip.append(sequencer_strip_menu_draw)

    # Keymaps
    #kc = bpy.context.window_manager.keyconfigs.addon

    #km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    #kmi = km.keymap_items.new('node.double_click',
                              #'ACTIONMOUSE', 'DOUBLE_CLICK')
    #keymaps.append((km, kmi))

    #km = kc.keymaps.new(name='Window', space_type='EMPTY')
    #kmi = km.keymap_items.new('compo_node_transform_grab.call', 'G', 'PRESS')
    #keymaps.append((km, kmi))


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_HT_upper_bar.remove(header_color_management)
    bpy.types.IMAGE_MT_image.remove(image_image_menu_draw)
    bpy.types.CLIP_MT_clip.remove(clip_clip_menu_draw)
    bpy.types.NODE_MT_node.remove(node_node_menu_draw)
    bpy.types.TOPBAR_MT_render.remove(render_menu_draw)
    bpy.types.SEQUENCER_MT_add.remove(sequencer_add_menu_draw)
    bpy.types.SEQUENCER_MT_strip.remove(sequencer_strip_menu_draw)

    # Keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()


if __name__ == '__main__':
    register()
