import bpy
import sys, os, logging

addon_name = os.path.basename(os.path.dirname(__file__))



class MOVIE_ASSEMBLY_Project_Settings(bpy.types.PropertyGroup):
    
    name = bpy.props.StringProperty(
        name = 'Name',
        default = 'Project'
    )
    
    dirpath = bpy.props.StringProperty(
        name = 'Path',
        subtype = 'DIR_PATH'
    )
    
    filename = bpy.props.StringProperty(
        name='File',
        default='file.mov'
    )


class MOVIE_ASSEMBLY_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    project_settings = bpy.props.CollectionProperty(type=MOVIE_ASSEMBLY_Project_Settings)
    
    def draw(self, context):
        layout = self.layout
        layout.operator('movie_assembly_add_project.btn')
        
        
        for project in self.project_settings:
            box = layout.box()
            box.prop(project, 'name')
            box.prop(project, 'dirpath')
            box.prop(project, 'filename')
        



class MOVIE_ASSEMBLY_Add_Project(bpy.types.Operator):
    bl_idname = 'movie_assembly_add_project.btn'
    bl_label = 'Add new project'
    
    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[addon_name].preferences
        
        addon_prefs.project_settings.add()
        
        
        return{'FINISHED'}
