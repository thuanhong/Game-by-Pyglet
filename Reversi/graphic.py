import pyglet
from tmp import *
from pyglet.window import mouse, key


class chess:
    def __init__(self, x, y, img = None):
        self.x = x
        self.y = y
        if img != None:
            self.sprite = pyglet.sprite.Sprite(img)
            self.sprite.x = self.x
            self.sprite.y = self.y


    def draw(self):
        self.sprite.draw()


class gameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         #  import picture
         self.white = pyglet.image.load('img/white.png')
         self.black = pyglet.image.load('img/black.png')
         self.mark = pyglet.image.load('img/mark.png')
         self.chess = pyglet.image.load('img/chess.gif')

         self.chess_board = chess(530, 230, self.chess)
         self.frame_rate = 1/60.0

         self.board = [['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', 'W', 'B', '.', '.', '.'],
                      ['.', '.', '.', 'B', 'W', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', '.', '.', '.', '.', '.', '.']]
         self.label = pyglet.text.Label("Player White",font_size=40 , y=650, x=50)
         self.text = pyglet.text.Label("Cannot play, press LEFT to play continue", font_size=30, y=650, x=400)

         self.can_play = 2 # both 2 player can play
         self.enemy = 'B'
         self.mark_list = [] # contain valid choice (X on chess board)
         self.tmp_list = print_valid_choice(self.board, self.enemy)
         for x in self.tmp_list:
             self.mark_list.append(chess(int(x/10) * self.black.width + 530 , int(x%10) * self.black.width + 230, self.mark))


    def reload(self): # reload when start a new game
        self.can_play = 2
        self.mark_list.clear()
        self.tmp_list.clear()
        self.enemy = 'B'
        self.board = [['.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', 'W', 'B', '.', '.', '.'],
                     ['.', '.', '.', 'B', 'W', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.']]

    def on_draw(self):
        self.clear()
        self.chess_board.draw()

        for x in range(8): # output chess board out display
            for y in range(8):
                if self.board[x][y] != '.':
                    if self.board[x][y] == 'B':
                        chess(x * self.black.width + 530, y * self.black.width + 230, self.black).draw()
                    else:
                        chess(x * self.black.width + 530, y * self.black.width + 230, self.white).draw()

        self.label.draw()
        if self.mark_list == []:
            self.text.draw()
        else:
            for cross in self.mark_list:
                cross.draw()

        if self.can_play == 0 or checkend(self.board): # when game over
            tmp = count(self.board)
            self.result = pyglet.text.Label("Result | W : " + str(int(tmp/100)) + "| B : " + str(int(tmp%100))
                                                  + ", Click E to exit, press R to reload",
                                                  font_size=30, y=150, x=100)
            self.result.draw()


    def hit(self, take, list): # return the move if click hit mark (X)
        if list == []:
            return 100
        for mark in list:
            if take[0] in range(mark.x, mark.x + 38) and take[1] in range(mark.y, mark.y + 38):
                for x in self.tmp_list:
                    if int(x/10) * self.black.width + 530 == mark.x and int(x%10) * self.black.width + 230 == mark.y:
                        return x
        return -1

    def on_key_press(self, symbol, modifiers): # take mouse event from keyboard
        if symbol == key.R:
            self.reload()
        if symbol == key.E:
            pyglet.app.exit()


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            temp = self.hit([x, y], self.mark_list)
            if temp != -1:
                self.list = main(self.board, self.enemy, temp, self.can_play)
                self.enemy = self.list[0]
                self.can_play = self.list[1]
                self.mark_list.clear()
                self.tmp_list = print_valid_choice(self.board, self.enemy)
                self.text.draw()
                self.label.text = 'Player Black' if self.enemy == 'W' else 'Player White'
                for x in self.tmp_list: # create an new mark list
                    self.mark_list.append(chess(int(x/10) * self.black.width + 530 , int(x%10) * self.black.width + 230, self.mark))

    def update(self, dt):
        pass

if __name__ == '__main__':
    window = gameWindow(1280, 720, 'Game Demo')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
