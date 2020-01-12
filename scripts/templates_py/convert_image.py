import bpy
import sys
import os

data = bpy.data
context = bpy.context
scene = context.scene

# Remove all objects
for obj in data.objects:
    data.objects.remove(obj)

# Scene setup
scene.use_nodes = True

# Clear default nodes
node_tree = scene.node_tree
for node in node_tree.nodes:
    node_tree.nodes.remove(node)

files = sys.argv[sys.argv.index('--') + 1:]
for f in files:
    image_node = node_tree.nodes.new('CompositorNodeImage')
    output_node = node_tree.nodes.new('CompositorNodeComposite')
    image = data.images.load(f)
    image.colorspace_settings.name = 'lin_rec709'
    image_node.image = image
    node_tree.links.new(image_node.outputs[0], output_node.inputs[0])

    x, y = image.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 95

    root, ext = os.path.splitext(f)
    outputpath = root + '.jpg'
    scene.render.filepath = outputpath
    bpy.ops.render.render(write_still=True)
