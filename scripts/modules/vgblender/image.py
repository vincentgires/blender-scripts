from bpy import data


def get_image_resolution(image):
    if image.type == 'MULTILAYER':
        # HACK to get the resolution of a multilayer EXR through movieclip
        movieclip = data.movieclips.load(image.filepath)
        x, y = movieclip.size
        data.movieclips.remove(movieclip)
    else:
        x, y = image.size
    return x, y
