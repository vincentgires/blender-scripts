import bpy
import sys, os, logging

addon_name = os.path.basename(os.path.dirname(__file__))

class SEQUENCER_movie_assembly(bpy.types.Panel):
    bl_label = "Movie Assembly"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    
    
    def draw(self, context):
        layout = self.layout
        
        for i in context.user_preferences.addons[addon_name].preferences.project_settings:
            print (i)
        #layout.props_enum(self, material_item)
        

class SEQUENCER_strip_version(bpy.types.Panel):
    bl_label = "Version"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    
    '''
    #@staticmethod
    def draw_header(self, context):
        layout = self.layout
        layout.label("", icon="LINENUMBERS_ON")
    '''
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.label("Type")
        

