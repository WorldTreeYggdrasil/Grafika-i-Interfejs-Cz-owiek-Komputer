for x in range(10):
        for y in range(10):
            # Create a model matrix for the cube
            translation_matrix = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0))
            M_matrix = translation_matrix * rotation_matrix

            glUniformMatrix4fv(M_location, 1, GL_FALSE, glm.value_ptr(M_matrix))

            glDrawArrays(GL_TRIANGLES, 0, 36)