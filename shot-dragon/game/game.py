import pyglet
from pyglet.window import key
import math
import random
import os
import sys
import time

game_start = 0
cwd = os.getcwd()
pyglet.options['audio'] = ('directsound', 'openal', 'pulse')

pyglet.lib.load_library('avbin')
pyglet.have_avbin = True

window = pyglet.window.Window(fullscreen=True)
pyglet.resource.path.append(cwd + '/image')
pyglet.resource.reindex()


def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.width // 2


center_x = window.width / 2
center_y = window.height / 2

start_pic = pyglet.resource.image('start1.jpg')
center_anchor(start_pic)

planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)

ship_image = pyglet.resource.image('ship.png')
center_anchor(ship_image)

ship_on_image = pyglet.resource.image('ship_on1.png')
center_anchor(ship_on_image)

bullet_image = pyglet.resource.image('bullet.png')
center_anchor(bullet_image)

alien_image = pyglet.resource.image('rsz_gd.png')
center_anchor(alien_image)

galaxy = pyglet.resource.image('Orange_galaxy.jpg')
center_anchor(galaxy)

# --------------------------------------sound---------------------------------
themesound = pyglet.resource.media('starwar.mp3')
themesound.play()


def shoot_sound():
    shoot = pyglet.resource.media('cut_lazer.mp3')
    shoot.play()


# -------------------------------------text-----------------------------------
start_text = pyglet.text.Label('Press ENTER to continue',
                               font_name='Arial', font_size=36, x=center_x,
                               y=center_y - 350,
                               anchor_x='center', anchor_y='center')
start_text.color = (255, 204, 153, 255)

guide_text = pyglet.text.Label("You are just a weak creature. Be careful!"
                               + " Press Up to fire engine",
                               font_name='Arial', font_size=30, x=center_x,
                               y=center_y, anchor_x='center',
                               anchor_y='center')
guide_text.color = (255, 231, 186, 255)

guide_text1 = pyglet.text.Label("Watch Out! You hit the planet, you die!"
                                + " Hit the dragon, you die. Dragon hit you,"
                                + "you die!", font_name='Arial',
                                font_size=30, x=center_x, y=center_y,
                                anchor_x='center',
                                anchor_y='center')
guide_text1.color = (255, 231, 186, 255)

ship_life = pyglet.text.Label('Lives', font_name='Arial', font_size=25,
                              x=window.width - 120, y=window.height - 175,
                              anchor_x='left', anchor_y='bottom')
ship_life.color = (255, 255, 255, 255)

ship_lives = pyglet.text.Label('Speed', font_name='Arial', font_size=25,
                               x=window.width - 120, y=window.height - 225,
                               anchor_x='left', anchor_y='bottom')
ship_lives.color = (255, 255, 255, 255)

dragon_life = pyglet.text.Label('Dragon', font_name='Arial', font_size=25,
                                x=window.width - 120,
                                y=window.height - 300, anchor_x='left',
                                anchor_y='bottom')
dragon_life.color = (255, 255, 255, 255)

dragon_lifepoint = pyglet.text.Label('Speed', font_name='Arial',
                                     font_size=25, x=window.width - 120,
                                     y=window.height - 350, anchor_x='left',
                                     anchor_y='bottom')
dragon_lifepoint.color = (255, 255, 255, 255)

win = pyglet.text.Label('You Win', font_name='Arial', font_size=50,
                        x=center_x, y=center_y,
                        anchor_x='center', anchor_y='center')
dragon_lifepoint.color = (255, 255, 255, 255)

lose = pyglet.text.Label('You lose', font_name='Arial', font_size=50,
                         x=center_x, y=center_y, anchor_x='center',
                         anchor_y='center')
dragon_lifepoint.color = (255, 255, 255, 255)

# ---------------------------------Class object-----------------------------------------


