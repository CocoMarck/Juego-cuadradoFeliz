from core.pygame.audio.play_background_sound import PlayBackgroundSounds
from core.pygame.audio.background_sound import BackgroundSound
from core.pygame.cf_util import all_music

# pygame
import time
import pygame, sys, os, random
pygame.init()

# Fotogramas del juego
clock = pygame.time.Clock()

# Titulo del juego
pygame.display.set_caption("background")

window = pygame.display.set_mode( (320,320) )

# Sonido
sounds = []
for key in ["bateria-songini", "808-test", "cf-end-theme"]:#all_music.keys():
    sounds.append(
        BackgroundSound( source=all_music[key], music=True, volume=1.0, repetitions=1 )
    )
play_background_sounds = PlayBackgroundSounds(
    sounds=sounds, mixer=pygame.mixer.music, play_music_sound=True, play_simple_sound=False
)

# Loop
exec_game = True
while exec_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exec_game = False

    play_background_sounds.select_background_sound( mode="random" )

    # Fin
    clock.tick(30)
    pygame.display.update()

pygame.quit()
