import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key, mouse
import Board
import random
import math

WHITE = 255, 255, 255
GRAY = 127.5, 127.5, 127.5
options = DrawOptions()
window = pyglet.window.Window(1280, 720, "Game", resizable = False)
window.set_mouse_visible(False)
space = pymunk.Space()
space.gravity = 0, 0

left_body = pymunk.Body(1, 100, pymunk.Body.KINEMATIC)
left_player = pymunk.Poly.create_box(left_body, size = (15, 150))
left_body.position = 30, 360
left_player.position = 30, 360

right_body = pymunk.Body(1, 100, pymunk.Body.KINEMATIC)
right_player = pymunk.Poly.create_box(right_body, size = (15, 150))
right_body.position = 1250, 360
right_player.position = 1250, 360

ball_body = pymunk.Body(1, 100)
ball = pymunk.Circle(ball_body, 10, offset = (0, 0))
ball_body.position = 640, 360
ball.position = 640, 360

left_player.color, right_player.color, ball.color = WHITE, WHITE, GRAY

space.add(left_body, left_player, right_body, right_player)

left_player.elasticity, left_body.elasticity, right_player.elasticity, right_body.elasticity, ball.elasticity, ball_body.elasticity = 0.99, 0.99, 0.99, 0.99, 0.99, 0.99
left_player.friction, left_body.friction, right_player.friction, right_body.friction, ball.friction, ball_body.friction = 0, 0, 0, 0, 0, 0

w_pressed, s_pressed, up_pressed, down_pressed = False, False, False, False

speed = 12
started = False
count = 1

damp_level = 1
left_score = 0
right_score = 0

def zero_gravity(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, (0,0), damp_level, dt)

ball_body.velocity_func = zero_gravity

def shoot():
    global damp_level
    ball_body.position = 640, 360
    ball.position = 640, 360
    ball_body.angle = 0
    ball.angle = 0
    random_num = random.randint(1, 2)
    if random_num == 1:
        ball_body.angle = random.uniform(math.pi/6, (-1 * math.pi)/6)
        ball.angle = ball_body.angle
    else:
        ball_body.angle = random.uniform((5 * math.pi)/6, (7 * math.pi)/6)
        ball.angle = ball_body.angle
    power = 40
    damp_level = 0
    ball_body.apply_force_at_local_point((1000 * power, 1000), (1000 * power, 1000))

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    if started == False:
        left_label = pyglet.text.Label('Use W/S to move up/down', font_name='Times New Roman', font_size=18, x=200, y=360, anchor_x='center', anchor_y='center')
        left_label.draw()
        right_label = pyglet.text.Label('Use the up/down arrows to move up/down', font_name='Times New Roman', font_size=18, x=1000, y=360, anchor_x='center', anchor_y='center')
        right_label.draw()
        top_label = pyglet.text.Label('Press Space to Start', font_name='Times New Roman', font_size=36, x=640, y=600, anchor_x='center', anchor_y='center')
        top_label.draw()
    else:
        left_score_label = pyglet.text.Label(str(left_score), font_name='Times New Roman', font_size=60, x=500, y=650, anchor_x='center', anchor_y='center')
        left_score_label.draw()
        right_score_label = pyglet.text.Label(str(right_score), font_name='Times New Roman', font_size=60, x=780, y=650, anchor_x='center', anchor_y='center')
        right_score_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    global w_pressed, s_pressed, up_pressed, down_pressed, started
    if symbol == key.W:
        w_pressed = True
        s_pressed = False
        x, y = left_player.position
        if y <= 720 - 75:
            left_player.position = x, y + speed
            x,y = left_body.position
            left_body.position = x, y + speed
    elif symbol == key.S:
        w_pressed = False
        s_pressed = True
        x, y = left_player.position
        if y >= 75:
            left_player.position = x, y - speed
            x,y = left_body.position
            left_body.position = x, y - speed
    elif symbol == key.UP:
        up_pressed = True
        down_pressed = False
        x, y = right_player.position
        if y <= 720 - 75:
            right_player.position = x, y + speed
            x,y = right_body.position
            right_body.position = x, y + speed
    elif symbol == key.DOWN:
        up_pressed = False
        down_pressed = True
        x, y = right_player.position
        if y >= 75:
            right_player.position = x, y - speed
            x,y = right_body.position
            right_body.position = x, y - speed
    elif symbol == key.SPACE and started == False:
        for i in Board.net:
            space.add(i)
        space.add(ball, ball_body)
        shoot()
        started = True

@window.event
def on_key_release(symbol, modifiers):
    global w_pressed, s_pressed, up_pressed, down_pressed
    if symbol == key.W:
        w_pressed = False
    elif symbol == key.S:
        s_pressed = False
    elif symbol == key.UP:
        up_pressed = False
    elif symbol == key.DOWN:
        down_pressed = False

def refresh(time):
    global count, damp_level, energy, left_score, right_score
    ball_body_x, ball_body_y = ball_body.position
    if ball_body_x < 0:
        right_score += 1
        shoot()
        count = 1
    elif ball_body_x > 1280:
        left_score += 1
        shoot()
        count = 1
    space.step(time)
    if count == 1 and started == True:
        energy = ball_body.kinetic_energy
        count += 1
    if ball_body.kinetic_energy == 0:
        damp_level = 1
    else:
        damp_level = energy/ball_body.kinetic_energy
    if w_pressed == True and s_pressed == False:
        x, y = left_player.position
        if y <= 720 - 75:
            left_player.position = x, y + speed
            x,y = left_body.position
            left_body.position = x, y + speed
    elif w_pressed == False and s_pressed == True:
        x, y = left_player.position
        if y >= 75:
            left_player.position = x, y - speed
            x,y = left_body.position
            left_body.position = x, y - speed
    elif up_pressed == True and down_pressed == False:
        x, y = right_player.position
        if y <= 720 - 75:
            right_player.position = x, y + speed
            x,y = right_body.position
            right_body.position = x, y + speed
    elif up_pressed == False and down_pressed == True:
        x, y = right_player.position
        if y >= 75:
            right_player.position = x, y - speed
            x,y = right_body.position
            right_body.position = x, y - speed

if __name__ == "__main__":
    pyglet.clock.schedule_interval(refresh, 1.0/120.0)
    pyglet.app.run()