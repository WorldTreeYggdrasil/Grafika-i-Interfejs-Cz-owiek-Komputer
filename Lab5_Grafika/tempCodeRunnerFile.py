light_diffuse = light_color
    light_ambient = [light_color[0] * 0.1, light_color[1] * 0.1, light_color[2] * 0.1, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)