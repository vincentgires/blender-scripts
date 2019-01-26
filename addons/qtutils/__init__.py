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
from qtutils.utils import QtWindowEventLoop

bl_info = {
    'name': 'qtutils',
    'author': 'Vincent Girès',
    'description': 'Qt Integration',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'category': 'Qt'}


def register():
    bpy.utils.register_class(QtWindowEventLoop)
    from qtutils import example
    bpy.utils.register_class(example.CustomWindowOperator)
    bpy.utils.register_class(example.QtPanelExample)


def unregister():
    bpy.utils.unregister_class(QtWindowEventLoop)
    bpy.utils.unregister_class(example.CustomWindowOperator)
    bpy.utils.unregister_class(example.QtPanelExample)
