import pygame



layer_all_sprites = pygame.sprite.LayeredUpdates()
nocamera_back_sprites = pygame.sprite.Group()

player_objects = pygame.sprite.Group()
update_objects = pygame.sprite.Group()

solid_objects = pygame.sprite.Group()
ladder_objects = pygame.sprite.Group()
jumping_objects = pygame.sprite.Group()
moving_objects = pygame.sprite.Group()

damage_objects = pygame.sprite.Group()
limit_objects = pygame.sprite.Group()
level_objects = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()
climate_objects = pygame.sprite.Group()
score_objects = pygame.sprite.Group()
particle_objects = pygame.sprite.Group()

lighting_objects = pygame.sprite.Group()