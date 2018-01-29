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


bl_info = {
    'name': 'Qt Integration',
    'author': 'Vincent Gires',
    'description': 'Qt Integration',
    'version': (0, 0, 1),
    'blender': (2, 7, 8),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Qt'}

import bpy
import sys
import os
import logging

from qt_integration import config

logger = logging.getLogger(__name__)

for path in config.MODULE_PATH:
    if os.path.exists(path):
        sys.path.append(path)

if config.MODULE_PATH:
    try:
        from PyQt5 import QtGui, QtWidgets, QtCore
    except:
        logger.error('Can not find the PyQt module')
else:
    logger.warning('No MODULE_PATH is configured in config.py')


class QtWindowEventLoop(bpy.types.Operator):
    bl_idname = 'screen.qt_event_loop'
    bl_label = 'PyQt Event Loop'
    _timer = None
    
    def __init__(self, widget):
        self._widget = widget
    
    def modal(self, context, event):
        wm = context.window_manager
        if self.widget.widget_close:
            logger.debug('cancel modal operator')
            wm.event_timer_remove(self._timer)
            return {'CANCELLED'}
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
            self.app = QtWidgets.QApplication(['blender'])
        self.event_loop = QtCore.QEventLoop()
        
        self.widget = self._widget()
        self.widget.context = context
        
        logger.debug(self.app)
        logger.debug(self.widget)
        
        # run modal
        wm = context.window_manager
        self._timer = wm.event_timer_add(1/120, context.window)
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_module(__name__)
    
    from qt_integration import example
    bpy.utils.register_class(example.CustomWindow)
    bpy.utils.register_class(example.QtPanelExample)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == '__main__':
    register()
