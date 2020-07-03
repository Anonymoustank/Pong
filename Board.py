import pymunk
WHITE = 255, 255, 255

top_body = pymunk.Body(1, 100, pymunk.Body.STATIC)
top_wall = pymunk.Poly.create_box(top_body, size = (1280, 10))
top_body.position = 640, 725

bottom_body = pymunk.Body(1, 100, pymunk.Body.STATIC)
bottom_wall = pymunk.Poly.create_box(bottom_body, size = (1280, 10))
bottom_body.position = 640, -5

top_body.elasticity, top_wall.elasticity, bottom_body.elasticity, bottom_wall.elasticity = 0.99, 0.99, 0.99, 0.99
top_body.friction, top_wall.friction, bottom_body.friction, bottom_wall.friction = 0, 0, 0, 0

net = []

net.append(top_body)
net.append(top_wall)
net.append(bottom_body)
net.append(bottom_wall)

y_value = 0

for i in range(1, 11):
    y_value += 10
    y_value += 61/2
    exec("body%s = pymunk.Body(1, 100, pymunk.Body.KINEMATIC)" % i)
    exec("box%s = pymunk.Poly.create_box(body%s, size = (40, 61))" % (i, i))
    exec("box%s.color = WHITE" % i)
    exec("box%s.sensor = True" % i)
    exec("body%s.position = 640, y_value" % i)
    exec("net.append(body%s)" % i)
    exec("net.append(box%s)" % i)
    y_value += 61/2