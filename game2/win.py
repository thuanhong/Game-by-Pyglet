import pyglet
from pyglet.window import key
from object import *
from random import randint, choice
from math import sin


class gameWindow(pyglet.window.Window):
    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.fire_sound = pyglet.media.load('sound/player_gun.mp3', streaming=False)
        self.exp_sound = pyglet.media.load('sound/exp_01.mp3', streaming=False)

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
        self.shot_ene = load_img('dan1.png')
        self.shot_enemy_list = []
        self.fire_enemy_rate = 0

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
        self.wait = 1.5

        label = pyglet.text.Label("Score", font_size=36, y=650, x=1000, batch=self.exp_batch)
        self.score = pyglet.text.Label("0", font_size=36, y=650, x=1150, batch=self.exp_batch)
        self.text = pyglet.text.Label("Press ENTER to PLAY",
                                        font_size=45,
                                        y=self.height/2,
                                        x= self.width/2,
                                        anchor_x = 'center',
                                        anchor_y = 'center')

        back_tmp = pyglet.image.load_animation('img/giphy.gif')
        self.back_ground = pyglet.sprite.Sprite(img=back_tmp)
        self.back_ground.update(scale_x=self.width/self.back_ground.width, scale_y=self.height/self.back_ground.height)
        self.play = False
        self.alive = False


    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        if symbol == key.ENTER:
            self.play = True
            self.alive = True
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


    def reload(self):
        self.mons_draw.clear()
        self.shot_enemy_list.clear()
        self.fire_enemy_rate = 0
        self.shot_list.clear()
        self.fire_rate = 0
        self.exploit_list.clear()
        self.score.text = '0'
        self.player.posx = self.width / 2.3
        self.player.posy = self.height / 7
        self.wait = 1.5
        self.time_bom = 1.5


    def on_draw(self):
        if not self.play:
            self.reload()
            self.clear()
            self.back_ground.draw()
            self.text.draw()
        else:
            self.clear()
            for space in self.space_list:
                space.draw()
            self.player.draw()
            for bul in self.shot_list:
                bul.draw()
            for mons in self.mons_draw:
                mons.draw()
            for sho in self.shot_enemy_list:
                sho.draw()
            self.exp_batch.draw()


    def update_shot_player(self, dt):
        for gun in self.shot_list:
            gun.update()
            gun.posy += 2000 * dt
            if gun.posy > 750:
                self.shot_list.remove(gun)


    def update_shot_enemy(self, dt):
        for shot in self.shot_enemy_list:
            shot.update()
            shot.posy -= 200 * dt
            if shot.posy < 0:
                self.shot_enemy_list.remove(shot)


    def bullet(self, dt):
        self.fire_enemy_rate -= dt
        if self.fire_enemy_rate <= 0:
            for enemy in self.mons_draw:
                if randint(0, 10) <= 2:
                    self.shot_enemy_list.append(gameObject(enemy.posx + 200, enemy.posy, pyglet.sprite.Sprite(self.shot_ene)))
            self.fire_enemy_rate += 1


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


    def update_enemy(self, dt):
        for x in self.mons_draw:
            x.update()
            x.posy -= 100 * dt
            x.posx += sin(x.posy/50) * randint(70, 100) * dt
            if x.posy < 0:
                self.mons_draw.remove(x)


    def hit(self, take, list):
        for obj in list:
            if obj.posx < take.posx + take.width and obj.posx + obj.width > take.posx \
                and obj.posy < take.posy + take.height and obj.height + obj.posy > take.posy:
                list.remove(obj)
                return True


    def shot_enemy(self, dt):
        for take in self.mons_draw:
            if self.hit(take, self.shot_list):
                self.exploit_list.append(pyglet.sprite.Sprite(self.exploit, x=take.posx, y=take.posy, batch=self.exp_batch))
                self.mons_draw.remove(take)
                self.score.text = str(int(self.score.text) + 1)
                self.exp_sound.play()


    def hit_player(self, dt):
        if self.hit(self.player, self.mons_draw) or self.hit(self.player, self.shot_enemy_list):
            self.exploit_list.append(pyglet.sprite.Sprite(self.exploit, x=self.player.posx, y=self.player.posy, batch=self.exp_batch))
            self.exp_sound.play()
            self.alive = False


    def wait_time(self, dt):
        self.wait -= 0.1
        if self.wait <= 0:
            self.play = False


    def update_exploit(self, dt):
        self.time_bom -= 0.1
        if self.time_bom <= 0:
            for exp in self.exploit_list:
                self.exploit_list.remove(exp)
                exp.delete()
            self.time_bom += 1.5


    def create_enenmy(self, dt):
        tmp = choice(self.mons_list)
        self.mons_draw.append(gameObject(randint(50, 1200), 700, pyglet.sprite.Sprite(tmp)))


    def update_space(self, dt):
        for space in self.space_list:
            space.update()
            space.posy -= 200 * dt
            if space.posy <= -1300:
                self.space_list.remove(space)
                self.space_list.append(gameObject(0, 760, pyglet.sprite.Sprite(self.space_img)))


    def update(self, dt):
        if self.play:
            self.update_shot_player(dt)
            self.update_shot_enemy(dt)
            if self.fire:
                self.fired(dt)
            self.bullet(dt)
            self.update_player(dt)
            self.update_space(dt)
            self.update_enemy(dt)
            if len(self.mons_draw) <= 5:
                self.create_enenmy(dt)
            self.shot_enemy(dt)
            self.hit_player(dt)
            self.update_exploit(dt)
        if not self.alive:
            self.update_exploit(dt)
            self.wait_time(dt)


if __name__ == "__main__":
    pyglet.options['audio'] = ('directsound', 'openal', 'pulse')
    window = gameWindow(1280, 720, "Matrix")
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
