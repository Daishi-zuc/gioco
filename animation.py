from SpriteAnimato import SpriteAnimato
class ANIMATION(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=0.6)
        
        self.aggiungi_animazione(
            nome="idle",
            percorso="assets/Colour2/NoOutline/120x80_PNGSheets/_Idle.png",
            frame_width=120, frame_height=80,
            num_frame=10, colonne=10,
            durata=0.8,
            loop=True,
            default=True
        )

        self.aggiungi_animazione(
            nome="run",
            percorso="assets/Colour2/Outline/120x80_PNGSheets/_Run.png",
            frame_width=120, frame_height=80,
            num_frame=10, colonne=10,
            durata=0.6,
            loop=True
        )

        self.aggiungi_animazione(
            nome="fall",
            percorso="assets/Colour2/NoOutline/120x80_PNGSheets/_Fall.png", 
            frame_width=120, frame_height=80,
            num_frame=3, colonne=3,
            durata=0.6,
            loop=False
        )

        self.aggiungi_animazione(
            nome="jump",
            percorso="assets/Colour2/NoOutline/120x80_PNGSheets/_Jump.png", 
            frame_width=120, frame_height=80,
            num_frame=3, colonne=3,
            durata=0.6,
            loop=False
        )