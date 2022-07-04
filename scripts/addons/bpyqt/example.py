import bpy
import sys
from PySide2 import QtWidgets, QtCore
from bpyqt import QtWindowEventLoop


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self, label_name, text):
        super().__init__()
        self.resize(720, 300)
        self.setWindowTitle('Qt Window')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.label = QtWidgets.QLabel(label_name)
        self.label2 = QtWidgets.QLabel(text)
        self.label3 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        self.setLayout(layout)
        self.show()

    def enterEvent(self, event):
        self.label3.setText(bpy.context.object.name)


class CustomWindowOperator(QtWindowEventLoop):
    bl_idname = 'screen.custom_window'
    bl_label = 'Custom window'

    def __init__(self):
        super().__init__(ExampleWidget, 'LABEL_NAME', text='a text')


class QtPanelExample(bpy.types.Panel):
    bl_label = 'Qt'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator('screen.custom_window')


if __name__ == '__main__':
    bpy.utils.register_class(CustomWindowOperator)
    bpy.ops.screen.custom_window()
