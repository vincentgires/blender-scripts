import bpy
import sys
import os
from vgblender.argconfig import get_args

FILE_EXT = '.jpg'

args = get_args()

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

output_node = node_tree.nodes.new('CompositorNodeComposite')
for f in args.inputs:
    image_node = node_tree.nodes.new('CompositorNodeImage')
    image = data.images.load(f)
    image.colorspace_settings.name = 'lin_rec2020'
    image_node.image = image
    node_tree.links.new(image_node.outputs[0], output_node.inputs[0])

    x, y = image.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 95

    if args.output:
        if args.output.endswith(FILE_EXT):
            outputpath = args.output
        else:
            # assume that output path is a directory, the filename extension
            # of each files is then replaced
            _, filename = os.path.split(f)
            outputpath = os.path.join(
                args.output, os.path.splitext(filename)[0] + FILE_EXT)
    else:
        root, _ = os.path.splitext(f)
        outputpath = root + FILE_EXT
    scene.render.filepath = outputpath
    bpy.ops.render.render(write_still=True)