class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(image, x, y, batch=None)
        self.x = x
        self.y = y
        self.mass = 2000000
        self.radius = self.image.width / 2

    def update(self, dt):
        distance, angle = self.dist_vector(ship)
        if distance <= ship.radius + self.radius:
            ship.reset()
            ship.alive = False
            return
        force, angle = self.force_on(ship)
        force_x = force * math.cos(angle) * dt
        force_y = force * math.sin(angle) * dt
        ship.dx += force_x
        ship.dy += force_y

    def dist_vector(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        angle = math.acos(float(dx) / distance)
        if dy < 0:
            angle = 2*math.pi - angle
        return (distance, angle)

    def force_on(self, target):
        G = 1
        distance, angle = self.dist_vector(target)
        return((-G * self.mass) / (distance ** 2), angle)


class Ship(pyglet.sprite.Sprite, key.KeyStateHandler):
    def __init__(self, image, x=0, y=0, dx=0, dy=0, rotv=0, batch=None):
        super(Ship, self).__init__(image, x=0, y=0, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rotation = rotv
        self.thrust = 300.0
        self.rot_spd = 150.0
        self.rot_left = False
        self.rot_right = False
        self.engines = False
        self.alive = True
        self.radius = self.image.width / 2
        self.shot_timer = 0.2
        self.reload_timer = self.shot_timer
        self.bullets = []
        self.lives = 7
        self.end = True

    def reset(self):
        self.life_timer = 2.0
        self.x = center_x + 500
        self.y = center_y
        self.dx = 0
        self.dy = 200
        self.rotation = -90

    def update(self, dt):
        self.image = ship_image
        if self.rot_left:
            self.rotation -= self.rot_spd * dt
        if self.rot_right:
            self.rotation += self.rot_spd * dt
        self.direction = wrap(self.rotation, 360.0)
        if self.engines:
            self.image = ship_on_image
            rotation_x = math.cos(to_radian(self.rotation))
            rotation_y = math.sin(to_radian(-self.rotation))
            self.dx += self.thrust * rotation_x * dt
            self.dy += self.thrust * rotation_y * dt
        self.x += self.dx * dt
        self.y += self.dy * dt
        ship_lives.text = '%d' % self.lives
        if not self.alive:
            self.life_timer -= dt
            if self.life_timer > 0:
                return
            else:
                self.reset()
                self.lives -= 1
                self.alive = True
        rotation_x = math.cos(to_radian(self.rotation))
        rotation_y = math.sin(to_radian(-self.rotation))
        if self.reload_timer > 0:
            self.reload_timer -= dt
        elif self[key.SPACE]:
            self.bullets.append(Bullet(self.x, self.y,
                                       rotation_x*500 + self.dx,
                                       rotation_y*500 + self.dy, bullets))
            self.reload_timer = self.shot_timer
            shoot_sound()

        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        if self.lives == 0:
            self.end = False


class Bullet(pyglet.sprite.Sprite):
    def __init__(self, x=0, y=0, dx=0, dy=0, batch=None):
        super(Bullet, self).__init__(bullet_image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = self.image.width / 2
        self.timer = 5.0

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        self.timer -= dt
        distance, angle = planet.dist_vector(self)
        if distance <= planet.radius or self.timer < 0:
            ship.bullets.remove(self)
        dist, angle = dist_vec_to(self, alien)
        if dist < alien.radius:
            ship.bullets.remove(self)
            alien.health -= 100
            return


class Alien(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, dx=0, dy=0, batch=None):
        super(Alien, self).__init__(image, x, y, batch=None)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = self.image.width / 2
        self.alive = True
        self.accel_spd = 200.0
        self.max_spd = 550.0
        self.health = 10000
        self.life_timer = 2

    def update(self, dt):
        if self.health == 0:
            self.alive = False
        if random.random() < 0.5:
            accel_dir = random.random() * math.pi * 2
            accel_a = random.random() * self.accel_spd
            accel_x, accel_y = vec_to_xy(accel_a, accel_dir)
            self.dx += accel_x
            self.dy += accel_y
        if self.alive:
            self.dx = min(self.dx, self.max_spd)
            self.dx = max(self.dx, -self.max_spd)
            self.dy = min(self.dy, self.max_spd)
            self.dy = max(self.dy, -self.max_spd)

            self.x += self.dx * dt
            self.y += self.dy * dt
            if self.x == center_x + 500:
                self.x += 300
            self.x = wrap(self.x, window.width)
            self.y = wrap(self.y, window.height)
        dragon_lifepoint.text = '%d' % self.health
        player_dist, player_angle = dist_vec_to(self, ship)
        if player_dist < (ship.radius + self.radius) * 0.75:
            ship.reset()
            ship.alive = False


bullets = pyglet.graphics.Batch()
planet = Planet(planet_image, center_x, center_y, None)
ship = Ship(ship_image)
ship.reset()
alien = Alien(alien_image)
gala = pyglet.sprite.Sprite(galaxy, center_x, center_y + 420)
start = pyglet.sprite.Sprite(start_pic, center_x, center_y + 420)


def wrap(value, width):
    if width == 0:
        return 0
    if value > width:
        value -= width
    if value < 0:
        value += width
    return value


def to_radian(degrees):
    return (math.pi * degrees / 180.0)


def update(dt):
    planet.update(dt)
    ship.update(dt)
    for bullet in ship.bullets:
        bullet.update(dt)
    alien.update(dt)


def make_vec(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return (0, 0)
    angle = math.acos(float(dx) / distance)
    if dy < 0:
        angle = 2*math.pi - angle
    return (distance, angle)


def vec_to_xy(distance, angle):
    x = distance * math.cos(angle)
    y = distance * math.sin(angle)
    return (x, y)


def dist_vec_to(source, target):
    return make_vec((source.x, source.y), (target.x, target.y))


def exit():
    time.sleep(3)
    sys.exit()


@window.event
def on_draw():
    global game_start
    if game_start is 0:
        window.clear()
        start.draw()
        start_text.draw()
    elif game_start is 1:
        window.clear()
        start.opacity = 140
        start.draw()
        guide_text.draw()
    elif game_start is 2:
        window.clear()
        start.draw()
        guide_text1.draw()
    elif game_start is 3:
        window.clear()
        gala.draw()
        planet.draw()
        bullets.draw()
        if ship.alive:
            ship.draw()
        if not ship.end:
            game_start = 5
        if alien.alive:
            alien.draw()
        else:
            game_start = 4
        ship_life.draw()
        ship_lives.draw()
        dragon_life.draw()
        dragon_lifepoint.draw()
    elif game_start is 4:
        window.clear()
        start.opacity = 255
        start.draw()
        win.draw()
    elif game_start is 5:
        window.clear()
        start.draw()
        lose.draw()


@window.event
def on_key_press(symbol, modifiers):
    global game_start
    if symbol == key.UP:
        ship.engines = True
    if symbol == key.LEFT:
        ship.rot_left = True
    if symbol == key.RIGHT:
        ship.rot_right = True
    if symbol == key.ENTER:
        if game_start < 3:
            game_start += 1


@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.UP:
        ship.engines = False
    if symbol == key.LEFT:
        ship.rot_left = False
    if symbol == key.RIGHT:
        ship.rot_right = False


window.push_handlers(ship)
pyglet.clock.schedule_interval(update, 1/80.0)
pyglet.app.run()
