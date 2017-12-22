bl_info = {
    'name': 'Box',
    'author': "Vincent Gires",
    'version': (0, 1),
    'blender': (2, 7, 0),
    'location': 'View3D > Add > Mesh',
    'description': 'Creates box/shelf/cabinet.',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Add Mesh'}


import bpy
import math

def create_panel(name='Panel', width=1.0, height=1.0, thickness=1.0):
    context = bpy.context
    data = bpy.data
    
    verts = [
        (0.0, 0.0, 0.0),
        (width, 0.0, 0.0),
        (0.0, 0.0, height),
        (width, 0.0, height),
        (0.0, thickness, 0.0),
        (width, thickness, 0.0),
        (0.0, thickness, height),
        (width, thickness, height)
        ]
    
    faces = [
        (1, 0, 2, 3),
        (7, 6, 4, 5),
        (3, 2, 6, 7),
        (5, 4, 0, 1),
        (2, 0, 4, 6),
        (7, 5, 1, 3)
        ]
    
    mesh = data.meshes.new('Mesh')
    mesh.from_pydata(verts, [], faces)
    object = data.objects.new(name, mesh)
    context.scene.objects.link(object)
    
    return object

'''
def create_cube(name='Cube'):
    context = bpy.context
    data = bpy.data
    
    verts = [(0.5, 0.5, -0.5),
             (0.5, -0.5, -0.5),
             (-0.5, -0.5, -0.5),
             (-0.5, 0.5, -0.5),
             (0.5, 0.5, 0.5),
             (0.5, -0.5, 0.5),
             (-0.5, -0.5, 0.5),
             (-0.5, 0.5, 0.5)]
    
    offset = 0.5
    for i, v in enumerate(verts):
        x, y, z = v
        verts[i] = (x+offset, y+offset, z+offset)
    
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7)
        ]
    
    mesh = data.meshes.new('Mesh')
    mesh.from_pydata(verts, [], faces)
    object = data.objects.new(name, mesh)
    context.scene.objects.link(object)
    
    return object
'''

def create_panels(width, height, length, thickness, inside):
    
    panels = []
    
    # cover
    #
    #
    
    # FRONT
    if inside:
        front = create_panel('front', width-(thickness*2), height, thickness)
        front.location.x = thickness
    else:
        front = create_panel('front', width, height, thickness)
    panels.append(front)
    
    # BACK
    if inside:
        back = create_panel('back', width-(thickness*2), height, thickness)
        back.location = (thickness, length-thickness, 0)
    else:
        back = create_panel('back', width, height, thickness)
        back.location = (0, length-thickness, 0)
    panels.append(back)
    
    # SIDE A
    if inside:
        side_a = create_panel('side_a', length, height, thickness)
        side_a.location.x = thickness
    else:
        side_a = create_panel('side_a', length-(2*thickness), height, thickness)
        side_a.location = (thickness, thickness, 0)
    side_a.rotation_euler.z = math.radians(90)
    panels.append(side_a)
    
    # SIDE B
    if inside:
        side_b = create_panel('side_b', length, height, thickness)
        side_b.location.x = width
    else:
        side_b = create_panel('side_b', length-(2*thickness), height, thickness)
        side_b.location = (width, thickness, 0)
    side_b.rotation_euler.z = math.radians(90)
    panels.append(side_b)
    
    return panels

def create_box(name, width, length, height, thickness, inside):
    context = bpy.context
    data = bpy.data
    
    panels = create_panels(width, height, length, thickness, inside)
    empty = data.objects.new('Empty', None)
    empty.name = name
    context.scene.objects.link(empty)
    
    for p in panels:
        p.parent = empty


class AddBox(bpy.types.Operator):
    '''Add a box/shelf/cabinet mesh.'''
    bl_idname = 'mesh.create_box'
    bl_label = 'Add box'
    bl_description = 'Create a box/shelf/cabinet mesh.'
    bl_options = {'REGISTER', 'UNDO'}
    
    width = bpy.props.FloatProperty(
        name='Width',
        subtype='DISTANCE',
        default=0.80)
    length = bpy.props.FloatProperty(
        name='Lenght',
        subtype='DISTANCE',
        default=0.60)
    height = bpy.props.FloatProperty(
        name='Height',
        subtype='DISTANCE',
        default=0.35)
    thickness = bpy.props.FloatProperty(
        name='Thickness',
        subtype='DISTANCE',
        default=0.018)
    inside = bpy.props.BoolProperty(
        name='Inside',
        default=False)
 
    def execute(self, context):
        create_box(
            name='Box',
            width=self.width,
            length=self.length,
            height=self.height,
            thickness=self.thickness,
            inside=self.inside
            )
 
        return {'FINISHED'}
 
    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}


def menu_add_box(self, context):
    self.layout.operator('mesh.create_box', text='Box', icon='MESH_CUBE')
 
 
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_add_box)
 
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_add_box)
 
if __name__ == '__main__':
    register()
