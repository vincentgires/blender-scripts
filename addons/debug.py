bl_info = {
    "name": "Debug",
    "author": "Vincent Gires",
    "description": "---",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "location": "Tool shelf / Properties panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"}


import bpy, sys

#sys.path.append("C:/SOFT/eclipse/java-mars/plugins/org.python.pydev_4.4.0.201510052309/pysrc/")
sys.path.append("/home/vincent/.p2/pool/plugins/org.python.pydev_5.3.1.201610311318/pysrc/")
import pydevd

'''
class SEQUENCER_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.operator("debug_connect_to_eclipse.btn")
        layout.operator("debug_disconnect_to_eclipse.btn")
'''

def draw_eclipse_panel(layout):
    layout.operator("debug_connect_to_eclipse.btn")
    layout.operator("debug_disconnect_to_eclipse.btn")

class VIEW3D_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Debug"

    def draw(self, context):
        layout = self.layout
        draw_eclipse_panel(layout)
        
class NODE_EDITOR_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Debug"

    def draw(self, context):
        layout = self.layout
        draw_eclipse_panel(layout)


class SEQUENCER_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        draw_eclipse_panel(layout)


class DEBUG_connect_to_eclipse(bpy.types.Operator):
    bl_idname = "debug_connect_to_eclipse.btn"
    bl_label = "Connect to Eclipse/Pydev debugger"
    
    def execute(self, context):
        pydevd.settrace(stdoutToServer=True, stderrToServer=True, suspend=False)
        
        return{'FINISHED'}

class DEBUG_disconnect_to_eclipse(bpy.types.Operator):
    bl_idname = "debug_disconnect_to_eclipse.btn"
    bl_label = "Disconnect Eclipse/Pydev debugger"
    
    def execute(self, context):
        pydevd.stoptrace()
        
        return{'FINISHED'}

        
        
        
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()


    
