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


# TODO

# stereo viewer en setup
# marche pas s'il y a du son dans la video pcq il y a une piste en + > changer le num de sequence_all[0] par le nom du strip loadé
# seq: prendre que les images, pas les autres fichiers qui pourraient poser probleme

bl_info = {
	"name": "Check sequence",
	"author": "Vincent Gires",
	"description": "---",
	"version": (0, 1),
	"blender": (2, 7, 0),
	"location": "Sequencer > Property",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Sequencer"}

import bpy, os
'''
bpy.context.scene = bpy.context.scene
sequence_editor = bpy.context.scene.sequence_editor
'''

## CALL BACK ##
###############

def effect_fader_callback(self, context):
	bpy.context.scene.sequence_editor.sequences_all["Wipe"].effect_fader = bpy.context.scene.effect_fader

def display_side_callback(self, context):
	set_display_side()


## CUSTOM PROPERTIES ##
#######################

class check_sequence_properties(bpy.types.PropertyGroup):
	
	# LOAD
	bpy.types.Scene.load_type = bpy.props.EnumProperty(
		items = (
			('movie', 'Movie', 'Load movie'),
			('img_seq', 'Image sequence', 'Load image sequence'),
		),
		name = "Type",
		description = "Type of strip to load",
		default = 'movie',
	)
	
	bpy.types.Scene.imageSequence_path = bpy.props.StringProperty(
		name = "",
		description = "Image sequence folder path",
		default = "",
		subtype = 'DIR_PATH',
	)
	
	bpy.types.Scene.movie_filepath = bpy.props.StringProperty(
		name = "",
		description="Movie file path",
		default = "",
		subtype ='FILE_PATH',
	)
	
	bpy.types.Scene.strip_height = bpy.props.IntProperty(
		name = "Strip height",
		description="Height resolution",
		default = 0,
	)
	
	bpy.types.Scene.strip_width = bpy.props.IntProperty(
		name = "Strip width",
		description="Width resolution",
		default = 0,
	)
   
   
   # WIPE
	bpy.types.Scene.effect_fader = bpy.props.FloatProperty(
		name = "Wipe",
		description = "Float value",
		default = 0.5,
		min = 0, max = 1,
		step = 0.15, precision = 3,
		update = effect_fader_callback
	)
   
   # COMPARE SIDE
	bpy.types.Scene.display_side = bpy.props.EnumProperty(
		items = (
			('wipe', 'Wipe', 'Display as Wipe'),
			('side_h', 'Horizontal', 'Display as two sides'),
			('side_v', 'Vertical', 'Display as two sides'),
		),
		name = "Display",
		description = "Display type",
		default = 'wipe',
		update = display_side_callback
	)
	
	
	# LOAD FOR COMPARE
	
	# A
	
	bpy.types.Scene.stripA_load_type = bpy.props.EnumProperty(
		items = (
			('movie', 'Movie', 'Load movie'),
			('img_seq', 'Sequence', 'Load image sequence'),
		),
		name = "Strip A",
		description = "Type of strip to load",
		default = 'movie',
	)
	
	bpy.types.Scene.movieA_filepath = bpy.props.StringProperty(
		name = "",
		description = "Movie file path",
		default = "",
		subtype ='FILE_PATH',
	)
   
	bpy.types.Scene.imgSeqA_path = bpy.props.StringProperty(
		name = "",
		description = "Image sequence folder path",
		default = "",
		subtype ='DIR_PATH',
	)

   # B
   
	bpy.types.Scene.stripB_load_type = bpy.props.EnumProperty(
		items = (
			('movie', 'Movie', 'Load movie'),
			('img_seq', 'Sequence', 'Load image sequence'),
		),
		name = "Strip B",
		description = "Type of strip to load",
		default = 'movie',
	)
   
   
	bpy.types.Scene.movieB_filepath = bpy.props.StringProperty(
		name = "",
		description = "Movie file path",
		default = "",
		subtype ='FILE_PATH',
	)
	
	bpy.types.Scene.imgSeqB_path = bpy.props.StringProperty(
		name = "",
		description ="Image sequence folder path",
		default = "",
		subtype ='DIR_PATH',
	)

## FUNCTIONS ##
###############


def delete_effect_strip():
	for index, strip in enumerate(bpy.context.scene.sequence_editor.sequences):
		strip.select = False
		if index == 2: # the effect strip
			strip.select = True
			bpy.ops.sequencer.delete()

def apply_wipe():
	
	# wipe effect
	bpy.ops.sequencer.effect_strip_add(type="WIPE")
	bpy.context.scene.sequence_editor.sequences_all["Wipe"].angle = -1.5708 # 90°
	bpy.context.scene.sequence_editor.sequences_all["Wipe"].use_default_fade = False
	bpy.context.scene.sequence_editor.sequences_all["Wipe"].effect_fader = bpy.context.scene.effect_fader
	
	
def apply_alpha_over():
	bpy.ops.sequencer.effect_strip_add(type="ALPHA_OVER")


def set_frame_range():
	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = bpy.context.scene.sequence_editor.sequences[0].frame_duration-1

def set_resolution():
	
	if bpy.context.scene.frame_current not in range(0, bpy.context.scene.frame_end):
		bpy.context.scene.frame_current = 0
	bpy.ops.render.opengl(sequencer=True)
	# needed to get the strip's resolution : to be on a active strip frame with at once the frame rendered
	
	frame_current = bpy.context.scene.frame_current
	elem = False
	strip = bpy.context.scene.sequence_editor.sequences[0]		

	if strip.type == 'IMAGE':
		elem = strip.strip_elem_from_frame(frame_current)
	elif strip.type == 'MOVIE':
		elem = strip.elements[0]
	
	if elem and elem.orig_width > 0 and elem.orig_height > 0:
		
		# set properties to use in wipe/horizontal mode
		bpy.context.scene.strip_width = elem.orig_width
		bpy.context.scene.strip_height = elem.orig_height
		
		# set resolution scene
		bpy.context.scene.render.resolution_x = bpy.context.scene.strip_width
		bpy.context.scene.render.resolution_y = bpy.context.scene.strip_height
		

def path_to_absolute(path):
	absolute_path = os.path.abspath(bpy.path.abspath(path))
	return absolute_path

def folder_to_sequence(folder):
	
	folder = path_to_absolute(folder)
	files = []
	for i in os.listdir(folder):
		files.append(i)
	files.sort()
	filesDict = []
	for i in files:
		frame = {"name":i}
		filesDict.append(frame)
   
	return filesDict


def clean_sequencer():
	# delete strips on sequencer
	try:
		for strip in bpy.context.scene.sequence_editor.sequences:
			strip.select = True
			bpy.ops.sequencer.delete() # delete the selection
	except:
		pass

def load_strip():
	if bpy.context.scene.load_type == "movie":
		bpy.ops.sequencer.movie_strip_add(filepath=bpy.context.scene.movie_filepath)
	elif bpy.context.scene.load_type == "img_seq":
		path = bpy.context.scene.imageSequence_path
		files = folder_to_sequence(path)
		bpy.ops.sequencer.image_strip_add(directory = path, files = files)
	bpy.context.scene.sequence_editor.sequences[0].use_translation = True
		
def load_strips():
	# strip A
	if bpy.context.scene.stripA_load_type == "movie":
		bpy.ops.sequencer.movie_strip_add(filepath=bpy.context.scene.movieA_filepath)
	elif bpy.context.scene.stripA_load_type == "img_seq":
		path = bpy.context.scene.imgSeqA_path
		files = folder_to_sequence(path)
		bpy.ops.sequencer.image_strip_add(directory = path, files = files)
	set_resolution() # RESOLUTION
	# strip B
	if bpy.context.scene.stripB_load_type == "movie":
		bpy.ops.sequencer.movie_strip_add(filepath=bpy.context.scene.movieB_filepath)
	elif bpy.context.scene.stripB_load_type == "img_seq":
		path = bpy.context.scene.imgSeqB_path
		files = folder_to_sequence(path)
		bpy.ops.sequencer.image_strip_add(directory = bpy.context.scene.imgSeqB_path, files = files)

def set_display_side():
	
	delete_effect_strip()
	# select strips to apply effect
	for index, strip in enumerate(bpy.context.scene.sequence_editor.sequences):
		strip.select = True
		strip.use_translation = True # active the image offset
	
	if bpy.context.scene.display_side == "wipe":
		apply_wipe()
		bpy.context.scene.render.resolution_x = bpy.context.scene.strip_width
		bpy.context.scene.render.resolution_y = bpy.context.scene.strip_height
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_x = 0
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_x = 0
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_y = 0
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_y = 0
   
   
	elif bpy.context.scene.display_side == "side_h":
		apply_wipe()
		bpy.context.scene.render.resolution_x = bpy.context.scene.strip_width*2
		bpy.context.scene.render.resolution_y = bpy.context.scene.strip_height
		bpy.context.scene.sequence_editor.sequences_all["Wipe"].effect_fader = 0.5
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_x = 0
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_x = bpy.context.scene.strip_width
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_y = 0
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_y = 0
	   
	elif bpy.context.scene.display_side == "side_v":
		apply_alpha_over()
		bpy.context.scene.render.resolution_x = bpy.context.scene.strip_width
		bpy.context.scene.render.resolution_y = bpy.context.scene.strip_height*2
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_x = 0
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_x = 0
		bpy.context.scene.sequence_editor.sequences[0].transform.offset_y = bpy.context.scene.strip_height
		bpy.context.scene.sequence_editor.sequences[1].transform.offset_y = 0

## PANEL ##
###########

class SEQUENCER_check_sequence(bpy.types.Panel):
	bl_label = "Check Sequence"
	bl_space_type = "SEQUENCE_EDITOR"
	bl_region_type = "UI"
	bl_category = "Custom"
	bl_options = {'DEFAULT_CLOSED'}
  
	def draw(self, context):
		layout = self.layout
		
		layout.prop(context.scene, "load_type", expand=True)
		
		row = layout.row(align=False)
		if bpy.context.scene.load_type == 'img_seq':
			row.prop(context.scene, "imageSequence_path", icon="FILE_IMAGE")
		elif bpy.context.scene.load_type == 'movie':
			row.prop(context.scene, "movie_filepath", icon="FILE_MOVIE")
		row.operator("load_movie_sequence.btn", icon="SEQUENCE")


class SEQUENCER_compare_sequence(bpy.types.Panel):
	bl_label = "Compare Strips"
	bl_space_type = "SEQUENCE_EDITOR"
	bl_region_type = "UI"
	bl_category = "Custom"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout = self.layout
		
		layout.prop(context.scene, "display_side", expand=True)
		if bpy.context.scene.display_side == "wipe":
			layout.prop(context.scene, "effect_fader")
		
		# STRIP A
		row = layout.row(align=False)
		row.prop(context.scene, "stripA_load_type")
		if bpy.context.scene.stripA_load_type == "movie":
			row.prop(context.scene, "movieA_filepath", icon="FILE_MOVIE")
		elif bpy.context.scene.stripA_load_type == "img_seq":
			row.prop(context.scene, "imgSeqA_path", icon="FILE_IMAGE")
		
		# STRIP B
		row = layout.row(align=False)
		row.prop(context.scene, "stripB_load_type")
		if bpy.context.scene.stripB_load_type == "movie":
			row.prop(context.scene, "movieB_filepath", icon="FILE_MOVIE")
		elif bpy.context.scene.stripB_load_type == "img_seq":
			row.prop(context.scene, "imgSeqB_path", icon="FILE_IMAGE")

		layout.operator("load_compare_sequence.btn", icon="SEQUENCE")
		layout.operator("swap.btn", icon="ARROW_LEFTRIGHT")
		
		#layout.prop(context.scene, "strip_height")
		#layout.prop(context.scene, "strip_width")


## OPERATOR ##
##############

class load_movie_sequence(bpy.types.Operator):
	bl_idname = "load_movie_sequence.btn"
	bl_label = "Load"
	bl_description = "Load sequence or movie to sequencer"
 
	def execute(self, context):
		
		clean_sequencer()
		load_strip()
		set_frame_range()
		set_resolution()
		return{'FINISHED'}


class load_compare_sequence(bpy.types.Operator):
	bl_idname = "load_compare_sequence.btn"
	bl_label = "Load"
	bl_description = "Load two strips to sequence and add a wipe effect to compare them"
 
	def execute(self, context):
		
		# delete strips on sequencer
		clean_sequencer()
	 
		# load strips
		load_strips()
		
		apply_wipe() # needs to be removed but it resolves problem
		
		set_frame_range()
		set_resolution()
		set_display_side()
	 
		return{'FINISHED'}

class swap_strips(bpy.types.Operator):
	bl_idname = "swap.btn"
	bl_label = "Swap"
	bl_description = "Invert strips"
 
	def execute(self, context):
		
		# delete strips on sequencer
		clean_sequencer()
		
		# swap path
		tmp_path_movie = bpy.context.scene.movieA_filepath
		tmp_path_imgSeq = bpy.context.scene.imgSeqA_path
		bpy.context.scene.movieA_filepath = bpy.context.scene.movieB_filepath
		bpy.context.scene.imgSeqA_path = bpy.context.scene.imgSeqB_path
		bpy.context.scene.movieB_filepath = tmp_path_movie
		bpy.context.scene.imgSeqB_path = tmp_path_imgSeq
		
		# swap strip type
		tmp_type = bpy.context.scene.stripA_load_type
		bpy.context.scene.stripA_load_type = bpy.context.scene.stripB_load_type
		bpy.context.scene.stripB_load_type = tmp_type
		
		# reload strips
		load_strips()
		
		apply_wipe() # needs to be removed but it resolves problem
		
		set_frame_range()
		set_resolution()
		set_display_side()
		
		pass
		return{'FINISHED'}

#########################
#########################



def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()



