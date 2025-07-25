# Contador jugador en el aire, basado en la resolucion de pantalla de juego.
air_count_based_on_resolution = round(1920/data_CF.disp[0])
if air_count_based_on_resolution < 0:
    air_count_based_on_resolution = 0
elif air_count_based_on_resolution > 10:
    air_count_based_on_resolution = 10


class Player_newver(pygame.sprite.Sprite):
    def __init__( self, position=[0, 0], size=data_CF.pixel_space, show_collide=False, show_sprite=True, color_sprite=[153,252,152] ):
        super().__init__()
        
        # Collider
        size = [size//2, size]
        self.surf = pygame.Surface( size, pygame.SRCALPHA )
        self.surf.fill( generic_colors(color='green', transparency=255 ) )
        
        self.rect = self.surf.get_rect( topleft=position )
        self.rect.x += size[0]//2
        layer_all_sprites.add(self, layer=3)
        player_objects.add(self) # Para que la lluvia colisione
        

        # Movimiento
        self.not_move = False
        self.moving_xy = [0,0]
        self.hp = 100
        self.speed = size[1]*0.5
        
        self.gravity_power = size[1]*0.025
        self.gravity_limit = size[1]*0.75
        self.gravity_current = -self.gravity_power # Para que empieze en 0 poder de gravedad
        self.air_count = 8 # Para que inicie en caida
        
        self.move_jump = False
        self.jump_power = size[1]*0.5
        self.jump_count = 0
        self.jump_max_height = size[1]*4
        self.jumping = False

        # Movimiento | Sonido contador de pasos
        self.step_count = 0
        self.state_collide_in_floor = 'wait'
        
        # Movimiento | Teclas de movimiento y variables de movimiento
        self.pressed_jump       = pygame.K_SPACE
        self.pressed_left       = pygame.K_LEFT
        self.pressed_right      = pygame.K_RIGHT
        self.pressed_up         = pygame.K_UP
        self.pressed_down       = pygame.K_DOWN
        self.pressed_walk       = pygame.K_LSHIFT
        
        
    def get_speed( self, multipler=1 ):
        return self.speed*multipler
    
    
    def move(self):
        # Movimiento | Funcion que se encarga de saber si se han percionado las Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()

        self.move_left = pressed_keys[self.pressed_left]
        self.move_right = pressed_keys[self.pressed_right]
        self.move_up = pressed_keys[self.pressed_up]
        self.move_down = pressed_keys[self.pressed_down]
        self.walking = pressed_keys[self.pressed_walk]
        

    def jump(self):
        self.move_jump = True
    
    
    def update(self):
        # Movimiento | Actualizar movimiento del jugador
        
        
        # HP | Determinar si el jugador esta vivo o muerto
        if self.hp <= 0:
            self.dead = True
            self.not_move = True
            self.jump_count = self.jump_max_height
            self.gravity_current = 0
        else:
            self.not_move = False
            self.dead = False

        # Dejar de moverse
        if self.not_move == True:
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.move_jump = False
            self.walking = False
        



        # Detectar si esta en el piso o no
        # Esto se determina dependiendo la cantidad de frames en las que el jugador esta en el aire
        # Entre mas alto, major funciona en res bajas, y entre mas bajo mejor funciona en res altas.
        if self.air_count <= air_count_based_on_resolution:
            fall = False
        else:
            fall = True
        
        
        
        
        # Determinar velocidad del jugador
        if self.walking == True:
            speed = self.get_speed(multipler=0.5)
        else:
            speed = self.get_speed()
        
        
        
        # Mover el jugador
        self.moving_xy = [0,0]
        if self.move_left == True:  self.moving_xy[0] -= speed
        if self.move_right == True: self.moving_xy[0] += speed
        if self.move_jump == True:
            if fall == False:
                self.jumping = True
                self.move_jump = False
        
        
        
        
        # Gravedad | Caida
        self.moving_xy[1] += self.gravity_current
        
        if self.gravity_current < self.gravity_limit:
            self.gravity_current += self.gravity_power
        else:
            self.gravity_current = self.gravity_limit   
        
        
        
        
        # Salto
        if self.jumping == True:
            self.gravity_current, self.moving_xy[1] = 0, 0
            self.jump_count += self.jump_power
            if self.jump_count <= self.jump_max_height:
                self.moving_xy[1] -= self.jump_power
                self.jumping = True
            else: self.jumping = False

        else: self.jump_count = 0
        
        
        
        
        # Colisiones | Solidos
        collided_side = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        if collided_side == 'bottom':
            self.gravity_current = 0
            self.air_count = 0
        else:
            self.air_count += 1
        
        if collided_side == 'top':
            self.gravity_current = 0
            
            self.jumping = False
            self.jump_count = 0
