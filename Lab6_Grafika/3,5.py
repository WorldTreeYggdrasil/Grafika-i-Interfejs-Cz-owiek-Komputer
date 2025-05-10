import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [0.1, 0.1, 0.0, 1.0]
light1_diffuse = [0.8, 0.8, 0.0, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [0.0, 0.0, -10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# Initialize wall visibility
wall_visibility = [True, True, True, True, True]
selected_wall = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)    
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glEnable(GL_TEXTURE_2D)
    #glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("tekstury/N3_t.tga")
    #image = Image.open("tekstury/cat.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    


    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    
    # Pyramid peak
    pyramid_peak = [0.0, 0.0, 5.0]
    
    # Base square vertices
    base_vertices = [
        [-5.0, -5.0, 0.0],
        [5.0, -5.0, 0.0],
        [5.0, 5.0, 0.0],
        [-5.0, 5.0, 0.0]
    ]
    
    # Base of the pyramid
    if wall_visibility[0]:
        # Triangle 1
        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*base_vertices[0])
        glTexCoord2f(1.0, 0.0)
        glVertex3f(*base_vertices[1])
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*base_vertices[2])
        glEnd()

        # Triangle 2
        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*base_vertices[0])
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*base_vertices[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3f(*base_vertices[3])
        glEnd()
    

    if wall_visibility[1]:
    # Triangular wall 1
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*base_vertices[0])
        glTexCoord2f(1.0, 0.0)
        glVertex3f(*base_vertices[1])
        glTexCoord2f(0.5, 0.5)
        glVertex3f(*pyramid_peak)
        glEnd()

    if wall_visibility[2]:
        # Triangular wall 2
        glBegin(GL_TRIANGLES)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(*base_vertices[1])
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*base_vertices[2])
        glTexCoord2f(0.5, 0.5)
        glVertex3f(*pyramid_peak)
        glEnd()

    if wall_visibility[3]:  
        # Triangular wall 3
        glBegin(GL_TRIANGLES)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*base_vertices[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3f(*base_vertices[3])
        glTexCoord2f(0.5, 0.5)
        glVertex3f(*pyramid_peak)
        glEnd()
        
    if wall_visibility[4]:  
        # Triangular wall 4
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(*base_vertices[3])
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*base_vertices[0])
        glTexCoord2f(0.5, 0.5)
        glVertex3f(*pyramid_peak)
        glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global selected_wall
    if action == GLFW_PRESS:
        if key == GLFW_KEY_B:
            selected_wall = 0
            print("Selected base")
        elif key == GLFW_KEY_1:
            selected_wall = 1
            print("Selected wall 1")
        elif key == GLFW_KEY_2:
            selected_wall = 2
            print("Selected wall 2")
        elif key == GLFW_KEY_3:
            selected_wall = 3
            print("Selected wall 3")
        elif key == GLFW_KEY_4:
            selected_wall = 4
            print("Selected wall 4")
        elif key == GLFW_KEY_S:
            wall_visibility[selected_wall] = True
            if selected_wall == 0:
                print("Base is now visible")
            else:
                print(f"Wall {selected_wall} is now visible")
                print("Current wall visibility:", wall_visibility)
        elif key == GLFW_KEY_H:
            wall_visibility[selected_wall] = False
            if selected_wall == 0:
                print("Base is now hidden")
            else:
                print(f"Wall {selected_wall} is now hidden")
                print("Current wall visibility:", wall_visibility)
        elif key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)



def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
        

def print_instructions():
    print("Pyramid Viewer Instructions:")
    print("B: Select the base")
    print("1-4: Select a wall")
    print("S: Show the selected wall")
    print("H: Hide the selected wall")
    print("Mouse: Rotate the pyramid")
    print("ESC: Exit the program")

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)
    glDisable(GL_CULL_FACE)

    startup()
    print_instructions()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
