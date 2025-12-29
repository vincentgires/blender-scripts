import os
import argparse
import bpy
from vgblender.argconfig import get_args
from vgblender.render import set_render_settings


def convert_image(
        input_path: str,
        output_path: str,
        input_colorspace: str | None = None,
        look: str | None = None,
        display_view: tuple[str, str] | None = None,
        resize: tuple[int, int] | None = None,
        compression: str | int | None = None,
        file_format: str | None = None,
        color_mode: str | None = None,
        color_depth: int | None = None,
        quality: int | None = None,
        codec: str | None = None,
        additional_image_settings: dict | None = None) -> None:
    data = bpy.data
    image = data.images.load(input_path)
    if input_colorspace is not None:
        image.colorspace_settings.name = input_colorspace
    if resize is not None:
        image.scale(*resize)
    if display_view is None:
        if file_format is not None:
            image.file_format = file_format.upper()
        image.save(filepath=output_path)
    else:
        scene = bpy.context.scene
        set_render_settings(
            scene=scene,
            look=look,
            display_view=display_view,
            file_format=file_format,
            color_mode=color_mode,
            color_depth=color_depth,
            compression=compression,
            quality=quality,
            codec=codec,
            additional_image_settings=additional_image_settings)
        image.save_render(filepath=output_path)
    print(f'bpy: {output_path}')
    data.images.remove(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-path', required=True, metavar='path')
    parser.add_argument(
        '-o', '--output-path', required=True, metavar='path')
    parser.add_argument(
        '--input-colorspace', required=False, metavar='name')
    parser.add_argument(
        '--look', required=False, metavar='name')
    parser.add_argument(
        '--display-view', required=False, nargs=2, metavar=('display', 'view'))
    parser.add_argument(
        '--compression', required=False, type=int, metavar='number')
    parser.add_argument(
        '--color-mode', required=False, metavar='name')
    parser.add_argument(
        '--color-depth', required=False, type=int, metavar='number')
    parser.add_argument(
        '--file-format', required=False, metavar='name')
    parser.add_argument(
        '--quality', required=False, type=int, metavar='number')
    parser.add_argument(
        '--codec', required=False, metavar='name')
    parser.add_argument(
        '--resize', required=False, type=int, nargs=2, metavar=('x', 'y'))
    
    args = get_args(parser)
    convert_image(
        input_path=args.input_path,
        output_path=args.output_path,
        input_colorspace=args.input_colorspace,
        look=args.look,
        display_view=args.display_view,
        resize=args.resize,
        compression=args.compression,
        file_format=args.file_format,
        color_mode=args.color_mode,
        color_depth=args.color_depth,
        quality=args.quality,
        codec=args.codec)

