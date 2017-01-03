import bpy

class SEQUENCER_QT_INTEGRATION(bpy.types.Panel):
    bl_label = 'Qt'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Qt'
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        window_btn = layout.operator('qt_window.event_loop')
