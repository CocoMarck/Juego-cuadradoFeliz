from .scene import Scene
import pygame

SECOND_TO_MILLISECONDS = 1000

class Window:
    def __init__(
        self, window_resolution:list, fps:int, scene:Scene, resize:bool=False, title:str="Window"
    ):
        self.title = title
        self.window_resolution = window_resolution
        self.fps = fps

        self.scene = scene
        self.layers = pygame.sprite.LayeredUpdates()
        self.resize = resize

        # Init pygame
        self.window = None
        self.clock = None
        self.update_layers = None # Funcion para actualizar leyers.

        #
        self.scroll_int = [0,0]

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption( self.title )
        if self.resize:
            self.window = pygame.display.set_mode( self.window_resolution, pygame.RESIZABLE )
        else:
            self.window = pygame.display.set_mode( self.window_resolution )

        self.clock = pygame.time.Clock()

    def get_window_resolution(self):
        if self.resize:
            return pygame.display.get_surface().get_size()
        else:
            return self.window_resolution

    def update_window_resolution(self):
        new_res = self.get_window_resolution()
        if self.window_resolution != new_res:
            self.window_resolution = new_res
            return True
        return False

    def run(self, datetime=True, show_fps=False):
        while self.scene.loop:
            dt = 1
            clock_tick_value = self.clock.tick(self.fps)
            if datetime:
                dt = clock_tick_value / SECOND_TO_MILLISECONDS
            fps = self.clock.get_fps()
            if show_fps:
                print(fps)

            self.scene.handle_events(pygame.event.get())

            self.scene.update( dt=dt, fps=fps, key_get_pressed=pygame.key.get_pressed() )

            self.scene.render()

            self.update_window_resolution()
            self.window.blit(
                pygame.transform.scale(self.scene.render_surface, self.window_resolution), (0,0)
            )

            if self.update_layers != None:
                self.update_layers()

            for sprite in self.layers.sprites():
                self.window.blit(
                    sprite.surf, (
                        sprite.rect.x -self.scroll_int[0], sprite.rect.y -self.scroll_int[1]
                    )
                )

            pygame.display.update()

        pygame.quit()
