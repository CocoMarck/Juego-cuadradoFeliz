import pygame

def surface_with_background( size:tuple, color='black' ):
    max_size = max(size)
    surf = pygame.Surface( (max_size, max_size), pygame.SRCALPHA )
    figure = pygame.Surface( size )
    figure.fill( color )

    position = [0,0]
    if max_size != size[0]:
        position[0] = max_size*0.5 -size[0]*0.5
    if max_size != size[1]:
        position[1] = max_size*0.5 -size[1]*0.5

    surf.blit( figure, position )

    return surf
