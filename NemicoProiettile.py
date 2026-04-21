import arcade
import math
 
 
class NemicoProiettile(arcade.SpriteSolidColor):
    """
    Proiettile sparato da un nemico verso il giocatore.
    Placeholder colorato; sostituibile con una texture.
    """
    VELOCITA = 5
    DURATA_MAX = 3.0        # secondi prima di sparire automaticamente
 
    def __init__(self, x, y, target_x, target_y):
        super().__init__(10, 10, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
 
        # Calcola direzione normalizzata verso il target
        dx = target_x - x
        dy = target_y - y
        lunghezza = math.hypot(dx, dy) or 1
        self.change_x = (dx / lunghezza) * self.VELOCITA
        self.change_y = (dy / lunghezza) * self.VELOCITA
 
        self._timer = 0.0
 
    def update(self, delta_time=1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self._timer += delta_time
        if self._timer >= self.DURATA_MAX:
            self.remove_from_sprite_lists()
 