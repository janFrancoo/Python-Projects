import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

cube_vertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
cube_quads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))


def wire_cube():
    glBegin(GL_LINES)
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()


def solid_cube():
    glBegin(GL_QUADS)
    for quad in cube_quads:
        for vertex in quad:
            glVertex3fv(cube_vertices[vertex])
    glEnd()


pg.init()
window_size = (1080, 720)
pg.display.set_mode(window_size, DOUBLEBUF | OPENGL)
gluPerspective(60, (window_size[0] / window_size[1]), 0.1, 100.0)
glTranslatef(0.0, 0.0, -5)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    solid_cube()
    pg.display.flip()
    pg.time.wait(10)
