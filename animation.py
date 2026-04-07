import os
from SpriteAnimato import SpriteAnimato

class ANIMATION(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=5)

        percorso_run = "assets/Colour2/Outline/120x80_PNGSheets/_Run.png"
        print("File esiste:", os.path.exists(percorso_run))
        print("Cartella corrente:", os.getcwd())

        self.aggiungi_animazione(
            nome="idle",
            percorso="assets/Colour2/NoOutline/120x80_PNGSheets/_Idle.png",
            frame_width=120, frame_height=80,
            num_frame=10, colonne=10,
            durata=0.8,
            loop=True,
            default=True
        )

        try:
            self.aggiungi_animazione(
                nome="corsa",
                percorso=percorso_run,
                frame_width=120, frame_height=80,
                num_frame=10, colonne=10,
                durata=0.6,
                loop=True
            )
            print("corsa caricata OK")
        except Exception as e:
            print("ERRORE corsa:", e)

        print("Animazioni caricate:", list(self.animazioni.keys()))