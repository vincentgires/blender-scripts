import bpy
import os
import shutil
import json


class UIBrowser(bpy.types.Panel):
    bl_label = 'Browser'
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Browser'

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        col = layout.column(align=True)
        col.prop(wm.sequence_player, 'directory_path', text='')

        path = wm.sequence_player.directory_path
        if path:
            row = col.row(align=True)

            btn = row.operator('screen.browse_folder', text=' ', icon='BACK')
            btn.back = True
            show_folders = wm.sequence_player.show_folders
            prop_icon = 'TRIA_DOWN' if show_folders else 'TRIA_RIGHT'
            row.prop(wm.sequence_player, 'show_folders',
                     text='', icon=prop_icon, emboss=False)

            if show_folders:
                sub = col.column(align=True)
                items = [os.path.join(path, i) for i in os.listdir(path)
                         if os.path.isdir(os.path.join(path, i))]
                items.sort()
                for item in items:
                    btn = sub.operator(
                        'screen.browse_folder',
                        text=os.path.basename(item),
                        icon='FILE_FOLDER')
                    btn.folderpath = item
                    btn.back = False

        layout.template_icon_view(
            wm.sequence_player, 'directory_image_preview', True)

        if wm.sequence_player.directory_image_preview:
            col = layout.column(align=True)
            show_files = wm.sequence_player.show_files
            prop_icon = 'TRIA_DOWN' if show_files else 'TRIA_RIGHT'
            if show_files:
                sub = col.column(align=True)
                sub.prop(wm.sequence_player, 'show_files',
                         text=' ', icon=prop_icon, emboss=False)
                sub.prop(wm.sequence_player, 'directory_image_preview',
                         expand=show_files)
            else:
                sub = col.row(align=True)
                sub.prop(wm.sequence_player, 'directory_image_preview',
                         text='', expand=show_files)
                sub.prop(wm.sequence_player, 'show_files',
                         text='', icon=prop_icon, emboss=False)


class UIDisplay(bpy.types.Panel):
    bl_label = 'Display'
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Display'

    def draw(self, context):
        scene = context.scene
        sc = context.space_data

        layout = self.layout
        row = layout.row(align=True)
        sub = row.row(align=True)
        sub.prop(sc, 'show_red_channel',
                 text='R', toggle=True, icon='COLOR_RED')
        sub.prop(sc, 'show_green_channel',
                 text='G', toggle=True, icon='COLOR_GREEN')
        sub.prop(sc, 'show_blue_channel',
                 text='B', toggle=True, icon='COLOR_BLUE')
        row.separator()
        row.prop(sc, 'use_grayscale_preview', text='B/W',
                 toggle=True, icon='IMAGE_ALPHA')

        clip = sc.clip
        if clip:
            col = layout.column(align=True)
            col.label(text="Aspect Ratio")
            row = col.row()
            row.prop(clip, "display_aspect", text="")


class UIColorManagement(bpy.types.Panel):
    bl_label = 'Color Management'
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Display'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.template_colormanaged_view_settings(scene, 'view_settings')


class UISettings(bpy.types.Panel):
    bl_label = 'Settings'
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Settings'

    def draw(self, context):
        user_preferences = context.user_preferences
        scene = context.scene
        layout = self.layout
        layout.prop(user_preferences.system, 'memory_cache_limit')


class UIMediaInfo(bpy.types.Panel):
    bl_label = 'MediaInfo'
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'MediaInfo'

    @classmethod
    def poll(cls, context):
        for space in context.area.spaces:
            if space.type == 'CLIP_EDITOR':
                clip = space.clip
                if not clip:
                    return None
        app_exist = shutil.which('mediainfo')
        return app_exist

    def draw(self, context):
        scene = context.scene
        area = context.area
        layout = self.layout
        layout.operator('scene.get_mediainfo')

        for space in area.spaces:
            if space.type == 'CLIP_EDITOR':
                clip = space.clip
                if clip.mediainfo:
                    for line in clip.mediainfo.splitlines():
                        if line == '':
                            continue
                        elif ':' not in line:
                            box = layout.box()
                            col = box.column(align=True)
                        col.label(' '.join(line.split()))
