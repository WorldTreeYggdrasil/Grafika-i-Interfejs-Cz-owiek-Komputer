import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

    # generate colors / deform
    global R1, G1, B1, R2, G2, B2, R3, G3, B3, R4, G4, B4, D
    R1 = random.uniform(0.0, 1.0)
    G1 = random.uniform(0.0, 1.0)
    B1 = random.uniform(0.0, 1.0)
    R2 = random.uniform(0.0, 1.0)
    G2 = random.uniform(0.0, 1.0)
    B2 = random.uniform(0.0, 1.0)
    R3 = random.uniform(0.0, 1.0)
    G3 = random.uniform(0.0, 1.0)
    B3 = random.uniform(0.0, 1.0)
    R4 = random.uniform(0.0, 1.0)
    G4 = random.uniform(0.0, 1.0)
    B4 = random.uniform(0.0, 1.0)
    D = random.randint(1, 50)

def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # center
    center_x = 0
    center_y = 0

    # rectangle
    width = 100.0
    height = 50.0
    deform = D

    glBegin(GL_TRIANGLES)

    # First triangle
    glColor3f(R1, G1, B1)
    glVertex2f(center_x + (width), center_y + (height))
    glColor3f(R2, G2, B2)
    glVertex2f(center_x - (width) + deform*0.5, center_y + (height) + deform*1.5)
    glColor3f(R3, G3, B3)
    glVertex2f(center_x - (width), center_y - (height))
    
    # Second triangle
    glColor3f(R3, G3, B3)
    glVertex2f(center_x - (width), center_y - (height))
    glColor3f(R1, G1, B1)
    glVertex2f(center_x + (width), center_y + (height))
    glColor3f(R2, G2, B2)
    glVertex2f(center_x + (width)+ deform*1, center_y - (height)+ deform*0.7)

    glEnd()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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
