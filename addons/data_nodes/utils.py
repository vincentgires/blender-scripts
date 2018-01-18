# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import math, mathutils
from bpy.app.handlers import persistent


custom_nodes_type = ["ColorCombineNodeType",
                    "ColorPaletteNodeType",
                    "ColorSplitNodeType",
                    "ColorNodeType",
                    "DataInputNodeType",
                    "DataOutputNodeType",
                    "DebugNodeType",
                    "ExpressionNodeType",
                    "DistanceNodeType",
                    "FloatSwitchNodeType",
                    "FloatToIntNodeType",
                    "FloatToStringNodeType",
                    "FloatNodeType",
                    "IntToFloatNodeType",
                    "NoteNodeType",
                    "ObjectPropertiesNodeType",
                    "RenderNodeType",
                    "RenderLayersNodeType",
                    "RoundNodeType",
                    "TimeNodeType",
                    "VectorSplitNodeType",
                    "VectorNodeType"]

def update_nodes(scene):
    #print ("update_nodes")
    
    # update compositing tree
    if scene.node_tree:
        for node in scene.node_tree.nodes:
            if node.bl_idname in custom_nodes_type:
                node.update()
    
    # update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree != None:
            for node in material.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    node.update()

    # update custom node trees
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in custom_nodes_type:
                node.update()



def update_compositing_tree(scene, object, custom_nodes_type):
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in custom_nodes_type:
                if node.bl_idname == "ObjectPropertiesNodeType":
                    if node.data_item == object.name:
                        # update node property from scene object
                        node.update_props_from_object()
                node.update()

def update_material_tree(scene, object, custom_nodes_type):
    for material in bpy.data.materials:
        if material.node_tree != None:
            for node in material.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    if node.bl_idname == "ObjectPropertiesNodeType":
                        # update node property from scene object
                        node.update_props_from_object()
                    node.update()

def update_world_tree(scene, object, custom_nodes_type):
    for world in bpy.data.worlds:
        if world.use_nodes:
            for node in scene.world.node_tree.nodes:
                if node.bl_idname in custom_nodes_type:
                    if node.bl_idname == "ObjectPropertiesNodeType":
                        if node.data_item == object.name:
                            # update node property from scene object
                            node.update_props_from_object()
                    node.update()

def update_custom_tree(scene, object, custom_nodes_type):
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in custom_nodes_type:
                if node.bl_idname == "ObjectPropertiesNodeType":
                    # update node property from scene object
                    node.update_props_from_object()
                node.update()


@persistent
def frame_change(scene):
    #print ("frame_change")
    update_nodes(scene)

@persistent
def scene_update(scene):
    #print ("scene_update")
    check_objects = bpy.data.objects.is_updated
    check_scene = bpy.context.scene.is_updated
    
    if check_objects:
        #print ("check_objects")
        for object in bpy.data.objects:
            if object.is_updated:
                #print ("check_object", object)
                update_compositing_tree(scene, object, custom_nodes_type)
                update_material_tree(scene, object, custom_nodes_type)
                update_world_tree(scene, object, custom_nodes_type)
                update_custom_tree(scene, object, custom_nodes_type)
    
    if check_scene:
        #print ("check_scene")
        for object in bpy.data.objects:
            update_compositing_tree(scene, object, custom_nodes_type)
            update_material_tree(scene, object, custom_nodes_type)
            update_world_tree(scene, object, custom_nodes_type)
            update_custom_tree(scene, object, custom_nodes_type)
            
            
    
    ### node tree update ###
    '''
    # update compositing tree
    tree =  scene.node_tree
    if scene.use_nodes:
        if tree.is_updated:
            update_nodes(scene)
            
    # update nodes in materials
    for material in bpy.data.materials:
        if material.use_nodes:
            if material.is_updated:
                update_nodes(scene)
    
    # update custom node trees
    for tree in bpy.data.node_groups:
        if tree.is_updated:
            update_nodes(scene)
    '''
    
    
    
    
    
    
@persistent
def render_pre_update(scene):
    
    RenderNodeType = ["RenderNodeType"]
    # update compositing tree
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 1
                node.update()
    
    # update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree != None:
            for node in material.node_tree.nodes:
                if node.bl_idname in RenderNodeType:
                    node.on_render = 1
                    node.update()
    
    # update custom node trees
    for tree in bpy.data.node_groups:
        for node in tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 1
                node.update()
    
@persistent
def render_post_update(scene):
    
    RenderNodeType = ["RenderNodeType"]
    # update compositing tree
    if scene.use_nodes:
        for node in scene.node_tree.nodes:
            if node.bl_idname in RenderNodeType:
                node.on_render = 0
                node.update()
    
    # update nodes in materials
    for material in bpy.data.materials:
        if material.node_tree != None:
            for node in material.node_tree.nodes:
                if node.bl_idname in RenderNodeType:
                    node.on_render = 0
                    node.update()
    
    # update custom node trees
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
            
            # REROUTE
            if link.to_node.type == 'REROUTE':
                reroute = link.to_node
                send_value(reroute.outputs, value)
                
                
            elif output.type == link.to_socket.type:
                # assign value to connected socket
                link.to_socket.default_value = value
                # update connected target nodes
                link.to_node.update()
            
            # convert types
            #elif output.type == "RGBA" and link.to_socket.type == "VALUE":
                #link.to_socket.default_value = value[0]
                #link.to_node.update()
            #elif output.type == "VECTOR" and link.to_socket.type == "VALUE":
                #link.to_socket.default_value = value[0]
                #link.to_node.update()
            #elif output.type == "VALUE" and link.to_socket.type == "RGBA":
                #link.to_socket.default_value[0] = value
                #link.to_socket.default_value[1] = value
                #link.to_socket.default_value[2] = value
                #link.to_socket.default_value[3] = value
                #link.to_node.update()
            #elif output.type == "VALUE" and link.to_socket.type == "VECTOR":
                #link.to_socket.default_value[0] = value
                #link.to_socket.default_value[1] = value
                #link.to_socket.default_value[2] = value
                #link.to_node.update()
            
            else:
                ok = None
                
                if output.type == "VALUE" and link.to_socket.type == "BOOLEAN":
                    ok = True
                elif output.type == "VALUE" and link.to_socket.type == "INT":
                    ok = True
                elif output.type == "BOOLEAN" and link.to_socket.type == "VALUE":
                    ok = True
                elif output.type == "BOOLEAN" and link.to_socket.type == "INT":
                    ok = True
                elif output.type == "INT" and link.to_socket.type == "VALUE":
                    ok = True
                elif output.type == "INT" and link.to_socket.type == "BOOLEAN":
                    ok = True
                
                if ok:
                    link.to_socket.default_value = value
                    link.to_node.update()
                
                
                
def send_value_link(link, value):
    if link.is_valid:
        # REROUTE
        if link.to_node.type == 'REROUTE':
            reroute = link.to_node
            reroute_links = reroute.outputs[0].links
            for reroute_link in reroute_links:
                send_value(reroute_link, value)

        #elif output.type == link.to_socket.type:
        else:
            # assign value to connected socket
            link.to_socket.default_value = value
            # update connected target nodes
            link.to_node.update()

