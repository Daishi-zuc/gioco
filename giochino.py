import arcade
from animation import ANIMATION

class giochino(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.larghezza_livello = 1000000
        self.GRAVITY = 0.2
        self.PLAYER_JUMP_SPEED = 10
        self.velocita = 10

        self.pavimento_y = 0.2
        self.pavimento_x_start = 500
        self.pavimento_lunghezza = 200000

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.lista_character = arcade.SpriteList()
        self.lista_background = arcade.SpriteList()

        self.camera = arcade.camera.Camera2D()
        self.left_pressed = False
        self.right_pressed = False

        self.physics_engine = None
        self.setup()

    def setup(self):
        self.wallpaper()

        for x_pos in range(self.pavimento_x_start, self.pavimento_x_start + self.pavimento_lunghezza, 64):
            wall = arcade.SpriteSolidColor(64, 64, arcade.color.AMETHYST)
            wall.center_x = x_pos + 32
            wall.bottom = self.pavimento_y
            self.wall_list.append(wall)

        # Barriera sinistra
        barrier = arcade.SpriteSolidColor(64, 800, arcade.color.AMETHYST)
        barrier.center_x = self.pavimento_x_start - 32
        barrier.bottom = self.pavimento_y
        self.wall_list.append(barrier)

        self.character = ANIMATION()
        self.character.center_x = self.pavimento_x_start + 200
        self.character.bottom = self.pavimento_y + 64
        self.lista_character.append(self.character)

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
        self.lista_character.draw()

    def on_update(self, delta_time):
        self.character.change_x = 0
        self.character.update_animation(delta_time)

        if self.left_pressed and not self.right_pressed:
            self.character.change_x = -self.velocita
            self.character.scale = (-1, 1)
        elif self.right_pressed and not self.left_pressed:
            self.character.change_x = self.velocita
            self.character.scale = (1, 1)

        if self.physics_engine:
            self.physics_engine.update()

        # --- Logica delle animazioni ---         <-- stessa indentazione del resto
        if self.character.change_y > 0:
            self.character.imposta_animazione("salto")
        elif self.character.change_y < -1:
            self.character.imposta_animazione("caduta")
        elif self.character.change_x != 0:
            self.character.imposta_animazione("corsa")
        else:
            self.character.imposta_animazione("idle")

        # Telecamera
        if self.character.right > self.larghezza_livello:
            self.character.right = self.larghezza_livello
        cam_x = self.character.center_x
        cam_y = self.pavimento_y + (self.height / 2) * (1 / self.camera.zoom)
        self.camera.position = (cam_x, cam_y)

    def on_key_press(self, tasto, modificatori):
        match tasto:
            case arcade.key.UP | arcade.key.W | arcade.key.SPACE:
                if self.physics_engine.can_jump():
                    self.character.change_y = self.PLAYER_JUMP_SPEED
            case arcade.key.LEFT | arcade.key.A:
                self.left_pressed = True
            case arcade.key.RIGHT | arcade.key.D:
                self.right_pressed = True

    def on_key_release(self, tasto, modificatori):
        match tasto:
            case arcade.key.LEFT | arcade.key.A:
                self.left_pressed = False
            case arcade.key.RIGHT | arcade.key.D:
                self.right_pressed = False
            case arcade.key.N:
                self.camera.zoom += 0.1
            case arcade.key.M:
                self.camera.zoom -= 0.1

def main():
    gioco = giochino(800, 800, "Mago Platformer")
    arcade.run()

if __name__ == '__main__':
    main()