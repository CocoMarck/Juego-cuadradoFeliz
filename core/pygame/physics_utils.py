import pygame

def collide_and_move(rect: pygame.Rect, moving_xy: list, solid_objects: pygame.sprite.Group):
    '''
    Mueve el y colisiona rect del objeto, solo con objetos solidos.

    Rect que colisiona con objetos solidos (otro rect). Se posiciona dependiendo del moving xy.
    Determinar colisión en: Dos pasos/bucles, por cada dimención.

    Solo colisionar abajo si es igual o mas grande el solido.

    - solid_objects: Puede ser sprite.Group, o una lista, da igual.
    '''
    collision_side = {
        'right': False,
        'left':  False,
        'top': False,
        'bottom': False
    }
    collided_at_x = False

    # X
    rect.x += moving_xy[0]
    for solid in solid_objects:
        if rect.height > solid.rect.height:
            # Evitar colision con solido; si es mas pequeño.
            continue
        if rect.colliderect( solid.rect ):
            if moving_xy[0] > 0:
                rect.right = solid.rect.left
                collision_side['right'] = True
            if moving_xy[0] < 0:
                rect.left = solid.rect.right
                collision_side['left'] = True
    collided_at_x = collision_side['right'] or collision_side['left']

    # Y
    rect.y += moving_xy[1]
    for solid in solid_objects:
        if rect.colliderect( solid.rect ):
            collide_bottom = rect.height >= solid.rect.height

            if moving_xy[1] > 0:
                rect.bottom = solid.rect.top
                collision_side['bottom'] = True

            if moving_xy[1] < 0 and collide_bottom:
                rect.top = solid.rect.bottom
                collision_side['top'] = True

    # Despues de XY
    ## Si colisiono en x
    if collided_at_x:
        ### Forzar posicionar arriba
        if rect.y < solid.rect.y -( rect.height*0.5 ):
            rect.bottom = solid.rect.top
            collision_side['bottom'] = True


    return collision_side
