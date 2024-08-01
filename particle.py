import pygame

class Particle:
    def __init__(self, pos, velocity, direction, radius):
        
        self.screen = pygame.display.get_surface()

        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity
        self.direction = direction
        self.radius = radius

    def move(self):
        # self.x += self.velocity * self.direction
        self.y += self.velocity * self.direction

    def shrink(self):
        self.radius -= 0.1
            
    def draw_particle(self):
        pygame.draw.circle(self.screen, 'Yellow', (self.x, self.y), self.radius)
    
    def update(self):
        self.move()
        self.shrink()

    
