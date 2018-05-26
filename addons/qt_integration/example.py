import bpy
import sys
from PyQt5 import QtWidgets, QtCore
from qt_integration import QtWindowEventLoop


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self, label_name):
        super().__init__()
        self.context = None
        self.resize(720, 300)
        self.setWindowTitle("QT Window")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        label = QtWidgets.QLabel(label_name)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        self.setLayout(layout)
        self.show()


class CustomWindowOperator(QtWindowEventLoop):
    bl_idname = 'screen.custom_window'
    bl_label = 'Custom window'

    def __init__(self):
        super().__init__(ExampleWidget, 'LABEL_NAME')


class QtPanelExample(bpy.types.Panel):
    bl_label = 'Qt'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Custom'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.custom_window')


if __name__ == '__main__':
    bpy.utils.register_class(CustomWindowOperator)
    bpy.ops.screen.custom_window()
