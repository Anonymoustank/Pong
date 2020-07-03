import pymunk
WHITE = 255, 255, 255

top_body = pymunk.Body(1, 100, pymunk.Body.KINEMATIC)
top_wall = pymunk.Poly.create_box(top_body, size = (1280, 10))
top_body.position = 640, 725

bottom_body = pymunk.Body(1, 100, pymunk.Body.KINEMATIC)
bottom_wall = pymunk.Poly.create_box(bottom_body, size = (1280, 10))
bottom_body.position = 640, -5

net = []

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