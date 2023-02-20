import bpy
from operator import attrgetter

assignation = {
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

preferences = bpy.context.preferences

for k, v in assignation.items():
    if not isinstance(v, dict):
        setattr(preferences, k, v)
    else:
        for attr_name, attr_value in v.items():
            obj = attrgetter(k)(preferences)
            setattr(obj, attr_name, attr_value)

wm = bpy.context.window_manager
wm.keyconfigs['Blender'].preferences.select_mouse = 'RIGHT'
