import pygame, time

class Meteor(pygame.sprite.Sprite):
    def __init__(self, game, starting_pos, size, speed):

        # General Setup
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/graphics/meteor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=starting_pos)
        self.explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')

        self.meteor_mask = pygame.mask.from_surface(self.image)

        # Movement Attributes
        self.starting_pos = starting_pos
        self.speed = speed
        self.size = size

        self.gravity = 0

    def move_meteors(self):
        self.rect.y += self.speed
        offset_x = self.game.player.rect.x - self.rect.x
        offset_y = self.game.player.rect.y - self.rect.y

        # Collisions
        if self.meteor_mask.overlap(self.game.player.player_mask, (offset_x, offset_y)):
            self.game.running = False

        if pygame.sprite.spritecollide(self, self.game.laser_sprites, False):
            self.game.player.score += 1
            self.explosion_sound.play().set_volume(0.4)
            self.kill()

        if self.rect.y > 720+100:
            self.kill()

    def update(self):
        self.move_meteors()