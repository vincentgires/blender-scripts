# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import sys
import os
import logging

try:
    from PyQt5 import QtWidgets, QtCore
except ImportError:
    raise ImportError('Cannot find the PyQt module')

bl_info = {
    'name': 'Qt Integration',
    'author': 'Vincent Gires',
    'description': 'Qt Integration',
    'version': (0, 0, 1),
    'blender': (2, 7, 9),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Qt'}

logger = logging.getLogger(__name__)


class QtWindowEventLoop(bpy.types.Operator):
    '''This class is a modal operator that behave like QEventLoop and allows
    PyQt to run inside Blender.'''

    bl_idname = 'screen.qt_event_loop'
    bl_label = 'PyQt Event Loop'

    def __init__(self, widget, *args, **kwargs):
        self._widget = widget
        self._args = args
        self._kwargs = kwargs

    def close(self):
        self._close = True

    def modal(self, context, event):
        wm = context.window_manager

        if not self.widget.isVisible():
            logger.debug('cancel modal operator')
            wm.event_timer_remove(self._timer)
            return {'FINISHED'}
        else:
            logger.debug('process the events for Qt window')
            self.event_loop.processEvents()
            self.app.sendPostedEvents(None, 0)

        return {'PASS_THROUGH'}

    def execute(self, context):
        logger.debug('execute operator')

        self.app = QtWidgets.QApplication.instance()
        # instance() gives the possibility to have multiple windows
        # and close it one by one

        if not self.app:
            # create the first instance
            self.app = QtWidgets.QApplication(['blender'])

        if 'stylesheet' in self._kwargs:
            stylesheet = self._kwargs['stylesheet']
            self.set_stylesheet(self.app, stylesheet)

        self.event_loop = QtCore.QEventLoop()
        self.widget = self._widget(*self._args)
        self.widget.destroyed.connect(self.close)

        logger.debug(self.app)
        logger.debug(self.widget)

        # run modal
        wm = context.window_manager
        self._timer = wm.event_timer_add(1/120, context.window)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def set_stylesheet(self, app, filepath):
        file_qss = QtCore.QFile(filepath)
        if file_qss.exists():
            file_qss.open(QtCore.QFile.ReadOnly)
            stylesheet = QtCore.QTextStream(file_qss).readAll()
            app.setStyleSheet(stylesheet)
            file_qss.close()


def register():
    bpy.utils.register_module(__name__)

    from qt_integration import example
    bpy.utils.register_class(example.CustomWindowOperator)
    bpy.utils.register_class(example.QtPanelExample)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()
