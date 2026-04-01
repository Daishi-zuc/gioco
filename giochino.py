import arcade
from animation import ANIMATION
class giochino(arcade.Window):
            def __init__(self, larghezza, altezza, titolo):
                super().__init__(larghezza, altezza, titolo)

                # Variabili del mondo
                self.larghezza_livello = 1000000
                self.GRAVITY = 0.2
                self.PLAYER_JUMP_SPEED = 10
                self.velocita = 10

                # Liste Sprite
                
                self.wall_list = arcade.SpriteList(use_spatial_hash=True)
                self.lista_character = arcade.SpriteList()
                self.lista_background = arcade.SpriteList()
                
                # Camera e controlli
                self.camera = arcade.camera.Camera2D() 
                self.left_pressed = False
                self.right_pressed = False
                
                self.physics_engine = None

                self.setup()

            def setup(self):
                # 1. Sfondo
                self.wallpaper()

                # 2. Pavimento
                for x_pos in range(0, self.larghezza_livello, 64):
                    wall = arcade.SpriteSolidColor(64, 64, arcade.color.AMETHYST)
                    wall.center_x = x_pos + 32  
                    wall.bottom = 0
                    self.wall_list.append(wall)
                
                # 3. Personaggio
                self.character = ANIMATION()
                self.character.center_x = 300
                self.character.center_y = 150
                self.lista_character.append(self.character)

                # 4. physics engine
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.character, 
                    walls=self.wall_list, 
                    gravity_constant=self.GRAVITY
                )

            def wallpaper(self):
                temp_bg = arcade.Sprite("./assets/background.png")
                scala_adattata = self.height / temp_bg.height
                larghezza_pezzo = temp_bg.width * scala_adattata

                x_bg = 0
                while x_bg < self.larghezza_livello:
                    bg = arcade.Sprite("./assets/background.png")
                    bg.height = self.height
                    bg.width = larghezza_pezzo
                    bg.left = x_bg
                    bg.bottom = 0
                    self.lista_background.append(bg)
                    x_bg += larghezza_pezzo

            def on_draw(self):
                self.clear()
                self.camera.use()
                
                self.lista_background.draw()
                # self.wall_list.draw()
                self.lista_character.draw()

            def on_update(self, delta_time):

                self.character.change_x = 0

                self.character.update_animation(delta_time)
                
                if self.left_pressed and not self.right_pressed:
                    self.character.change_x = -self.velocita
                    self.character.scale = (-0.2, 0.2)
                elif self.right_pressed and not self.left_pressed:
                    self.character.change_x = self.velocita
                    self.character.scale = (0.2, 0.2)

                if self.physics_engine:
                    self.physics_engine.update()

                if self.character.left < 0:
                    self.character.left = 0
                elif self.character.right > self.larghezza_livello:
                    self.character.right = self.larghezza_livello

                self.camera.position = self.character.position

            def on_key_press(self, tasto, modificatori):
                if tasto in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
                    if self.physics_engine.can_jump():
                        self.character.change_y = self.PLAYER_JUMP_SPEED
                elif tasto in (arcade.key.LEFT, arcade.key.A):
                    self.left_pressed = True
                elif tasto in (arcade.key.RIGHT, arcade.key.D):
                    self.right_pressed = True

            def on_key_release(self, tasto, modificatori):
                if tasto in (arcade.key.LEFT, arcade.key.A):
                    self.left_pressed = False
                elif tasto in (arcade.key.RIGHT, arcade.key.D):
                    self.right_pressed = False

def main():    
            gioco = giochino(800, 800, "Mago Platformer")    
            arcade.run()

if __name__ == '__main__':
            main()