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

def create_board(name='Panel', width=1.0, height=1.0, thickness=1.0):
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

def create_boards(**kwargs):
    width = kwargs['width']
    height = kwargs['height']
    length = kwargs['length']
    thickness = kwargs['thickness']
    inside = kwargs['inside']
    bottom = kwargs['bottom']
    cover = kwargs['cover']
    
    boards = []
    
    # FRONT
    if inside:
        front = create_board(
            'front', width-(thickness*2), height, thickness)
        front.location.x = thickness
    else:
        front = create_board(
            'front', width, height, thickness)
    boards.append(front)
    
    # BACK
    if inside:
        back = create_board(
            'back', width-(thickness*2), height, thickness)
        back.location = (thickness, length-thickness, 0)
    else:
        back = create_board(
            'back', width, height, thickness)
        back.location = (0, length-thickness, 0)
    boards.append(back)
    
    # SIDE A
    if inside:
        side_a = create_board(
            'side_a', length, height, thickness)
        side_a.location.x = thickness
    else:
        side_a = create_board(
            'side_a', length-(2*thickness), height, thickness)
        side_a.location = (thickness, thickness, 0)
    side_a.rotation_euler.z = math.radians(90)
    boards.append(side_a)
    
    # SIDE B
    if inside:
        side_b = create_board(
            'side_b', length, height, thickness)
        side_b.location.x = width
    else:
        side_b = create_board(
            'side_b', length-(2*thickness), height, thickness)
        side_b.location = (width, thickness, 0)
    side_b.rotation_euler.z = math.radians(90)
    boards.append(side_b)
    
    # BOTTOM
    if bottom.enable:
        if bottom.inside:
            bottom_board = create_board(
                'bottom',
                width-(2*thickness),
                length-(2*thickness),
                bottom.thickness
                )
            bottom_board.location = (width-thickness, thickness, 0)
            bottom_board.rotation_euler = (
                math.radians(90), 0, math.radians(180))
            
        else:
            bottom_board = create_board(
                'bottom', width, length, bottom.thickness)
            bottom_board.location = (width, 0, -thickness)
            bottom_board.rotation_euler = (
                math.radians(90), 0, math.radians(180))
        
        boards.append(bottom_board)
    
    return boards

def create_box(**kwargs):
    context = bpy.context
    data = bpy.data
    
    boards = create_boards(**kwargs)
    empty = data.objects.new('Empty', None)
    empty.name = kwargs['name']
    context.scene.objects.link(empty)
    
    for b in boards:
        b.parent = empty


class BoardProperties(bpy.types.PropertyGroup):
    enable = bpy.props.BoolProperty(
        name='Enable',
        default=False)
    
    thickness = bpy.props.FloatProperty(
        name='Thickness',
        subtype='DISTANCE',
        default=0.018)
    
    offset = bpy.props.FloatProperty(
        name='Offset',
        subtype='DISTANCE',
        default=False)
    
    inside = bpy.props.BoolProperty(
        name='Inside',
        default=True)

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
    
    bottom = bpy.props.PointerProperty(
        type=BoardProperties,
        name='Bottom')
    
    cover = bpy.props.PointerProperty(
        type=BoardProperties,
        name='Cover')
    
    #shelf = bpy.props.CollectionProperty(
        #type=BoardProperties,
        #name='Bottom')
        
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.prop(self, 'width')
        col.prop(self, 'length')
        col.prop(self, 'height')
        col.prop(self, 'thickness')
        col.prop(self, 'inside')
        
        boards = [
            self.bottom,
            self.cover
            ]
        
        for board in boards:
            col = layout.column(align=True)
            col.label(board.name)
            col.prop(board, 'enable')
            col.prop(board, 'thickness')
            col.prop(board, 'inside')
    
    def execute(self, context):
        create_box(
            name='Shelf',
            width=self.width,
            length=self.length,
            height=self.height,
            thickness=self.thickness,
            inside=self.inside,
            bottom=self.bottom,
            cover=self.cover
            )
 
        return {'FINISHED'}
 
    def invoke(self, context, event):
        self.bottom.name = 'Bottom'
        self.cover.name = 'Cover'
        
        self.execute(context)
        return {'FINISHED'}


def menu_add_shelf(self, context):
    self.layout.operator('mesh.create_box', text='Box', icon='MESH_CUBE')
 
 
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_add_shelf)
 
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_add_shelf)
 
if __name__ == '__main__':
    register()
