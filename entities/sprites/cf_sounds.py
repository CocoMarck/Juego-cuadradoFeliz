import pygame
from controllers.cf_info import (
    dir_audio, data_CF
)

# Audio | Pasos | Golpes | Salto | Muertes
sounds_step = [
    pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-1.ogg') ),
    pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-2.ogg') ),
    pygame.mixer.Sound( dir_audio.joinpath('effects/steps/step-3.ogg') )
]
for step in sounds_step:
    step.set_volume(data_CF.volume)


sounds_hit = [
    pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-1.ogg') ),
    pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-2.ogg') ),
    pygame.mixer.Sound( dir_audio.joinpath('effects/hits/hit-3.ogg') )
]
for hit in sounds_hit:
    hit.set_volume(data_CF.volume)


sound_jump = pygame.mixer.Sound(
    dir_audio.joinpath('effects/jump.ogg')
)
sound_jump.set_volume(data_CF.volume)

sounds_dead = [
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/dead/dead-1.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/dead/dead-2.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/dead/dead-3.ogg' ) )
]
for dead in sounds_dead:
    dead.set_volume(data_CF.volume)


sounds_score = [
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/items/score-1.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/items/score-2.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/items/score-3.ogg' ) )
]
for score in sounds_score:
    score.set_volume(data_CF.volume)


sounds_shot = [
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/shooting/shot-1.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/shooting/shot-2.ogg' ) ),
    pygame.mixer.Sound( dir_audio.joinpath( 'effects/shooting/shot-3.ogg' ) )
]
for shot in sounds_shot:
    shot.set_volume( data_CF.volume )