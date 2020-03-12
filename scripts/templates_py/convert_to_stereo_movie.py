import bpy

from vgblender.path import normpath
from vgblender.argconfig import get_args
from vgblender.scene import set_scene_from_args
from vgblender.render.render import render_movie

args = get_args()

data = bpy.data
context = bpy.context
scene = context.scene


def process():
    # Remove all objects
    for obj in data.objects:
        data.objects.remove(obj)

    # Scene setup
    scene.use_nodes = True
    scene.render.use_multiview = True
    scene.render.views_format = 'STEREO_3D'
    scene.render.image_settings.views_format = 'STEREO_3D'
    scene.render.image_settings.stereo_3d_format.display_mode = 'ANAGLYPH'
    scene.render.image_settings.stereo_3d_format.anaglyph_type = 'RED_CYAN'

    # Clear default nodes
    node_tree = scene.node_tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    start_frame = args.startframe or 1
    end_frame = args.endframe or start_frame

    # Create nodes
    switchview_node = node_tree.nodes.new('CompositorNodeSwitchView')
    images = []
    view_inputs = (args.inputs[0], args.inputs[1])
    for index, inputpath in enumerate(view_inputs):
        image = data.images.load(normpath(inputpath))
        image.source = 'SEQUENCE'
        if args.colorspace:
            image.colorspace_settings.name = args.colorspace
        images.append(image)
        node = node_tree.nodes.new('CompositorNodeImage')
        node.image = image
        node.frame_duration = end_frame
        node_tree.links.new(node.outputs[0], switchview_node.inputs[index])
    bw_node = node_tree.nodes.new('CompositorNodeRGBToBW')
    scale_node = node_tree.nodes.new('CompositorNodeScale')
    scale_node.space = 'RENDER_SIZE'
    scale_node.frame_method = 'FIT'
    output_node = node_tree.nodes.new('CompositorNodeComposite')
    node_tree.links.new(switchview_node.outputs[0], bw_node.inputs[0])
    node_tree.links.new(bw_node.outputs[0], scale_node.inputs[0])
    node_tree.links.new(scale_node.outputs[0], output_node.inputs[0])

    scene.frame_start = start_frame
    scene.frame_end = end_frame
    x, y = images[0].size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100

    set_scene_from_args(scene)
    render_movie(
        scene, metadatas=args.metadatas, codec=args.codec, qscale=args.qscale)

    # Debug file
    # bpy.ops.wm.save_as_mainfile(
    #     filepath='{}.blend'.format(scene.render.filepath),
    #     check_existing=True,
    #     relative_remap=False)


process()
