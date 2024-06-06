import sys
from random import randrange
import pygame as pg
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

# pygame settings
FPS = 60
RES = WIDTH, HEIGHT = 900, 720

# initial pg, and connect system coordinate
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# pymunk settings
space = pymunk.Space()
space.gravity = 0, 8000

# points
R0, R1, R2, R3 = (0, 0), (WIDTH // 2 - 15, 30), (WIDTH // 2 + 15, 30), (WIDTH, HEIGHT - 120)
L0, L1, L2, L3 = (WIDTH, 0), (WIDTH//2 + 15, 30), (WIDTH//2 - 15, 30), (0, HEIGHT - 120)
lower_left_corner = (0, HEIGHT)
lower_right_corner = (WIDTH, HEIGHT)

# Pymunk code


# create segment(platforms)
def create_segment(start, end, radius):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(space.static_body, start, end, radius)
    space.add(body, segment_shape)
    return segment_shape


# create balls
def create_ball(pos):
    ball_mass, radius = 1, 4
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, radius)
    ball_body = pymunk.Body(ball_mass, ball_moment, body_type=pymunk.Body.DYNAMIC)
    ball_body.position = pos
    ball_shape = pymunk.Circle(ball_body, radius)
    ball_shape.elasticity = 0.8
    ball_shape.friction = 0.5
    ball_shape.color = [randrange(256) for i in range(4)]
    space.add(ball_body, ball_shape)
    return ball_shape


# create peg(circle)
def create_peg(x, y):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.elasticity = 0.3
    circle_shape.friction = 0.5
    space.add(circle_shape)
    return circle_shape

# PyGame code draw elements with help pygame


def draw_balls(balls_list):
    for ball in balls_list:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pg.draw.circle(screen, ball.color, (pos_x, pos_y), 2)


def draw_circle(pegs_list):
    for peg in pegs_list:
        pos_x = peg.body.position.x + peg.offset[0]
        pos_y = peg.body.position.x + peg.offset[1]
        pg.draw.circle(screen, "yellow", (pos_x, pos_y), peg.radius)


def draw_borders(borders_list):
    for border in borders_list:
        start_pos = border.a + border.body.position
        end_pos = border.b + border.body.position
        pg.draw.line(screen, (128, 128, 128), start_pos, end_pos, int(border.radius))


# Creating pymunk objects to then pass this to the soldering code for rendering
balls = []

for i in range(0, 2000):
    balls.append(create_ball((randrange(0, WIDTH), 0)))

# creating borders for draw with helps pygame
borders = []

# Bottom Borders
for i in range(0, 17):
    borders.append(create_segment((i * 60, HEIGHT), (i*60, HEIGHT-120), 5))
borders.append(create_segment((0, HEIGHT), (WIDTH, HEIGHT), 5))

# Top Borders
borders.append(create_segment(R0, R1, 5))
borders.append(create_segment(L0, L1, 5))

borders.append(create_segment(R2, R3, 5))
borders.append(create_segment(L2, L3, 5))

# for draw with helps pygame
pegs = []

# creating pegs, which form Pascal triangle. stepW - step width(between) balls. stepH - step top
stepW = 30
stepH = 40
for i in range(0, 13):
    k = WIDTH / 2 if i == 0 else WIDTH / 2 - i * 30
    h = create_peg(WIDTH / 2 if i == 0 else WIDTH / 2 - i * 30, HEIGHT / 10 if i == 0 else HEIGHT / 10 + i * stepH)
    pegs.append(h)
    count_balls_in_row = 1
    while count_balls_in_row != i + 1:
        pegs.append(create_peg(k + count_balls_in_row * 60, HEIGHT / 10 if i == 0 else HEIGHT / 10 + i * stepH))
        count_balls_in_row += 1

while True:
    screen.fill(pg.Color('black'))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            create_ball(event.pos)

    space.step(1 / FPS)
    #space.debug_draw(draw_options)
    draw_balls(balls)
    draw_circle(pegs)
    draw_borders(borders)

    pg.display.flip()
    clock.tick(FPS)
