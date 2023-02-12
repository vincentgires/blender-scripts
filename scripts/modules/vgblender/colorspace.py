def set_input_transform(datablock, value):
    colorspace_settings = getattr(datablock, 'colorspace_settings', None)
    if colorspace_settings is not None:
        colorspace_settings.name = value
