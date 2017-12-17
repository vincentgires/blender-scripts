import bpy, math
import bgl
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value

def draw_distance_opengl(self, context):
    # cette fonction sera appelee a chaque redraw des vues 3d
    # choisir une taille
    bgl.glPointSize(10)
    # choisir une couleur
    # 3i est une specialisation de glColor, qui prend 3 arguments de type float (0.0-1.0)
    bgl.glColor3f(1.0, 0.0, 0.0)
    # commencer le dessin en mode points
    # les points sont des carres... pour des ronds, il faut effectivement dessiner un polygone.
    bgl.glBegin(bgl.GL_POINTS)
    # dessiner un point a un certain endroit
    # egalement une specialisation
    bgl.glVertex3f(1.0, 1.0, 1.0)
    # finir le dessin
    bgl.glEnd()
    # changer de taille
    bgl.glPointSize(50)
    # autre couleur
    bgl.glColor3f(0.0, 0.0, 1.0)
    # recommencer le dessin (necessaire pour le changement de taille)
    bgl.glBegin(bgl.GL_POINTS)
    # autre point
    bgl.glVertex3f(-1.0, 0.0, 2.0)
    # finir le dessin
    bgl.glEnd()

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class DistanceNode(Node):
    '''Distance node'''
    bl_idname = 'DistanceNodeType'
    bl_label = 'Distance'
    
    display = bpy.props.BoolProperty(name='display', default=True)
    opengl_handle = [None]
    
    def init(self, context):
        self.inputs.new('NodeSocketVector', "VectorA")
        self.inputs.new('NodeSocketVector', "VectorB")
        self.outputs.new('NodeSocketFloat', "Distance")
        
        self.opengl_handle[0] = bpy.types.SpaceView3D.draw_handler_add(
            draw_distance_opengl, (self,context), 'WINDOW', 'POST_VIEW')
        
    def update(self):
        
        if len(self.inputs) >= 2:
        
            VectorA = self.inputs["VectorA"].default_value
            VectorB = self.inputs["VectorB"].default_value
            
            Distance = math.sqrt(
                (VectorB[0]-VectorA[0])**2 + (VectorB[1]-VectorA[1])**2 + (VectorB[2]-VectorA[2])**2
                )
            
            # send data value to connected nodes
            send_value(self.outputs, Distance)
    
    def free(self):
        bpy.types.SpaceView3D.draw_handler_remove(
            self.opengl_handle[0], 'WINDOW')
    
    def draw_label(self):
        return "Distance"

