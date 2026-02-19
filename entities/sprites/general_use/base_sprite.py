import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Identificador de sprite
        self.identifer = "base-sprite"

        # Variables de Superficie y collider
        self.position = [0,0]
        self.transparency = 255
        self.angle = 0

        # Daño
        self.damage = 0
        self.damage_activated = True

        # Volumen
        self.volume = 0
