import os
import argparse
import bpy
from vgblender.argconfig import get_args

FILE_EXT = '.jpg'

parser = argparse.ArgumentParser()
parser.add_argument(
    '-inputs',
    nargs='+',
    help='File inputs',
    required=False)
parser.add_argument(
    '-resolution',
    nargs='+',
    type=int,
    help='Resolution X Y',
    required=False)
parser.add_argument(
    '-colorspace',
    help='Footage colorspace',
    required=False)
parser.add_argument(
    '-displaydevice',
    help='OCIO Display Device',
    required=False)
parser.add_argument(
    '-viewtransform',
    help='OCIO View Transform',
    required=False)
parser.add_argument(
    '-output',
    help='File output',
    required=False)

args = get_args(parser)

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
    if args.colorspace:
        image.colorspace_settings.name = args.colorspace
    image_node.image = image
    node_tree.links.new(image_node.outputs[0], output_node.inputs[0])

    if args.resolution is not None:
        x, y = args.resolution
    else:
        x, y = image.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 95
    if args.displaydevice:
        scene.display_settings.display_device = args.displaydevice
    if args.viewtransform:
        scene.view_settings.view_transform = args.viewtransform

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
