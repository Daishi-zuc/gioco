import arcade
from NemicoProiettile import NemicoProiettile

class NemicoBase(arcade.SpriteSolidColor):
    
    VELOCITA = 2
    VITA_MAX = 1
 
    def __init__(self, x, y, colore=arcade.color.RED, larghezza=48, altezza=64):
        super().__init__(larghezza, altezza, colore)
        self.center_x = x
        self.bottom = y
        self.vita = self.VITA_MAX
 
        
        self._kb_timer = 0.0
        self._kb_vx = 0.0
        self._kb_vy = 0.0
 
        
        self.lista_proiettili = None
 
    def subisci_danno(self, danno=1, knockback_x=0, knockback_y=4):
        self.vita -= danno
        self._kb_vx = knockback_x
        self._kb_vy = knockback_y
        self._kb_timer = 0.25          
 
    @property
    def morto(self):
        return self.vita <= 0
 
    def _applica_knockback(self, delta_time):
        if self._kb_timer > 0:
            self._kb_timer -= delta_time
            self.center_x += self._kb_vx
            self.center_y += self._kb_vy
            self._kb_vy -= 0.4          
            return True
        return False
 
    def update_nemico(self, delta_time, player, wall_list):
        """Override nelle sottoclassi."""
        pass
 
 
class NemicoPattuglia(NemicoBase):
    """
    Cammina avanti e indietro in un range fisso.
    Infligge danno al giocatore toccandolo.
    """
    VELOCITA = 2
    VITA_MAX = 1
    RANGE_PATTUGLIA = 150       
 
    def __init__(self, x, y):
        super().__init__(x, y, colore=arcade.color.ORANGE)
        self.vita = self.VITA_MAX
        self._spawn_x = x
        self.change_x = self.VELOCITA
 
    def update_nemico(self, delta_time, player, wall_list):
        if self._applica_knockback(delta_time):
            return
 
        self.center_x += self.change_x
 
        # Inverti direzione ai bordi del range
        if self.center_x > self._spawn_x + self.RANGE_PATTUGLIA:
            self.change_x = -self.VELOCITA
        elif self.center_x < self._spawn_x - self.RANGE_PATTUGLIA:
            self.change_x = self.VELOCITA
 
class NemicoInseguitore(NemicoBase):
    """
    Segue il giocatore se è abbastanza vicino.
    Spara un proiettile periodicamente.
    """
    VELOCITA = 1.4
    VITA_MAX = 3
    RAGGIO_VISTA = 350          
    COOLDOWN_SPARO = 2.5       
 
    def __init__(self, x, y):
        super().__init__(x, y, colore=arcade.color.DARK_RED, larghezza=52, altezza=68)
        self.vita = self.VITA_MAX
        self._timer_sparo = self.COOLDOWN_SPARO   
 
    def update_nemico(self, delta_time, player, wall_list):
        if self._applica_knockback(delta_time):
            return
 
        dist_x = player.center_x - self.center_x
        dist_y = player.center_y - self.center_y
        distanza = (dist_x ** 2 + dist_y ** 2) ** 0.5
 
        if distanza < self.RAGGIO_VISTA:
            
            if abs(dist_x) > 10:
                self.center_x += self.VELOCITA * (1 if dist_x > 0 else -1)
 
            # Sparo
            self._timer_sparo -= delta_time
            if self._timer_sparo <= 0:
                self._timer_sparo = self.COOLDOWN_SPARO
                self._spara(player)
 
    def _spara(self, player):
        if self.lista_proiettili is None:
            return
        proiettile = NemicoProiettile(
            self.center_x, self.center_y,
            player.center_x, player.center_y
        )
        self.lista_proiettili.append(proiettile)