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
    
    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7)]
    
    mesh = data.meshes.new('Mesh')
    mesh.from_pydata(verts, [], faces)
    object = data.objects.new(name, mesh)
    context.scene.objects.link(object)
    
    return object


def create_panels(width, length, height, thickness):
    
    panels = []
    
    bottom = create_cube('bottom')
    bottom.scale = (width, length, thickness)
    panels.append(bottom)
    
    # cover
    #
    #
    
    side_a = create_cube('side_a')
    side_a.location = (0, 0, thickness)
    side_a.scale = (thickness, length, height-thickness)
    panels.append(side_a)
    
    side_b = create_cube('side_b')
    side_b.location = (width-thickness, 0, thickness)
    side_b.scale = (thickness, length, height-thickness)
    panels.append(side_b)
    
    front = create_cube('front')
    front.location = (thickness, 0, thickness)
    front.scale = (width-(thickness*2), thickness, height-thickness)
    panels.append(front)
    
    back = create_cube('back')
    back.location = (thickness, length-thickness, thickness)
    back.scale = (width-(thickness*2), thickness, height-thickness)
    panels.append(back)
    
    return panels

def create_box(name, width, length, height, thickness):
    context = bpy.context
    data = bpy.data
    
    panels = create_panels(width, length, height, thickness)
    empty = data.objects.new('Empty', None)
    empty.name = name
    context.scene.objects.link(empty)
    
    for p in panels:
        p.parent = empty


class AddBox(bpy.types.Operator):
    '''Add a box/shelf/cabinet mesh.'''
    bl_idname = "mesh.create_box"
    bl_label = "Add box"
    bl_description = "Create a box/shelf/cabinet mesh."
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
 
    def execute(self, context):
        create_box(
            name='Box',
            width=self.width,
            length=self.length,
            height=self.height,
            thickness=self.thickness
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
 
if __name__ == "__main__":
    register()
