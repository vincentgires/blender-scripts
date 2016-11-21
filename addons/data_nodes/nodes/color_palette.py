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
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.functions import send_value


class template_ColorPalette_collection_UL(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        layout.prop(item, "name", text="", emboss=False)
        
        row = layout.row(align=True)
        for color_item in item.colorCollection:
            row.prop(color_item, "color", text="")


class ColorPalette(Node):
    
    '''Color Palette node'''
    bl_idname = 'ColorPaletteNodeType'
    bl_label = 'Color Palette'
    
    
    # === Callbacks ===
    
    def update_props(self, context):
        self.update()
    
    # === Custom Properties ===
    settings = bpy.props.BoolProperty(name = "Settings", default = True)
    palette_id = bpy.props.IntProperty(name = "Palette ID", default = 0, update = update_props)
    
    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color")
        self.outputs.new('NodeSocketColor', "Color")
        self.outputs.new('NodeSocketColor', "Color")
        for palette in bpy.context.scene.ColorPalette_collection:
            for color in palette.colorCollection:
                if ( len(self.outputs) <= len(palette.colorCollection) ):
                    self.outputs.new('NodeSocketColor', "Color")
    
    
    
    def update(self):
        
        if bpy.context.scene.ColorPalette_collection:
            palette = bpy.context.scene.ColorPalette_collection[self.palette_id]
            palette_color = palette.colorCollection
            
            # send data value to connected nodes
            for index, output in enumerate(self.outputs):
                for link in output.links:
                    if link.is_valid:
                        if link.to_node.type == 'REROUTE':
                            reroute = link.to_node
                            send_value(self.outputs, palette_color[index].color)
                        
                        if output.type == link.to_socket.type:
                            # assign value to connected socket
                            link.to_socket.default_value = palette_color[index].color
                            # update connected target nodes
                            link.to_node.update()
        
        
    
                 
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        
        
        if self.settings:
            row = layout.row()
            row.prop(self, "settings", text="", icon="TRIA_DOWN", emboss=False)
            
            row = layout.row()
            row.template_list("template_ColorPalette_collection_UL", "", context.scene, "ColorPalette_collection", self, "palette_id")
            
            col = row.column(align=True)
            col.operator("color_palette_add_item.btn", icon='ZOOMIN', text="")
            col.operator("color_palette_remove_item.btn", icon='ZOOMOUT', text="")
        
        else:
            row = layout.row()
            row.prop(self, "settings", text="", icon="TRIA_RIGHT", emboss=False)
        
        
        if context.scene.ColorPalette_collection:
            palette = context.scene.ColorPalette_collection[self.palette_id]
            
            row = layout.row(align=True)
            row.operator("color_palette_add_color.btn", text="", icon="ZOOMIN")
            for color_item in palette.colorCollection:
                row.prop(color_item, "color", text="")
            row.operator("color_palette_remove_color.btn", text="", icon="ZOOMOUT")
            row.operator("color_palette_clear_color.btn", text="", icon="X")
    
    
    # Detail buttons in the sidebar.
    """def draw_buttons_ext(self, context, layout):
        pass"""

    
    def draw_label(self):
        return "Color Palette"




### OPERATORS ###
#################


class custom_nodes_add_palette_item(bpy.types.Operator):
    bl_idname = "color_palette_add_item.btn"
    bl_label = "Palette add item"
    
    @classmethod
    def poll(cls, context):
        try:
            tree_type = context.space_data.tree_type
            node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
            return tree_type in node_tree
        
        except:
            return False
    
    def execute(self, context):
        node = context.node
        
        palette_collection = context.scene.ColorPalette_collection
        p = palette_collection.add()
        p.name = str(len(palette_collection))
        p.colorCollection.add()
        p.colorCollection.add()
        p.colorCollection.add()
        node.palette_id = len(palette_collection)-1
        return{'FINISHED'}
    
class custom_nodes_remove_palette_item(bpy.types.Operator):
    bl_idname = "color_palette_remove_item.btn"
    bl_label = "Palette remove item"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        node = context.node
        
        palette_collection = context.scene.ColorPalette_collection
        palette_collection.remove(node.palette_id)
        if node.palette_id > 0:
            node.palette_id -= 1
        
        return{'FINISHED'}


class custom_nodes_add_palette_color(bpy.types.Operator):
    bl_idname = "color_palette_add_color.btn"
    bl_label = "Palette add color"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        node = context.node
        
        palette = context.scene.ColorPalette_collection[node.palette_id]
        palette.colorCollection.add()
        
        # SOCKETS
        if ( len(node.outputs) <= len(palette.colorCollection)-1 ):
            node.outputs.new('NodeSocketColor', "Color")
        
        return{'FINISHED'}


class custom_nodes_remove_palette_color(bpy.types.Operator):
    bl_idname = "color_palette_remove_color.btn"
    bl_label = "Palette remove color"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        node = context.node
        
        palette = context.scene.ColorPalette_collection[node.palette_id]
        palette.colorCollection.remove( len(palette.colorCollection)-1 )
        
        
        return{'FINISHED'}


class custom_nodes_clear_palette_color(bpy.types.Operator):
    bl_idname = "color_palette_clear_color.btn"
    bl_label = "Palette clear color"
    
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree
    
    def execute(self, context):
        node = context.node
        
        palette = context.scene.ColorPalette_collection[node.palette_id]
        palette.colorCollection.clear()
            
        return{'FINISHED'}



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    
    
print ("---")
