import bpy
from qt_integration import QtWindowEventLoop
from qt_integration.qt_window import ExampleWidget

class CustomWindow(QtWindowEventLoop):
    bl_idname = 'screen.custom_window'
    bl_label = 'Custom window'
    
    def __init__(self):
        super().__init__(widget=ExampleWidget)

class QtPanelExample(bpy.types.Panel):
    bl_label = 'Qt'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.custom_window')
