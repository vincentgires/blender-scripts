import bpy

data = bpy.data
objects = data.objects

def create_cube(name='Cube'):
    
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
    bpy.context.scene.objects.link(object)
    
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
    
    panels = create_panels(width, length, height, thickness)
    
    empty = objects.new('Empty', None)
    empty.name = name
    bpy.context.scene.objects.link(empty)
    
    for p in panels:
        p.parent = empty

create_box(
    name='Box',
    width=30,
    length=70,
    height=10,
    thickness=1.8
    )


