import bpy
import sys
import logging

bl_info = {
    'name': 'Debug',
    'author': 'Vincent Girès',
    'description': 'Connect external debugger',
    'version': (0, 0, 1),
    'blender': (2, 7, 8),
    'location': 'Tool shelf / Properties panel',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Development'}


class DEBUG_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    pydevd_dir = bpy.props.StringProperty(
        name='pydevd directory',
        subtype='DIR_PATH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'pydevd_dir')


def draw_debug_panel(layout):
    layout.operator('debug_connect_to_eclipse.btn')
    layout.operator('debug_disconnect_to_eclipse.btn')
    layout.operator_menu_enum('debug_logging_setlevels.menu', 'typeEnum')


class VIEW3D_debug(bpy.types.Panel):
    bl_label = 'Debug'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Debug'

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)


class NODE_EDITOR_debug(bpy.types.Panel):
    bl_label = 'Debug'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Debug'

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)


class SEQUENCER_debug(bpy.types.Panel):
    bl_label = 'Debug'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Debug'

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)


class DEBUG_connect_to_eclipse(bpy.types.Operator):
    bl_idname = 'debug_connect_to_eclipse.btn'
    bl_label = 'Connect to Eclipse/Pydev debugger'

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences
        sys.path.append(addon_prefs.pydevd_dir)
        try:
            import pydevd
            pydevd.settrace(
                stdoutToServer=True, stderrToServer=True, suspend=False)
        except Exception:
            raise ImportError('pydevd module is missing')
        return{'FINISHED'}


class DEBUG_disconnect_to_eclipse(bpy.types.Operator):
    bl_idname = 'debug_disconnect_to_eclipse.btn'
    bl_label = 'Disconnect Eclipse/Pydev debugger'

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences
        sys.path.append(addon_prefs.pydevd_dir)
        import pydevd
        pydevd.stoptrace()
        return{'FINISHED'}


class DEBUG_logging_setLevels(bpy.types.Operator):
    bl_idname = 'debug_logging_setlevels.menu'
    bl_label = 'Set Logger levels'

    def get_enum(self, context):
        return bpy.props.logging_setLevels

    typeEnum = bpy.props.EnumProperty(
        items=get_enum)

    def execute(self, context):
        logger = logging.getLogger()
        logger.setLevel(self.typeEnum)
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    bpy.props.logging_setLevels = [
        ('DEBUG', 'DEBUG', 'DEBUG'),
        ('INFO', 'INFO', 'INFO'),
        ('WARNING', 'WARNING', 'WARNING'),
        ('ERROR', 'ERROR', 'ERROR'),
        ('CRITICAL', 'CRITICAL', 'CRITICAL')]


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.props.logging_setLevels


if __name__ == '__main__':
    register()
