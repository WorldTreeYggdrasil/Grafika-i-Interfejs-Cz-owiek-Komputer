import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


viewer = [0.0, 0.0, 10.0]
R=5.0
theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

phi = 0.0
mouse_y_pos_old = 0
delta_y = 0
right_mouse_button_pressed = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0


color_component = 0
light_color = [0.8, 0.8, 0.0, 1.0]


light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 5.0, 1.0]

light1_position = [0.0, 0.0, 5.0, 1.0]
light1_ambient = [0.1, 0.1, 0.0, 1.0]
light1_diffuse = [0.8, 0.8, 0.0, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


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


def shutdown():
    pass

def keyboard_key_callback(window, key, _ , action, mods ):
    global light_color, color_component, move_light_source
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_C and action == GLFW_PRESS:
        color_component = (color_component + 1) % 3
        print(f"Current color component: {['Red', 'Green', 'Blue'][color_component]}")
    elif key == GLFW_KEY_N and action == GLFW_PRESS:
        light_color[color_component] = min(1.0, light_color[color_component] + 0.1)
        print(f"Current color: {light_color}")
    elif key == GLFW_KEY_M and action == GLFW_PRESS:
        light_color[color_component] = max(0.0, light_color[color_component] - 0.1)
        print(f"Current color: {light_color}")

def render(time):
    global theta, phi, light_position, R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


    theta_rad = theta * np.pi / 180.0
    phi_rad = phi * np.pi / 180.0
    light_position[0] = R * np.cos(theta_rad) * np.cos(phi_rad)
    light_position[1] = R * np.sin(phi_rad)
    light_position[2] = R * np.sin(theta_rad) * np.cos(phi_rad)
    light1_position[0] = -light_position[0]  # Negate the x-coordinate
    light1_position[1] = -light_position[1]  # Negate the y-coordinate
    light1_position[2] = -light_position[2]  # Negate the z-coordinate
    # Set the light position
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    # Draw the light source
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(light1_position[0], light1_position[1], light1_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    #The object
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    light_diffuse = light_color
    light_ambient = [light_color[0] * 0.1, light_color[1] * 0.1, light_color[2] * 0.1, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

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



def mouse_motion_callback(window, x_pos, y_pos):
    global theta, phi, delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)


    print("ESC - exit\n"
          "C - change color component\n"
          "N - increase color component\n"
          "M - decrease color component\n")
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

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
