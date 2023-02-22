import bpy
from operator import attrgetter

preferences_assignation = {
    'use_preferences_save': False,  # Auto save preferences
    'view': {
        'show_splash': False,
        'show_developer_ui': True,
        'show_tooltips_python': True
    },
    'inputs': {
        'use_emulate_numpad': True,
        'use_mouse_continuous': True,  # Continuous grab
        'use_drag_immediately': False  # Release confirms
    },
    'system': {
        'memory_cache_limit': 12288,
        'sequencer_proxy_setup': 'MANUAL'
    },
    'filepaths': {
        'save_version': 0
    }
}

keyconfigs_assignation = {
    'select_mouse': 'RIGHT',
    'use_file_single_click': True  # Open folder on single click
}


def set_preferences(prefs, assignation):
    for k, v in assignation.items():
        if not isinstance(v, dict):
            setattr(prefs, k, v)
            continue
        for attr_name, attr_value in v.items():
            obj = attrgetter(k)(prefs)
            setattr(obj, attr_name, attr_value)


preferences = bpy.context.preferences
wm = bpy.context.window_manager
kc_preferences = wm.keyconfigs['Blender'].preferences

set_preferences(preferences, preferences_assignation)
set_preferences(kc_preferences, keyconfigs_assignation)

bpy.ops.wm.save_userpref()
