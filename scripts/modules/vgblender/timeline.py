import bpy
from bpy.types import Operator, WorkSpaceTool


def go_to_next_frame(scene, frames, reverse=False):
    for frame in frames:
        if reverse:
            if frame < scene.frame_current:
                scene.frame_current = int(frame)
                break
        else:
            if frame > scene.frame_current:
                scene.frame_current = int(frame)
                break


def view_all(context=None):
    context = context or bpy.context
    if not context.screen:
        return None
    for area in context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    ctx = context.copy()
                    ctx['area'] = area
                    ctx['region'] = region
                    bpy.ops.action.view_all(ctx)


class InteractiveTimeline(Operator):
    bl_idname = 'screen.interactive_timeline'
    bl_label = 'Interactive timeline'

    @classmethod
    def poll(cls, context):
        return context.region.type == 'PREVIEW'

    def modal(self, context, event):
        w = context.window_manager.windows[0]
        w.cursor_modal_set('SCROLL_X')

        context.area.header_text_set(
            'Left/right to change frame | '
            'enter key or left click to valid | '
            'escape or right clic to exit')

        scene = context.scene
        frame_start = context.scene.frame_start
        frame_end = context.scene.frame_end

        match event.type:
            case 'RET' | 'NUMPAD_ENTER' | 'SPACE' | 'LEFTMOUSE':
                w.cursor_modal_restore()
                context.area.header_text_set(text='')
                return {'FINISHED'}
            case 'ESC' | 'RIGHTMOUSE':
                context.scene.frame_current = self.frame_init
                w.cursor_modal_restore()
                context.area.header_text_set(text='')
                return {'CANCELLED'}
            case 'MOUSEMOVE':
                target_frame = self.frame_init + (
                    event.mouse_region_x - self.region_x_init)
                if target_frame > frame_start and target_frame < frame_end:
                    scene.frame_current = target_frame
                elif target_frame <= frame_start:
                    scene.frame_current = frame_start
                elif target_frame >= frame_end:
                    scene.frame_current = frame_end

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.frame_init = context.scene.frame_current
        self.region_x_init = event.mouse_region_x
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class InteractiveTimelineTool(WorkSpaceTool):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_context_mode = None
    bl_idname = 'timeline.interactive_move'
    bl_label = 'Interactive timeline'
    bl_icon = 'ops.transform.transform'
    bl_widget = None
    bl_keymap = (
        ('screen.interactive_timeline',
         {'type': 'LEFTMOUSE', 'value': 'PRESS'}, None),
    )


def register():
    bpy.utils.register_class(InteractiveTimeline)
    bpy.utils.register_tool(InteractiveTimelineTool)


def unregister():
    bpy.utils.unregister_class(InteractiveTimeline)
    bpy.utils.unregister_tool(InteractiveTimelineTool)
