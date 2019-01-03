# Global variables
import pyglet

window = pyglet.window.Window(800, 600)
label = pyglet.text.Label("0", font_size=36, y=300, x=400)

# Event callbacks
@window.event
def on_draw():
    window.clear()
    label.draw()


# Game loop (loop? Why loop?)
def game_loop(_):
    label = str(int(label) + 1)

pyglet.clock.schedule(game_loop)
pyglet.app.run()
