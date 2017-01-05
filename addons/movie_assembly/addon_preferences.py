import bpy
import sys, os, logging

ADDON_NAME = os.path.basename(os.path.dirname(__file__))

class MovieAssemblyVariables(bpy.types.PropertyGroup):
    
    name = bpy.props.StringProperty(
        name = 'Variable',
        default = ''
    )
    
    

class MovieAssemblyProjects(bpy.types.PropertyGroup):
    
    name = bpy.props.StringProperty(
        name = 'Name',
        default = 'Project'
    )
    
    dirpath = bpy.props.StringProperty(
        name = 'Path',
        subtype = 'DIR_PATH'
    )
    
    path_variables = bpy.props.CollectionProperty(type=MovieAssemblyVariables)


class MovieAssemblyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME
    
    projects = bpy.props.CollectionProperty(type=MovieAssemblyProjects)
    
    def draw(self, context):
        layout = self.layout
        layout.operator('movie_assembly_add_project.btn')
        
        for index, project in enumerate(self.projects):
            box = layout.box()
            box.prop(project, 'name')
            row = box.row()
            split = row.split(percentage=0.75)
            split.prop(project, 'dirpath')
            for i, variable in enumerate(project.path_variables):
                row_variable = split.row(align=True)
                row_variable.prop(variable, 'name', text='')
                remove = row_variable.operator('movie_assembly_remove_path.btn', text='', icon='ZOOMOUT')
                remove.project_index = index
                remove.variable_index = i
                
            add_path = box.operator('movie_assembly_add_path.btn')
            add_path.project_index = index
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
    bl_label = 'Remove project'
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



class MovieAssemblyAddPath(bpy.types.Operator):
    bl_idname = 'movie_assembly_add_path.btn'
    bl_label = 'Add new path'
    bl_options = {'REGISTER', 'UNDO'}
    
    project_index = bpy.props.IntProperty(
        name = 'Project index',
        default = 0
    )
    
    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[ADDON_NAME].preferences
        addon_prefs.projects[self.project_index].path_variables.add()

        return{'FINISHED'}


class MovieAssemblyRemovePath(bpy.types.Operator):
    bl_idname = 'movie_assembly_remove_path.btn'
    bl_label = 'Remove variable'
    bl_options = {'REGISTER', 'UNDO'}
    
    project_index = bpy.props.IntProperty(
        name = 'Project index',
        default = 0
    )
    
    variable_index = bpy.props.IntProperty(
        name = 'Project index',
        default = 0
    )
    
    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[ADDON_NAME].preferences
        project = addon_prefs.projects[self.project_index]
        project.path_variables.remove(self.variable_index)

        return{'FINISHED'}
