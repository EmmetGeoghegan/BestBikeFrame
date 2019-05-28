# Graphing Engine
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.locals import *
import pygame.color
import pygame
import math
import inspect
import pymunk


"""
Pymunk constraints demo. Showcase of all the constraints included in Pymunk.
Adapted from the Chipmunk Joints demo:
https://github.com/slembcke/Chipmunk2D/blob/master/demo/Joints.c
"""


pymunk.pygame_util.positive_y_is_up = False

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


help_txt = font.render(
    "Pymunk constraints demo. Use mouse to drag/drop. Hover to see descr.",
    1, pygame.color.THECOLORS["darkgray"])

space = pymunk.Space()
space.gravity = (0.0, 900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# containers
box_size = 200
w = screen.get_width()
h = screen.get_height()
for i in range(6):
    sw = pymunk.Segment(space.static_body,
                        (0, i*box_size), (w, i * box_size), 1)
    sw.friction = 1
    sw.elasticity = 1
    sh = pymunk.Segment(space.static_body,
                        (i*box_size, 0), (i*box_size, h-box_size), 1)
    sh.friction = 1
    sh.elasticity = 1
    space.add(sw, sh)


def add_ball(space, pos, box_offset):
    body = pymunk.Body()
    body.position = Vec2d(pos) + box_offset
    shape = pymunk.Circle(body, 20)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


def add_bar(space, pos, box_offset):
    body = pymunk.Body()
    body.position = Vec2d(pos) + box_offset
    shape = pymunk.Segment(body, (60, 40), (-10, -40), 6)
    shape.mass = 2
    shape.friction = 0.7
    space.add(body, shape)
    return body


txts = {}

box_offset = box_size*2, 0
b1 = add_bar(space, (50, 60), box_offset)
b2 = add_bar(space, (150, 60), box_offset)
c = pymunk.PivotJoint(b1, b2, Vec2d(box_offset) + (100, 60))
txts[box_offset] = inspect.getdoc(c)
# space.add(c)


mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

# Build rendered help texts
box_texts = {}
for k in txts:
    l = 0
    box_texts[k] = []
    # Only take the first 5 lines.
    for line in txts[k].splitlines()[:5]:
        txt = font.render(line, 1, pygame.color.THECOLORS["black"])
        box_texts[k].append(txt)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if mouse_joint != None:
                space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit != None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                mouse_joint = pymunk.PivotJoint(mouse_body, shape.body,
                                                (0, 0), shape.body.world_to_local(nearest))
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1-0.15) ** 60
                space.add(mouse_joint)

        elif event.type == MOUSEBUTTONUP:
            if mouse_joint != None:
                space.remove(mouse_joint)
                mouse_joint = None

    screen.fill(pygame.color.THECOLORS["white"])

    screen.blit(help_txt, (5, screen.get_height() - 20))

    mouse_pos = pygame.mouse.get_pos()

    # Display help message
    x = mouse_pos[0] / box_size * box_size
    y = mouse_pos[1] / box_size * box_size
    if (x, y) in box_texts:
        txts = box_texts[(x, y)]
        i = 0
        for txt in txts:
            pos = (5, box_size * 2 + 10 + i*20)
            screen.blit(txt, pos)
            i += 1

    mouse_body.position = mouse_pos

    space.step(1./60)

    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
