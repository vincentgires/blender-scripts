import argparse
import bpy
from vgblender.path import normpath
from vgblender.argconfig import get_args
from vgblender.render.render import render_movie

parser = argparse.ArgumentParser()
parser.add_argument(
    '-input',
    help='File input',
    required=False)
parser.add_argument(
    '-startframe',
    type=int,
    help='Start frame to begin the clip',
    required=False)
parser.add_argument(
    '-endframe',
    type=int,
    help='End frame',
    required=False)
parser.add_argument(
    '-fps',
    type=int,
    help='FPS',
    required=False)
parser.add_argument(
    '-resolution',
    nargs='+',
    type=int,
    help='Resolution X Y',
    required=False)
parser.add_argument(
    '-colordepth',
    help='Color depth',
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
parser.add_argument(
    '-metadata',
    nargs='+',
    required=False)
parser.add_argument(
    '-codec',
    required=False)
parser.add_argument(
    '-qscale',
    required=False)

args = get_args(parser)

data = bpy.data
context = bpy.context
scene = context.scene


def process():
    # Remove all objects
    for obj in data.objects:
        data.objects.remove(obj)

    # Scene setup
    scene.use_nodes = True

    # Clear default nodes
    node_tree = scene.node_tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    start_frame = args.startframe or 1
    end_frame = args.endframe or start_frame

    image = data.images.load(normpath(args.input))
    image.source = 'SEQUENCE'
    if args.colorspace:
        image.colorspace_settings.name = args.colorspace
    image_node = node_tree.nodes.new('CompositorNodeImage')
    image_node.image = image
    image_node.frame_duration = end_frame
    scale_node = node_tree.nodes.new('CompositorNodeScale')
    scale_node.space = 'RENDER_SIZE'
    scale_node.frame_method = 'FIT'
    output_node = node_tree.nodes.new('CompositorNodeComposite')
    node_tree.links.new(image_node.outputs[0], scale_node.inputs[0])
    node_tree.links.new(scale_node.outputs[0], output_node.inputs[0])

    scene.frame_start = start_frame
    scene.frame_end = end_frame
    if args.resolution:
        x, y = args.resolution
    else:
        x, y = image.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100
    if args.fps:
        scene.render.fps = args.fps
    if args.displaydevice:
        scene.display_settings.display_device = args.displaydevice
    if args.viewtransform:
        scene.view_settings.view_transform = args.viewtransform
    if args.colordepth:
        scene.render.image_settings.color_depth = args.colordepth
    if args.output:
        scene.render.filepath = args.output

    render_movie(
        scene, metadata=args.metadata, codec=args.codec, qscale=args.qscale)

    # Debug file
    # bpy.ops.wm.save_as_mainfile(
    #     filepath='{}.blend'.format(scene.render.filepath),
    #     check_existing=True,
    #     relative_remap=False)


process()
