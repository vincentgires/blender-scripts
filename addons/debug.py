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


import bpy, sys, logging

#sys.path.append("C:/SOFT/eclipse/java-mars/plugins/org.python.pydev_4.4.0.201510052309/pysrc/")
sys.path.append("/home/vincent/.p2/pool/plugins/org.python.pydev_5.3.1.201610311318/pysrc/")
try:
    import pydevd
except:
    pass

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

def draw_debug_panel(layout):
    layout.operator("debug_connect_to_eclipse.btn")
    layout.operator("debug_disconnect_to_eclipse.btn")
    layout.operator_menu_enum("debug_logging_setlevels.menu", "typeEnum")

class VIEW3D_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Debug"

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)
        
class NODE_EDITOR_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Debug"

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)


class SEQUENCER_debug(bpy.types.Panel):
    bl_label = "Debug"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Debug"

    def draw(self, context):
        layout = self.layout
        draw_debug_panel(layout)


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

        

class DEBUG_logging_setLevels(bpy.types.Operator):
    bl_idname = "debug_logging_setlevels.menu"
    bl_label = "Set Logger levels"
    
    def get_enum(self, context):
        return bpy.props.logging_setLevels
    
    typeEnum = bpy.props.EnumProperty(
        items = get_enum
    )
    
    def execute(self, context):
        logger = logging.getLogger()
        logger.setLevel(self.typeEnum)
        
        return {"FINISHED"}
    
        
def register():
    bpy.utils.register_module(__name__)
    bpy.props.logging_setLevels = [
        ("DEBUG","DEBUG","DEBUG"),
        ("INFO","INFO","INFO"),
        ("WARNING","WARNING","WARNING"),
        ("ERROR","ERROR","ERROR"),
        ("CRITICAL","CRITICAL","CRITICAL")
        
    ]
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.props.logging_setLevels

if __name__ == "__main__":
	register()


    
