import pygame

from .game_object import GameObject

class StickySprite(GameObject):
    def __init__(self, *args, game_object: GameObject, center=False, **kwargs):
        super().__init__( *args, **kwargs)

        self.game_object = game_object
        self.center = center

    def stick(self, offset_xy: [int,int] = [0,0], multiplier=[1,1]):
        if self.center:
            xy = self.game_object.rect.center
        else:
            xy = self.game_object.rect.topleft
        position = [
            (xy[0] + offset_xy[0])*multiplier[0], (xy[1] + offset_xy[1])*multiplier[1]
        ]

        if self.center:
            self.rect.center = position
        else:
            self.rect.topleft = position
