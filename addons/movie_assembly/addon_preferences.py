import bpy
import sys, os, logging

ADDON_NAME = os.path.basename(os.path.dirname(__file__))


class MovieAssemblyProjects(bpy.types.PropertyGroup):
    
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


class MovieAssemblyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME
    
    projects = bpy.props.CollectionProperty(type=MovieAssemblyProjects)
    
    def draw(self, context):
        layout = self.layout
        layout.operator('movie_assembly_add_project.btn')
        
        
        for index, project in enumerate(self.projects):
            box = layout.box()
            box.prop(project, 'name')
            box.prop(project, 'dirpath')
            box.prop(project, 'filename')
            remove = box.operator('movie_assembly_remove_project.btn')
            remove.projet_index = index



class MovieAssemblyAddProject(bpy.types.Operator):
    bl_idname = 'movie_assembly_add_project.btn'
    bl_label = 'Add new project'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[ADDON_NAME].preferences
        addon_prefs.projects.add()
        
        return{'FINISHED'}


class MovieAssemblyRemoveProject(bpy.types.Operator):
    bl_idname = 'movie_assembly_remove_project.btn'
    bl_label = 'Remove'
    bl_options = {'REGISTER', 'UNDO'}
    
    projet_index = bpy.props.IntProperty(
        name = 'Index',
        default = 0
    )
    
    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[ADDON_NAME].preferences
        addon_prefs.projects.remove(self.projet_index)
        
        return{'FINISHED'}
