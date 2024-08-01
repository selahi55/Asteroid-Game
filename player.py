import pygame
WIDTH = 1280
HEIGHT = 720

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Movement Attributes
        self.pos = pos
        self.velocityX = 0
        self.velocityY = 0
        self.velocityChange = 0.5
    
        # General Setup
        self.image = pygame.image.load('assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.player_mask = pygame.mask.from_surface(self.image)

        self.fuel_status = 100
        self.score = 0
        self.can_fire_laser = True
        self.shield = False
    
    def check_bounds(self):
        #Left
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < -100:
            self.rect.top = 0

    def player_input(self): 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.velocityY += -self.velocityChange
        if keys[pygame.K_DOWN]:
            self.velocityY += self.velocityChange 
        if keys[pygame.K_RIGHT]:
            self.velocityX += self.velocityChange
        if keys[pygame.K_LEFT]:
            self.velocityX += -self.velocityChange

        self.rect.centerx += self.velocityX
        self.rect.centery += self.velocityY

    def update_fuel_status(self):
        if self.fuel_status > 0:
            self.fuel_status -= 10
            if self.fuel_status <= 0:
                self.can_fire_laser = False

    def update(self):
        self.player_input()
        self.check_bounds()


