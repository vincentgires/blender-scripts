import bpy
import logging
import subprocess
from vgblender.sequencer import get_current_strips
from vgblender.glutils import FONT_SANS
from vgblender.area import redraw_area

IMAGEMAGICK_BIN = 'magick'


def add_text(strip, text=None, color=None, position=None):
    item = strip.texts.add()
    if text:
        item.name = text
    if color:
        item.color = color
    if position:
        item.position = position
    strip.active_text_index = len(strip.texts) - 1  # Adapt index
    redraw_area(bpy.context)
    return item


def remove_item_from_collection(collection, properties, index_name):
    if index_name in properties:
        index = properties[index_name]
        # Adapt index of note collection's items
        if (len(collection) - 1) >= index:
            if properties[index_name] > 0:
                properties[index_name] -= 1
        # Remove item
        collection.remove(index)


def export_texts(scene, output_path, input_path=None):
    """Create note with ImageMagick"""
    width = scene.render.resolution_x
    height = scene.render.resolution_y
    text_args = []
    for strips in get_current_strips(scene):
        for text in strips.texts:
            if not text.display:
                continue
            r = str(text.color[0] * 255)
            g = str(text.color[1] * 255)
            b = str(text.color[2] * 255)
            x = str(text.position[0] * width)
            y = str((1 - text.position[1]) * height)
            text_args += [
                '-font', FONT_SANS, '-pointsize',
                str(text.size), '-fill',
                'rgb(' + r + ',' + g + ',' + b + ')']
            text_args += [
                '-draw',
                'text ' + x + ',' + y + ' "' + text.name + '"']
    command = [IMAGEMAGICK_BIN]
    if input_path is not None:
        command.append(input_path)
    else:
        command.extend(['-size', '{}_{}'.format(width, height)])
        command.extend(['-background', 'transparent'])
    command.extend(text_args)
    command.append(output_path)
    print(command)
    subprocess.call(command)
    logging.info('ImageMagick: frame {0} exported in {1}'.format(
        scene.frame_current, output_path))
