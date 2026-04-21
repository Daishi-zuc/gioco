import arcade
from animation import ANIMATION
from Nemico import NemicoPattuglia, NemicoInseguitore

PLAYER_VITA_MAX = 100
IFRAMES = 1.5

SPAWN_INTERVALLO   = 4.0    # secondi tra uno spawn e il successivo
SPAWN_MAX_NEMICI   = 15     # max num nemici
SPAWN_DISTANZA_MIN = 600    # min pixel davanti/dietro al player
SPAWN_DISTANZA_MAX = 1200   # max pixel davanti/dietro al player

   
STATO_MENU     = "menu"
STATO_GIOCO    = "gioco"
STATO_GAMEOVER = "gameover"

class giochino(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.larghezza_livello = 100000
        self.GRAVITY = 0.2
        self.PLAYER_JUMP_SPEED = 8
        self.velocita = 5

        self.pavimento_y = 1
        self.pavimento_x_start = 500
        self.pavimento_lunghezza = 200000

        self.wall_list                = None
        self.lista_character          = None
        self.lista_background         = None
        self.lista_nemici             = None
        self.lista_proiettili_nemici  = None
        self.lista_proiettili_player  = None

        self.camera = arcade.camera.Camera2D()

        self.camera_ui = arcade.camera.Camera2D()

        self.left_pressed = False
        self.right_pressed = False

        self.physics_engine = None
        
        self.player_vita = PLAYER_VITA_MAX
        self._iframe_timer = 0.0

        self._attacco_attivo  = False   # True durante l'animazione di attacco
        self._attacco_fatto   = False   # True se il danno è già stato applicato
        self._spawn_timer     = SPAWN_INTERVALLO
 

        self._sound_attacco = None
        try:
            self._sound_attacco = arcade.load_sound("dragon-studio-sword-slice-393847.mp3")
        except Exception:
            pass  # asset mancante – il gioco va lo stesso perchè si
 
        self.stato = STATO_MENU
 
        self._bg_texture        = None
        self._bg_scala          = 1.0
        self._bg_larghezza_pezzo = 0
 
        self._precarica_sfondo()
        self.setup()
 
    def _precarica_sfondo(self):
        self._bg_texture         = arcade.load_texture("./assets/background.png")
        self._bg_scala           = self.height / self._bg_texture.height
        self._bg_larghezza_pezzo = self._bg_texture.width * self._bg_scala
 
    def wallpaper(self):
        """
        Ricostruisce la lista background coprendo tutto il livello.
        Parte dalla coordinata X della camera meno un pezzo di margine,
        così non ci sono mai zone nere ai lati.
        """
        self.lista_background = arcade.SpriteList()
        x_bg = 0.0
        fine  = self.larghezza_livello + self._bg_larghezza_pezzo
 
        while x_bg < fine:
            bg = arcade.Sprite(scale=self._bg_scala)
            bg.texture = self._bg_texture
            bg.left    = x_bg
            bg.bottom  = 0          # allineato al pavimento virtuale
            self.lista_background.append(bg)
            x_bg += self._bg_larghezza_pezzo    

    def setup(self):
        self.wall_list               = arcade.SpriteList(use_spatial_hash=True)
        self.lista_character         = arcade.SpriteList()
        self.lista_nemici            = arcade.SpriteList()
        self.lista_proiettili_nemici = arcade.SpriteList()
        self.lista_proiettili_player = arcade.SpriteList()
 
        self.player_vita   = PLAYER_VITA_MAX
        self._iframe_timer = 0.0
        self._attacco_attivo = False
        self._attacco_fatto  = False
        self.left_pressed    = False
        self.right_pressed   = False
 
        self.wallpaper()
        self._crea_pavimento()
        self._crea_player()
        self._spawn_nemici()
 
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.character,
            walls=self.wall_list,
            gravity_constant=self.GRAVITY
        )

    def _crea_pavimento(self):
        for x_pos in range(self.pavimento_x_start,
                           self.pavimento_x_start + self.pavimento_lunghezza, 64):
            wall = arcade.SpriteSolidColor(64, 64, arcade.color.AMETHYST)
            wall.center_x = x_pos + 32
            wall.bottom = self.pavimento_y
            self.wall_list.append(wall)

        # Barriera sinistra
        barrier = arcade.SpriteSolidColor(64, 800, arcade.color.AMETHYST)
        barrier.center_x = self.pavimento_x_start - 32
        barrier.bottom = self.pavimento_y
        self.wall_list.append(barrier)

    def _crea_player(self):
        self.character = ANIMATION()
        self.character.center_x = self.pavimento_x_start + 200
        self.character.bottom = self.pavimento_y + 64
        self.lista_character.append(self.character)    

    def _spawn_nemici(self):
        
        import random
        for i in range(3):
            x = self.pavimento_x_start + 400 + i * 300
            y = self.pavimento_y + 64
            n = NemicoPattuglia(x, y) if i % 2 == 0 else NemicoInseguitore(x, y)
            n.lista_proiettili = self.lista_proiettili_nemici
            self.lista_nemici.append(n)
 
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.character,
            walls=self.wall_list,
            gravity_constant=self.GRAVITY
        )

    def _spawn_nemico_casuale(self):

        import random
        if len(self.lista_nemici) >= SPAWN_MAX_NEMICI:
            return
 
        # Scegli un lato (davanti o dietro) e una distanza casuale
        direzione = random.choice([-1, 1])
        dist = random.randint(SPAWN_DISTANZA_MIN, SPAWN_DISTANZA_MAX)
        x = self.character.center_x + direzione * dist
 
        # Clamp dentro i limiti del livello
        x = max(self.pavimento_x_start + 64, min(x, self.larghezza_livello - 64))
        y = self.pavimento_y + 64
 
        tipo = random.choice([NemicoPattuglia, NemicoInseguitore])
        n = tipo(x, y)
        n.lista_proiettili = self.lista_proiettili_nemici
        self.lista_nemici.append(n)

    def on_draw(self):
        self.clear()

        if self.stato == STATO_MENU:
            self.camera_ui.use()
            self._disegna_menu()
        elif self.stato == STATO_GIOCO:
            self._disegna_gioco()
        elif self.stato == STATO_GAMEOVER:
            self._disegna_gioco() 
            self.camera_ui.use()
                     
            self._disegna_gameover()
            
        
    def _disegna_gioco(self):
        self.camera.use()
        self.lista_background.draw()
        self.lista_nemici.draw()
        self.lista_proiettili_nemici.draw()
        self.lista_proiettili_player.draw()
        self.lista_character.draw()

        self.camera_ui.use()
        self._disegna_vita()

    def _disegna_vita(self):

        x0, y0 = 20, self.height - 12
        larghezza_barra = 150
        altezza_barra = 18

        # sfondo rosso
        arcade.draw_lrbt_rectangle_filled(
            x0, x0 + larghezza_barra,
            y0 - altezza_barra, y0,
            arcade.color.DARK_RED
        )
        # vita attuale
        fill = larghezza_barra * (self.player_vita / PLAYER_VITA_MAX)
        if fill > 0:
            arcade.draw_lrbt_rectangle_filled(
                x0, x0 + fill,
                y0 - altezza_barra, y0,
                arcade.color.BRIGHT_GREEN
            )
        arcade.draw_lrbt_rectangle_outline(
            x0, x0 + larghezza_barra,
            y0 - altezza_barra, y0,
            arcade.color.WHITE, 2
        )
        arcade.draw_text(
            f"HP  {self.player_vita}/{PLAYER_VITA_MAX}",
            x0 + 4, y0 - altezza_barra + 2,
            arcade.color.WHITE, 12, bold=True
        )

    def _disegna_menu(self):
        """Schermata principale con titolo e pulsante Play."""

        arcade.draw_lrbt_rectangle_filled(
            0, self.width, 0, self.height,
            (10, 10, 30, 240)
        )
 
        cx = self.width  / 2
        cy = self.height / 2
 
        # Titolo
        arcade.draw_text(
            "CAVALIERE PLATFORMER",
            cx, cy + 120,
            arcade.color.GOLD, 48,
            anchor_x="center", anchor_y="center",
            bold=True
        )
 
        # Sottotitolo
        arcade.draw_text(
            "progetto per scuola",
            cx, cy + 60,
            arcade.color.LIGHT_BLUE, 20,
            anchor_x="center", anchor_y="center"
        )
 
        bw, bh = 200, 55
        bx, by = cx - bw / 2, cy - 20
        arcade.draw_lrbt_rectangle_filled(bx, bx + bw, by, by + bh, arcade.color.DARK_GREEN)
        arcade.draw_lrbt_rectangle_outline(bx, bx + bw, by, by + bh, arcade.color.GREEN, 3)
        arcade.draw_text(
            "▶  PLAY",
            cx, by + bh / 2,
            arcade.color.WHITE, 26,
            anchor_x="center", anchor_y="center",
            bold=True
        )
 
        arcade.draw_text(
            "Premi INVIO o clicca PLAY",
            cx, by - 30,
            arcade.color.GRAY, 14,
            anchor_x="center", anchor_y="center"
        )
 
        # Controlli
        controlli = (
            "← → / A D  :  muoviti       ↑ / W / SPAZIO  :  salta\n"
            "Z  :  attacca       N / M  :  zoom +/-"
        )
        arcade.draw_text(
            controlli,
            cx, 60,
            arcade.color.LIGHT_GRAY, 13,
            anchor_x="center", anchor_y="center",
            multiline=True, width=600
        )
 
        self._play_btn = arcade.LRBT(bx, bx + bw, by, by + bh)   

    def _disegna_gameover(self):
        """Overlay semitrasparente Game Over."""
        arcade.draw_lrbt_rectangle_filled(
            0, self.width, 0, self.height,
            (0, 0, 0, 180)
        )
 
        cx = self.width  / 2
        cy = self.height / 2
 
        arcade.draw_text(
            "GAME OVER",
            cx, cy + 60,
            arcade.color.RED, 64,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            "La tua avventura è finita…",
            cx, cy,
            arcade.color.LIGHT_GRAY, 22,
            anchor_x="center", anchor_y="center"
        )
 
        # Pulsanti RIGIOCA / MENU
        bw, bh = 180, 50
 
        # -- RIGIOCA
        bx_r = cx - bw - 20
        by_r = cy - 80
        arcade.draw_lrbt_rectangle_filled(bx_r, bx_r + bw, by_r, by_r + bh, arcade.color.DARK_GREEN)
        arcade.draw_lrbt_rectangle_outline(bx_r, bx_r + bw, by_r, by_r + bh, arcade.color.GREEN, 2)
        arcade.draw_text(
            "↺  RIGIOCA",
            bx_r + bw / 2, by_r + bh / 2,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
 
        # -- MENU
        bx_m = cx + 20
        by_m = cy - 80
        arcade.draw_lrbt_rectangle_filled(bx_m, bx_m + bw, by_m, by_m + bh, (50, 50, 120))
        arcade.draw_lrbt_rectangle_outline(bx_m, bx_m + bw, by_m, by_m + bh, arcade.color.LIGHT_BLUE, 2)
        arcade.draw_text(
            "⌂  MENU",
            bx_m + bw / 2, by_m + bh / 2,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
 
        arcade.draw_text(
            "R  =  rigioca       ESC  =  menu",
            cx, by_r - 28,
            arcade.color.GRAY, 14,
            anchor_x="center", anchor_y="center"
        )
 
        # Salva rect pulsanti per click
        self._rigioca_btn = arcade.LRBT(bx_r, bx_r + bw, by_r, by_r + bh)
        self._menu_btn    = arcade.LRBT(bx_m, bx_m + bw, by_m, by_m + bh)     

        
    def on_update(self, delta_time):

        if self.stato != STATO_GIOCO:   
            return
    
        self.character.change_x = 0
        self.character.update_animation(delta_time)


        if not self._attacco_attivo:
            if self.left_pressed and not self.right_pressed:
                self.character.change_x = -self.velocita
                self.character.scale = (-1, 1)
            elif self.right_pressed and not self.left_pressed:
                self.character.change_x = self.velocita
                self.character.scale = (1, 1)

            else:
                self.character.change_x = 0   # fermo durante l'attacco

            if self.physics_engine:
                self.physics_engine.update()    

        if self.physics_engine:
            self.physics_engine.update()
        if not self._attacco_attivo:
            if self.character.change_y > 0:
                self.character.imposta_animazione("jump")
            elif self.character.change_y < -1:
                self.character.imposta_animazione("fall")
            elif self.character.change_x != 0:
                self.character.imposta_animazione("run")
            else:
                self.character.imposta_animazione("idle")

        if self._attacco_attivo and self.character.animazione_finita("attack"):
            self._attacco_attivo = False
            self._attacco_fatto  = False
            
        #── Danno in mischia (durante attacco) ──       
        if self._attacco_attivo and not self._attacco_fatto:
            portata = 80
            for nemico in list(self.lista_nemici):
                dist = abs(nemico.center_x - self.character.center_x)
                if dist <= portata:
                    if hasattr(nemico, 'subisci_danno'):
                        nemico.subisci_danno(1)
                    else:
                        nemico.morto = True
            self._attacco_fatto = True

        # ── Proiettili player ─────────────────────────────────────────────
        for p in list(self.lista_proiettili_player):
            p.update(delta_time)
            if arcade.check_for_collision_with_list(p, self.wall_list):
                p.remove_from_sprite_lists()
                continue
            for nemico in list(self.lista_nemici):
                if arcade.check_for_collision(p, nemico):
                    p.remove_from_sprite_lists()
                    if hasattr(nemico, 'subisci_danno'):
                        nemico.subisci_danno(1)
                    else:
                        nemico.morto = True
                    break    

        # ── Spawn continuo nemici ─────────────────────────────────────────
        self._spawn_timer -= delta_time
        if self._spawn_timer <= 0:
            self._spawn_timer = SPAWN_INTERVALLO
            self._spawn_nemico_casuale()         

        # --- Nemici ---    

        for nemico in self.lista_nemici:
            nemico.update_nemico(delta_time, self.character, self.wall_list)
 
        for nemico in list(self.lista_nemici):
            if nemico.morto:
                nemico.remove_from_sprite_lists()
 
        # --- Proiettili nemici ---
        for p in list(self.lista_proiettili_nemici):
            p.update(delta_time)
            if arcade.check_for_collision_with_list(p, self.wall_list):
                p.remove_from_sprite_lists()
 
        # ── Danni al player ───────────────────────────────────────────────
        self._iframe_timer = max(0.0, self._iframe_timer - delta_time)
        if self._iframe_timer == 0:
            colpiti = arcade.check_for_collision_with_list(
                self.character, self.lista_nemici
            )
            if colpiti:
                self._subisci_danno(1)
 
        if self._iframe_timer == 0:
            colpiti_p = arcade.check_for_collision_with_list(
                self.character, self.lista_proiettili_nemici
            )
            for p in colpiti_p:
                p.remove_from_sprite_lists()
                self._subisci_danno(1)
                break   

        # Telecamera
        if self.character.right > self.larghezza_livello:
            self.character.right = self.larghezza_livello
 
        cam_x = self.character.center_x
        
        cam_y = self.pavimento_y + (self.height / 2) * (1 / self.camera.zoom)
        self.camera.position = (cam_x, cam_y)   


    def on_key_press(self, tasto : arcade.key, modificatori):

        if self.stato == STATO_MENU:
            if tasto == arcade.key.RETURN or tasto == arcade.key.ENTER:
                self._avvia_gioco()
            return
 
        # ── GAME OVER ─────────────────────────────────────────────────────
        if self.stato == STATO_GAMEOVER:
            if tasto == arcade.key.R:
                self._avvia_gioco()
            elif tasto == arcade.key.ESCAPE:
                self.stato = STATO_MENU
            return
        
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
            case arcade.key.Z:              
                self._esegui_attacco()    

    # INPUT – MOUSE
    # ══════════════════════════════════════════════════════════════════════
 
    def on_mouse_press(self, x, y, button, modifiers):
        if self.stato == STATO_MENU:
            if hasattr(self, '_play_btn'):
                b = self._play_btn
                if b.left <= x <= b.right and b.bottom <= y <= b.top:
                    self._avvia_gioco()
 
        elif self.stato == STATO_GAMEOVER:
            if hasattr(self, '_rigioca_btn'):
                b = self._rigioca_btn
                if b.left <= x <= b.right and b.bottom <= y <= b.top:
                    self._avvia_gioco()
            if hasattr(self, '_menu_btn'):
                b = self._menu_btn
                if b.left <= x <= b.right and b.bottom <= y <= b.top:
                    self.stato = STATO_MENU

    def _avvia_gioco(self):
        self.stato = STATO_GIOCO
        self.setup()
 
    def _esegui_attacco(self):
        if self._attacco_attivo:
            return
        self._attacco_attivo = True
        self._attacco_fatto  = False
        self.character.imposta_animazione("attack")
        if self._sound_attacco:
            arcade.play_sound(self._sound_attacco)
 
    def _subisci_danno(self, danno):
        self.player_vita  -= danno
        self._iframe_timer = IFRAMES
        if self.player_vita <= 0:
            self.player_vita = 0
            self.stato = STATO_GAMEOVER                            


def main():
    gioco = giochino(800, 800, "Cavaliere Platformer")
    arcade.run()

if __name__ == "__main__":
    main()