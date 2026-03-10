from .scene import Scene
import pygame

SECOND_TO_MILLISECONDS = 1000

class Window:
    def __init__(self, window_size:list, fps:int, scene:Scene, title):
        self.title = title
        self.window_size = window_size
        self.fps = fps

        self.scene = scene
        self.layers = pygame.sprite.LayeredUpdates()

        # Init pygame
        self.window = None
        self.clock = None
        self.update_layers = None

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption( self.title )
        self.window = pygame.display.set_mode( self.window_size )

        self.clock = pygame.time.Clock()

    def run(self, datetime=True, show_fps=False):
        while self.scene.loop:
            dt = 1
            if datetime:
                dt = self.clock.tick(self.fps) / SECOND_TO_MILLISECONDS
            fps = self.clock.get_fps()
            if show_fps:
                print(fps)

            self.scene.handle_events(pygame.event.get())

            self.scene.update(dt, pygame.key.get_pressed())

            self.scene.render()

            self.window.blit(
                pygame.transform.scale(self.scene.render_surface, self.window_size), (0,0)
            )

            if self.update_layers != None:
                self.update_layers()
            for sprite in self.layers.sprites():
                self.window.blit( sprite.surf, sprite.rect )

            pygame.display.update()

        pygame.quit()
