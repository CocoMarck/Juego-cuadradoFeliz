from .character import Character

import pygame

class Player(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)

    def handle_input(self, keys=None):
        self.move_walk = keys[pygame.K_LSHIFT]
        self.move_left = keys[pygame.K_LEFT]
        self.move_right = keys[pygame.K_RIGHT]
        self.move_jump = keys[pygame.K_SPACE]
