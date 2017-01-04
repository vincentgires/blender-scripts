import bpy
import sys, os, logging

class SEQUENCER_MovieAssembly(bpy.types.Panel):
    bl_label = "Movie Assembly"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Movie Assembly"
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene.movie_assembly, "project_index")


class SEQUENCER_StripVersion(bpy.types.Panel):
    bl_label = "Version"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Movie Assembly"
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.label("Type")
        


