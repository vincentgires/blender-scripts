import bpy
import sys
import os
from bl_app_templates_user import sequence_player

bpy.ops.wm.read_homefile(
    use_splash=True, app_template='sequence_player')

args = sequence_player.argconfig.getargs()
path = args.path

if path:
    path = os.path.normpath(path)
    path = path.replace('//', '/')
    if os.path.isdir(path):
        wm = bpy.context.window_manager
        wm.sequence_player.directory_path = path
    elif sequence_player.check_file_extension(path):
        bpy.ops.scene.load_clip(filepath=path)

