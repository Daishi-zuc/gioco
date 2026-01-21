import arcade
import random

class giochino(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.background = None
        self.lista_background = arcade.SpriteList()
        self.setup()

    def setup(self):

        self.wallpaper()

    def wallpaper(self):
        self.background=arcade.Sprite("./assets/background.png")
        self.background.center_x = 300
        self.background.center_y = 300
        self.background.scale = 1
        self.lista_background.append(self.background)

    def on_draw(self):
        self.clear()
        self.lista_background.draw()

def main():    
    gioco = giochino(600, 600, "Giochino")    
    arcade.run()

if __name__ == '__main__':
    main()