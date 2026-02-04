import arcade
import random

class giochino(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.character = None
        self.background = None
        self.lista_character = arcade.SpriteList()
        self.lista_background = arcade.SpriteList()
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.velocita = 5

        self.setup()

    def setup(self):

        self.wallpaper()
        
        self.character = arcade.Sprite("./assets/Colour1/NoOutline/120x80_gifs/__Idle.gif")
        self.character.center_x = 300
        self.character.center_y = 100
        self.character.scale = 2.0
        self.lista_character.append(self.character)

    def wallpaper(self):
        self.background=arcade.Sprite("./assets/background.png")
        self.background.center_x = 300
        self.background.center_y = 300
        self.background.scale = 1
        self.lista_background.append(self.background)

    def on_draw(self):
        self.clear()
        self.lista_background.draw()
        self.lista_character.draw()

    def on_update(self, delta_time):
        # Calcola movimento in base ai tasti premuti
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        self.character.center_x += change_x
        self.character.center_y += change_y

        if change_x < 0: 
            self.character.scale = (-2, 2)
        elif change_x > 0:
            self.character.scale = (2, 2)

        if self.character.center_x < 0:
            self.character.center_x = 0
        elif self.character.center_x > self.width:
            self.character.center_x = self.width

        if self.character.center_y < 0:
            self.character.center_y = 0
        elif self.character.center_y > self.height:
            self.character.center_y = self.height

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True

    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False




def main():    
    gioco = giochino(600, 600, "Giochino")    
    arcade.run()

if __name__ == '__main__':
    main()