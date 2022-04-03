import bpy
from bpy.types import Panel, Operator
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


def find_xml(filepath):
    SUFFIX = 'M01'
    XML_EXTS = ['.xml', '.XML']
    filepath_base = bpy.path.abspath(filepath).rsplit('.', 1)[0]
    for suffix in ['', SUFFIX]:  # first look for filename without suffix
        for ext in XML_EXTS:
            xml_path = filepath_base + suffix + ext
            if os.path.exists(xml_path):
                return xml_path


def get_info_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    info = {}
    model_attrib = root[6].attrib
    info[model_attrib['manufacturer']] = model_attrib['modelName']
    videoformat = root[4]
    info['fps'] = videoformat[1].attrib['captureFps']
    info['resolution'] = '{}x{}'.format(
        videoformat[2].attrib['pixel'],
        videoformat[2].attrib['numOfVerticalLine'])
    colorspace = root[8][0]
    for c in colorspace:
        info[c.attrib['name']] = c.attrib['value']
    return info


def draw_info(layout, xml_info):
    for k, v in xml_info.items():
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text=k)
        row.label(text=v)


def set_colorspace(strip, xml_path):
    """Match camera colorspace to ACES OCIO config"""
    GAMMA = {
        'rec2100-hlg': 'hlg',
        's-log2': 'slog2',
        's-log3': 'slog3',
        's-log3-cine': 'slog3'}
    PRIMARIES = {
        'rec709': 'rec709',
        'rec2020': 'rec2020',
        's-gamut': 'sgamut',
        's-gamut3': 'sgamut3',
        's-gamut3-cine': 'sgamutcine'}
    tree = ET.parse(xml_path)
    root = tree.getroot()
    colorspace = {}
    for c in root[8][0]:
        if c.attrib['name'] == 'CaptureGammaEquation':
            colorspace['gamma'] = c.attrib['value']
        if c.attrib['name'] == 'CaptureColorPrimaries':
            colorspace['primaries'] = c.attrib['value']
    ocio_colorspace = '{}_{}'.format(
        GAMMA[colorspace['gamma']], PRIMARIES[colorspace['primaries']])
    strip.colorspace_settings.name = ocio_colorspace


class SetColorspace(Operator):
    bl_idname = 'scene.sonycamera_set_colorspace'
    bl_label = 'Set colorspace'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor

    def execute(self, context):
        scene = context.scene
        sequences = scene.sequence_editor.sequences_all
        for strip in sequences:
            if strip.select:
                xml_path = find_xml(strip.filepath)
                if not xml_path:
                    continue
                set_colorspace(strip, xml_path)
        return {'FINISHED'}


class SequencerPropertiesPanel(Panel):
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
        xml_path = find_xml(strip.filepath)
        if not xml_path:
            return
        draw_info(layout, get_info_from_xml(xml_path))
        layout.operator('scene.sonycamera_set_colorspace')


class FilebrowserPropertiesPanel(Panel):
    bl_idname = 'SONYCAMERA_PT_FilebrowserPropertiesPanel'
    bl_label = 'Sony'
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        space = context.space_data
        directory = space.params.directory
        if isinstance(directory, bytes):  # directory is a byte since 2.81
            directory = directory.decode()
        filepath = os.path.join(directory, space.params.filename)
        xml_path = find_xml(filepath)
        if not xml_path:
            return
        draw_info(layout, get_info_from_xml(xml_path))


classes = [
    SetColorspace,
    SequencerPropertiesPanel,
    FilebrowserPropertiesPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
