import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # center
    center_x = 0
    center_y = 0

    #rectangle
    width = 100.0
    height = 50.0

    glBegin(GL_TRIANGLES)

    # First triangle
    # First vertex (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(center_x - (width), center_y + (height))

    # Second vertex (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(center_x + (width), center_y + (height))

    # Third vertex (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(center_x + (width), center_y - (height))

    glEnd()

    glBegin(GL_TRIANGLES)

    # Second triangle
    # First vertex (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(center_x - (width), center_y + (height))

    # Second vertex (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(center_x + (width), center_y - (height))

    # Third vertex (yellow)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(center_x - (width), center_y - (height))

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
