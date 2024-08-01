import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.rect.y -= 20
        if self.rect.y < 0:
            self.kill()

    def update(self):
        self.move()