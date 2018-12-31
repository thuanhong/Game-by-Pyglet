import pyglet
from pyglet.window import key
from object import *
import random


class gameWindow(pyglet.window.Window):
    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.fire_sound = pyglet.media.load('sound/player_gun.mp3', streaming=False)
        self.exp_sound = pyglet.media.load('sound/exp_01.mp3', streaming=False)


        self.set_location(400,100)
        self.frame_rate = 1/60.0

        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.speed = 800

        player_tmp = pyglet.sprite.Sprite(load_img('jet.png'))
        self.player = gameObject(self.width / 2.3, self.height / 7, player_tmp)

        self.mons1 = load_img('quai1.png')
        self.mons2 = load_img('quai2.png')
        self.mons3 = load_img('quai3.png')
        self.mons_list = [self.mons1, self.mons2, self.mons3]
        self.mons_draw = []

        self.shot = load_img('dan.png')
        self.shot_list = []
        self.fire = False
        self.fire_rate = 0

        self.space_list = []
        self.space_img = load_img('back2.jpg')

        for i in range(2):
            self.space_list.append(gameObject(0, i*1000, pyglet.sprite.Sprite(self.space_img)))

        self.exploit = pyglet.image.load_animation('img/bom.gif')
        self.exploit_list = []
        self.exp_batch = pyglet.graphics.Batch()
        self.time_bom = 1.5


    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True

        if symbol == key.UP:
            self.up = True
        if symbol == key.DOWN:
            self.down = True
        if symbol == key.SPACE:
            self.fire = True
        if symbol == key.ESCAPE:
            pyglet.app.exit()


    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.fire = False
        if symbol == key.RIGHT:
            self.right = False
        if symbol == key.LEFT:
            self.left = False
        if symbol == key.UP:
            self.up = False
        if symbol == key.DOWN:
            self.down = False


    def on_draw(self):
        self.clear()
        for space in self.space_list:
            space.draw()
        self.player.draw()
        for bul in self.shot_list:
            bul.draw()
        for mons in self.mons_draw:
            mons.draw()
        self.exp_batch.draw()


    def update_shot(self, dt):
        for gun in self.shot_list:
            gun.update()
            gun.posy += 2000 * dt
            if gun.posy > 750:
                self.shot_list.remove(gun)


    def fired(self, dt):
        self.fire_rate -= dt
        if self.fire_rate <= 0:
            self.shot_list.append(gameObject(self.player.posx + 52, self.player.posy + 191, pyglet.sprite.Sprite(self.shot)))
            self.fire_rate += 0.3
            self.fire_sound.play()


    def update_player(self, dt):
        self.player.update()
        if self.right and self.player.posx < self.width - 70:
            self.player.posx += self.speed * dt
        if self.left and self.player.posx > 0 - 70:
            self.player.posx -= self.speed * dt
        if self.up and self.player.posy < self.height - 80:
            self.player.posy += self.speed * dt
        if self.down and self.player.posy > 0 - 80:
            self.player.posy -= self.speed * dt


    def update_move_enemy(self, dt):
        for x in self.mons_draw:
            x.update()
            x.posy -= 100 * dt
            if x.posy < 0:
                self.mons_draw.remove(x)


    def head_shot(self, take, shot_list):
        for bullet in shot_list:
            if bullet.posx < take.posx + take.width and bullet.posx + bullet.width > take.posx \
                and bullet.posy < take.posy + take.height and bullet.height + bullet.posy > take.posy:
                shot_list.remove(bullet)
                return True


    def hit(self, dt):
        for take in self.mons_draw:
            if self.head_shot(take, self.shot_list):
                self.exploit_list.append(pyglet.sprite.Sprite(self.exploit, x=take.posx, y=take.posy, batch=self.exp_batch))
                self.mons_draw.remove(take)
                self.exp_sound.play()


    def update_exploit(self, dt):
        self.time_bom -= 0.1
        if self.time_bom <= 0:
            for exp in self.exploit_list:
                self.exploit_list.remove(exp)
                exp.delete()
            self.time_bom += 1.5


    def update_enenmy(self, dt):
        tmp = random.choice(self.mons_list)
        self.mons_draw.append(gameObject(random.randint(50, 1200), 700, pyglet.sprite.Sprite(tmp)))


    def update_space(self, dt):
        for space in self.space_list:
            space.update()
            space.posy -= 200 * dt
            if space.posy <= -1300:
                self.space_list.remove(space)
                self.space_list.append(gameObject(0, 780, pyglet.sprite.Sprite(self.space_img)))


    def update(self, dt):
        self.update_shot(dt)
        if self.fire:
            self.fired(dt)

        self.update_player(dt)
        self.update_space(dt)
        self.update_move_enemy(dt)
        if len(self.mons_draw) <= 7:
            self.update_enenmy(dt)
        self.hit(dt)
        self.update_exploit(dt)


if __name__ == "__main__":
    pyglet.options['audio'] = ('directsound', 'openal', 'pulse')
    window = gameWindow(1280, 720, "Matrix")
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
