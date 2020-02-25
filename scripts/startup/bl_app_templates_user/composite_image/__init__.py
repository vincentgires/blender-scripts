import os
import sys
import bpy
from bpy.app.handlers import persistent
from vgblender.path import normpath

filepath = normpath(sys.argv[-1])


def load_file_as_image():
    if not os.path.exists(filepath):
        return
    context = bpy.context
    scene = context.scene
    image = bpy.data.images.load(filepath)
    image.use_view_as_render = True

    x, y = image.size
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.resolution_percentage = 100

    scene.use_nodes = True
    node_tree = scene.node_tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)
    image_node = node_tree.nodes.new('CompositorNodeImage')
    viewer_node = node_tree.nodes.new('CompositorNodeViewer')
    viewer_node.location.x += 300
    image_node.image = image
    node_tree.links.new(image_node.outputs[0], viewer_node.inputs[0])

    screen = context.screen
    for area in screen.areas:
        if area.type == 'IMAGE_EDITOR':
            render_image = bpy.data.images['Viewer Node']
            space = area.spaces.active
            space.image = render_image


@persistent
def load_handler(dummy):
    load_file_as_image()


def register():
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
