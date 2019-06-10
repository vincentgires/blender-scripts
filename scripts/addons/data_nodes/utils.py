import bpy
import math
import mathutils
from bpy.app.handlers import persistent


custom_nodes_type = [
    'ColorCombineNodeType',
    'ColorPaletteNodeType',
    'ColorSplitNodeType',
    'ColorNodeType',
    'DataInputNodeType',
    'DataOutputNodeType',
    'DebugNodeType',
    'ExpressionNodeType',
    'DistanceNodeType',
    'FloatNumberNodeType',
    'FloatSwitchNodeType',
    'FloatToIntNodeType',
    'FloatToStringNodeType',
    'IntToFloatNodeType',
    'NoteNodeType',
    'ObjectPropertiesNodeType',
    'RenderNodeType',
    'RenderLayersNodeType',
    'RoundFloatNodeType',
    'TimeNodeType',
    'VectorSplitNodeType',
    'VectorNodeType']


def update_nodes(scene):
    # Update compositing tree
    if scene.node_tree:
        for node in scene.node_tree.nodes:
            if node.bl_idname in custom_nodes_type:
                node.update()
    # Update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    node.update()
    # Update custom node trees
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in custom_nodes_type:
                node.update()


def update_compositing_tree(scene, object, custom_nodes_type):
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in custom_nodes_type:
                if node.bl_idname == 'ObjectPropertiesNodeType':
                    if node.data_item == object.name:
                        # Update node property from scene object
                        node.update_props_from_object()
                node.update()


def update_material_tree(scene, object, custom_nodes_type):
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    if node.bl_idname == 'ObjectPropertiesNodeType':
                        # Update node property from scene object
                        node.update_props_from_object()
                    node.update()


def update_world_tree(scene, object, custom_nodes_type):
    for world in bpy.data.worlds:
        if world.use_nodes:
            for node in scene.world.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    if node.bl_idname == 'ObjectPropertiesNodeType':
                        if node.data_item == object.name:
                            # Update node property from scene object
                            node.update_props_from_object()
                    node.update()


def update_custom_tree(scene, object, custom_nodes_type):
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in custom_nodes_type:
                if node.bl_idname == 'ObjectPropertiesNodeType':
                    # Update node property from scene object
                    node.update_props_from_object()
                node.update()


@persistent
def frame_change(scene):
    update_nodes(scene)


@persistent
def scene_update(scene):
    check_objects = bpy.data.objects.is_updated
    check_scene = bpy.context.scene.is_updated
    if check_objects:
        for object in bpy.data.objects:
            if object.is_updated:
                update_compositing_tree(scene, object, custom_nodes_type)
                update_material_tree(scene, object, custom_nodes_type)
                update_world_tree(scene, object, custom_nodes_type)
                update_custom_tree(scene, object, custom_nodes_type)
    if check_scene:
        for object in bpy.data.objects:
            update_compositing_tree(scene, object, custom_nodes_type)
            update_material_tree(scene, object, custom_nodes_type)
            update_world_tree(scene, object, custom_nodes_type)
            update_custom_tree(scene, object, custom_nodes_type)

    # # Node tree update
    # # Update compositing tree
    # tree =  scene.node_tree
    # if scene.use_nodes:
    #     if tree.is_updated:
    #         update_nodes(scene)
    #
    # # Update nodes in materials
    # for material in bpy.data.materials:
    #     if material.use_nodes:
    #         if material.is_updated:
    #             update_nodes(scene)
    #
    # # Update custom node trees
    # for tree in bpy.data.node_groups:
    #     if tree.is_updated:
    #         update_nodes(scene)


@persistent
def render_pre_update(scene):
    RenderNodeType = ['RenderNodeType']
    # Update compositing tree
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 1
                node.update()
    # Update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.bl_idname in RenderNodeType:
                    node.on_render = 1
                    node.update()
    # Update custom node trees
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 1
                node.update()


@persistent
def render_post_update(scene):
    RenderNodeType = ['RenderNodeType']
    # Update compositing tree
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 0
                node.update()
    # Update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.bl_idname in RenderNodeType:
                    node.on_render = 0
                    node.update()
    # Update custom node trees
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in RenderNodeType:
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
                link.to_node.update()
            else:
                ok = None
                if output.type == 'VALUE' and link.to_socket.type == 'BOOLEAN':
                    ok = True
                elif output.type == 'VALUE' and link.to_socket.type == 'INT':
                    ok = True
                elif output.type == 'BOOLEAN' and link.to_socket.type == 'VALUE':
                    ok = True
                elif output.type == 'BOOLEAN' and link.to_socket.type == 'INT':
                    ok = True
                elif output.type == 'INT' and link.to_socket.type == 'VALUE':
                    ok = True
                elif output.type == 'INT' and link.to_socket.type == 'BOOLEAN':
                    ok = True
                if ok:
                    link.to_socket.default_value = value
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
            link.to_node.update()
