import bpy
from vgblender.ui.color_management import (
    SequencerColorManagementDisplay, SequencerColorManagementCurves,
    ImageEditorColorManagementDisplay, ImageEditorColorManagementCurves)


classes = [
    SequencerColorManagementDisplay,
    SequencerColorManagementCurves,
    ImageEditorColorManagementDisplay,
    ImageEditorColorManagementCurves,]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
