import bpy


class SEQUENCER_Image_Preview(bpy.types.Panel):
    bl_label = 'Images'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Images'
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        wm = context.window_manager
        layout = self.layout
        
        layout.template_icon_view(wm, 'image_preview', show_labels=False)

class IMAGE_EDITOR_Image_Preview(bpy.types.Panel):
    bl_label = 'Images'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Images'
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        wm = context.window_manager
        layout = self.layout
        
        layout.template_icon_view(wm, 'image_preview', show_labels=False)
