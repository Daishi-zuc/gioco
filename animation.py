from SpriteAnimato import SpriteAnimato

class ANIMATION(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=0.2)
        self.aggiungi_animazione(
            nome="idle",
            percorso="assets/Colour2/NoOutline/120x80_PNGSheets/_Idle.png",
            frame_width=120, frame_height=80,
            num_frame=10, colonne=10,
            durata=0.8,
            loop=True,
            default=True
        )