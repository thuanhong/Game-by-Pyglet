import pyglet

def load_img(image):
    img =  pyglet.image.load('img/' + image)
    return img

class gameObject:
    def __init__(self, posx, posy, sprite = None):
        self.posx = posx
        self.posy = posy
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self):
        self.sprite.x = self.posx
        self.sprite.y = self.posy
