import bpy
from . import render
#from . import lighting
#from . import animation
#from . import look_through
#from . import node
from . import sequencer


bl_info = {
    'name': 'Custom tools',
    'author': 'Vincent Girès',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'category': '3D View'}


def header_color_management(self, context):
    scene = context.scene
    layout = self.layout
    layout.operator('scene.reset_exposure', emboss=False, text='Exposure')
    layout.prop(scene.view_settings, 'exposure', emboss=False, text='')
    layout.operator('scene.reset_gamma', emboss=False, text='Gamma')
    layout.prop(scene.view_settings, 'gamma', emboss=False, text='')


def render_menu_draw(self, context):
    self.layout.operator('render.render_gif')


class ResetExposure(bpy.types.Operator):
    bl_idname = 'scene.reset_exposure'
    bl_label = 'Reset Exposure'

    def execute(self, context):
        context.scene.view_settings.exposure = 0
        return{'FINISHED'}


class ResetGamma(bpy.types.Operator):
    bl_idname = 'scene.reset_gamma'
    bl_label = 'Reset Gamma'

    def execute(self, context):
        context.scene.view_settings.gamma = 1
        return{'FINISHED'}


keymaps = list()
classes = (
    ResetExposure,
    ResetGamma,
    render.RenderToGif,
    sequencer.SequencerCustomPanel,
    sequencer.OpenStripAsMovieclip,
    sequencer.OpenStripAsCompositing,
    sequencer.DisableSceneStrips,
    sequencer.SetActiveSceneFromStrip,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_HT_upper_bar.append(header_color_management)
    bpy.types.TOPBAR_MT_render.append(render_menu_draw)

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
    bpy.types.INFO_HT_header.remove(header_color_management)
    bpy.types.TOPBAR_MT_render.remove(render_menu_draw)

    # Keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()


if __name__ == '__main__':
    register()
