import bpy
from PyQt5 import QtGui, QtWidgets, QtCore
from qt_integration import QtWindowEventLoop


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.widget_close = None
        self.context = None
        self.initUI()
        
    def initUI(self):
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
        self.widget_close = True
        self.deleteLater()


class CustomWindow(QtWindowEventLoop):
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
    window = ExempleWidget()
    sys.exit(app.exec())
