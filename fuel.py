import pygame

class Fuel(pygame.sprite.Sprite):
    def __init__(self, game, starting_pos):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/graphics/fuel.png').convert_alpha()
        self.image.set_colorkey('#FFFFFF')
        self.rect = self.image.get_rect(center=starting_pos)

        self.mask = pygame.mask.from_surface(self.image)
        self.starting_pos = starting_pos
    
    def move(self):
        self.rect.y += 10
        offset_x = self.game.player.rect.x - self.rect.x
        offset_y = self.game.player.rect.y - self.rect.y
        if self.mask.overlap(self.game.player.player_mask, (offset_x, offset_y)) and self.game.player.fuel_status <= 95:
            self.kill()
            self.game.player.fuel_status += 20
            self.game.player.can_fire_laser = True

        if self.rect.y > 720+100:
            self.kill()

    def update(self):
        self.move()