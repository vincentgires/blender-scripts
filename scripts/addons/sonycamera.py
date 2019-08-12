import bpy
import os
import xml.etree.ElementTree as ET

bl_info = {
    'name': 'Sony Camera',
    'author': 'Vincent Girès',
    'description': '',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'location': 'Property panel',
    'category': 'Sequencer'}


def find_xml(strip):
    SUFFIX = 'M01'
    XML_EXTS = ['.xml', '.XML']
    filepath = bpy.path.abspath(strip.filepath).rsplit('.', 1)[0]
    for suffix in ['', SUFFIX]:  # first look for filename without suffix
        for ext in XML_EXTS:
            xml_path = filepath + suffix + ext
            if os.path.exists(xml_path):
                return xml_path


def get_info_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    info = {}
    model_attrib = root[6].attrib
    info[model_attrib['manufacturer']] = model_attrib['modelName']
    colorspace = root[8][0]
    for c in colorspace:
        info[c.attrib['name']] = c.attrib['value']
    return info


class SequencerPropertiesPanel(bpy.types.Panel):
    bl_idname = 'SONYCAMERA_PT_SequencerPropertiesPanel'
    bl_label = 'Sony'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Strip'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            return scene.sequence_editor.active_strip.type == 'MOVIE'

    def draw(self, context):
        scene = context.scene
        strip = scene.sequence_editor.active_strip
        layout = self.layout
        xml_path = find_xml(strip)
        if not xml_path:
            return
        xml_info = get_info_from_xml(xml_path)
        for k, v in xml_info.items():
            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text=k)
            row.label(text=v)


classes = [
    SequencerPropertiesPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
