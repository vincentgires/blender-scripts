import bpy
import os
import logging


class LoadClip(bpy.types.Operator):
    bl_idname = 'scene.load_clip'
    bl_label = 'Load Clip'
    filepath = bpy.props.StringProperty(name='Filepath')

    def execute(self, context):
        data = bpy.data
        movieclips = data.movieclips
        scene = context.scene
        wm = context.window_manager

        clip = movieclips.load(self.filepath, check_existing=True)
        if clip:
            logging.info('{} loaded'.format(clip.filepath))

            # display clip in all clip editors
            for screen in data.screens:
                for area in screen.areas:
                    if area.type == 'CLIP_EDITOR':
                        for space in area.spaces:
                            if space.type == 'CLIP_EDITOR':
                                space.clip = clip

            context.scene.frame_start = 1
            context.scene.frame_end = clip.frame_duration

            # set defaults
            for tracking_object in clip.tracking.objects:
                tracking_object.keyframe_a = 1
                tracking_object.keyframe_b = 1

            # set browser
            wm.sequence_player.directory_path = os.path.dirname(clip.filepath)

        return {'FINISHED'}


class FolderNavigation(bpy.types.Operator):
    bl_idname = 'screen.browse_folder'
    bl_label = 'Browser folder'
    bl_description = 'Browser folder'
    folderpath = bpy.props.StringProperty(name='Folderpath')
    back = bpy.props.BoolProperty(name='Folderpath', default=False)

    def execute(self, context):
        wm = context.window_manager
        if self.back:
            parent_path = os.path.join(
                wm.sequence_player.directory_path,
                os.pardir)
            parent_path = os.path.normpath(parent_path)
            wm.sequence_player.directory_path = parent_path
        else:
            wm.sequence_player.directory_path = self.folderpath

        # put enum property to the first item
        # to be sure to not have empty preview if the folder contains images
        wm.sequence_player['directory_image_preview'] = 0
        return {'FINISHED'}


class InteractiveTimeline(bpy.types.Operator):
    bl_idname = 'screen.interactive_timeline'
    bl_label = 'Interactive timeline'
    region_x_init = None
    frame_init = None

    def modal(self, context, event):
        scene = context.scene
        w = context.window_manager.windows[0]
        w.cursor_modal_set('SCROLL_X')

        context.area.header_text_set((
            'Left/right to change frame | '
            'Enter key or left click to valid | '
            'Esc or right clic to exit'))

        self.mouse_position = (event.mouse_region_x, event.mouse_region_y)

        frame_start = scene.frame_start
        frame_end = scene.frame_end
        if self.region_x_init:
            target_frame = self.frame_init \
                + (event.mouse_region_x - self.region_x_init)
            if target_frame > frame_start and target_frame < frame_end:
                scene.frame_current = target_frame
            if target_frame <= frame_start:
                scene.frame_current = frame_start
            if target_frame >= frame_end:
                scene.frame_current = frame_end
        else:
            self.region_x_init = event.mouse_region_x
            self.frame_init = scene.frame_current

        if event.type in ('RET', 'NUMPAD_ENTER', 'LEFTMOUSE', 'SPACE'):
            w.cursor_modal_restore()
            context.area.header_text_set()
            return {'FINISHED'}

        elif event.type in ('RIGHTMOUSE', 'ESC'):
            context.scene.frame_current = self.frame_init
            w.cursor_modal_restore()
            context.area.header_text_set()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.mouse_position = ()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
