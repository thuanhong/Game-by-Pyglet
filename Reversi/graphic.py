import pyglet
from tmp import *
from pyglet.window import mouse


class chess:
    def __init__(self, x, y, img = None):
        self.x = x
        self.y = y
        if img != None:
            img.anchor_x = img.width // 2
            img.anchor_y = img.width // 2
            self.sprite = pyglet.sprite.Sprite(img)
            self.sprite.x = self.x
            self.sprite.y = self.y


    def draw(self):
        self.sprite.draw()


class gameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.white = pyglet.image.load('img/white.png')
         self.black = pyglet.image.load('img/black.png')
         self.mark = pyglet.image.load('img/mark.png')
         self.frame_rate = 1/60.0

         self.board = [['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', 'W', 'B', '.', '.', '.'],
                      ['.', '.', '.', 'B', 'W', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.']]
         self.enemy = 'B'
         self.mark_list = []
         self.tmp_list = print_valid_choice(self.board, self.enemy)
         for x in self.tmp_list:
             self.mark_list.append(chess(int(x/10) * self.black.width + 550 , int(x%10) * self.black.width + 290, self.mark))

    def on_draw(self):
        self.clear()
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != '.':
                    if self.board[x][y] == 'B':
                        chess(x * self.black.width + 550, y * self.black.width + 290, self.black).draw()
                    else:
                        chess(x * self.black.width + 550, y * self.black.width + 290, self.white).draw()

        for cross in self.mark_list:
            cross.draw()

    def hit(self, take, list):
        for mark in list:
            if take[0] in range(mark.x, mark.x + 20) and take[1] in range(mark.y, mark.y + 20):
                for x in self.tmp_list:
                    if int(x/10) * self.black.width + 550 == mark.x:
                        return x
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            temp = self.hit([x, y], self.mark_list)
            if temp != False:
                main(self.board, self.enemy, temp)
                print(self.enemy)

    def update(self, dt):
        self.on_draw()



if __name__ == '__main__':
    window = gameWindow(1280, 720, 'Game Demo')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
