import bpy
from bpy.app.handlers import persistent
from .nodes import NODES_TYPES


def get_all_data_nodes():
    nodes = []
    data = bpy.data
    # Compositing tree
    for scene in data.scenes:
        if scene.node_tree is None:
            continue
        for node in scene.node_tree.nodes:
            nodes.append(node)
    # Material trees
    for material in data.materials:
        if material.node_tree is None:
            continue
        for node in material.node_tree.nodes:
            nodes.append(node)
    # Node groups trees
    for tree in data.node_groups:
        for node in tree.nodes:
            nodes.append(node)
    nodes = [n for n in nodes if n.bl_idname in NODES_TYPES]
    return nodes


def is_updatable(node):
    if hasattr(node, 'update') and callable(getattr(node, 'update')):
        return True
    return False


def update_nodes():
    nodes = get_all_data_nodes()
    for node in nodes:
        if is_updatable(node):
            node.update()


@persistent
def frame_change(scene):
    update_nodes()


@persistent
def scene_update(scene):
    update_nodes()


@persistent
def render_pre_update(scene):
    node_types = ['RenderNodeType']
    nodes = get_all_data_nodes()
    for node in nodes:
        if node.bl_idname in node_types:
            node.on_render = 1
            node.update()


@persistent
def render_post_update(scene):
    node_types = ['RenderNodeType']
    nodes = get_all_data_nodes()
    for node in nodes:
        if node.bl_idname in node_types:
            node.on_render = 0
            node.update()


def send_value(outputs, value):
    for output in outputs:
        for link in output.links:
            if not link.is_valid:
                continue
            if link.to_node.type == 'REROUTE':
                reroute = link.to_node
                send_value(reroute.outputs, value)
            elif output.type == link.to_socket.type:
                # Assign value to connected socket
                link.to_socket.default_value = value
                # Update connected target nodes
                if is_updatable(link.to_node):
                    link.to_node.update()
            else:
                value_types = ('VALUE', 'BOOLEAN', 'INT')
                if (output.type in value_types
                        and link.to_socket.type in value_types):
                    link.to_socket.default_value = value
                    if is_updatable(link.to_node):
                        link.to_node.update()


def send_value_link(link, value):
    if link.is_valid:
        if link.to_node.type == 'REROUTE':
            reroute = link.to_node
            reroute_links = reroute.outputs[0].links
            for reroute_link in reroute_links:
                send_value(reroute_link, value)
        else:
            # Assign value to connected socket
            link.to_socket.default_value = value
            # Update connected target nodes
            if is_updatable(link.to_node):
                link.to_node.update()
