import bpy
import sys
from PyQt5 import QtWidgets, QtCore
from qt_integration import QtWindowEventLoop


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.context = None
        self.configure()

    def configure(self):
        self.resize(720, 300)
        self.setWindowTitle("QT Window")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        label = QtWidgets.QLabel('Label')
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        self.setLayout(layout)

        self.show()

    def closeEvent(self, event):
        self.deleteLater()


class CustomWindowOperator(QtWindowEventLoop):
    bl_idname = 'screen.custom_window'
    bl_label = 'Custom window'

    def __init__(self):
        super().__init__(widget=ExampleWidget)


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
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleWidget()
    sys.exit(app.exec())
