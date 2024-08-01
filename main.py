import pygame, sys, random
from player import Player
from meteor import Meteor
from laser import Laser
from fuel import Fuel
from particle import Particle
from debug import debug

WIDTH = 1280
HEIGHT = 720
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Asteroid Game!')

        # Assets
        self.background = pygame.image.load('assets/graphics/background.png')
        self.font = pygame.font.Font('assets/graphics/subatomic.ttf', 45)
        self.explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
        self.laser_sound = pygame.mixer.Sound('assets/sounds/laser.ogg')
        self.music_sound = pygame.mixer.Sound('assets/sounds/music.wav')
        
        # Player
        self.player = Player((WIDTH//2, HEIGHT-125))
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)
        
        # Meteors, Lasers and Fuel
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.fuel_sprites = pygame.sprite.Group()

        # Meteor Timer
        self.meteor_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.meteor_timer, 500)

        # Fuel Timer
        self.fuel_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.fuel_timer, 1500)

        # Score Timer
        self.score_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.score_timer, 3000)

        # Restart Screen
        self.restart_text = self.font.render('Press Space to Restart', False, '#FFFFFF')
        self.restart_rect = pygame.Rect(640-300, HEIGHT//2, 100, 100)

        self.particle_list = []

        self.running = True

    # Meteors, Fuel Related, and Particle System
    def make_meteors(self):
        random_starting_x = random.randint(0, WIDTH)
        random_size = random.randint(100, 200)
        speed = random.randint(5, 8)
        meteor = Meteor(self, (random_starting_x, -100), (random_size, random_size), speed)
        self.meteor_sprites.add(meteor)

    def make_fuel_pickups(self):
        random_starting_x = random.randint(0, WIDTH)
        fuel = Fuel(self, (random_starting_x, -100)) 
        self.fuel_sprites.add(fuel)

    def draw_fuel_bar(self):
        # Get player's fuel_status
        fuel_level = self.player.fuel_status
        # Rectangle (x, y, w, h)
        fuel_rect = pygame.Rect(WIDTH-50, HEIGHT // 2, 25, fuel_level)
        pygame.draw.rect(self.screen, 'Yellow', fuel_rect)
        pygame.draw.rect(self.screen, 'White', fuel_rect, 3)

    #Score
    def score_display(self):
        # Get player's score
        score = self.player.score
        score_display = self.font.render(f'Score: {int(score)}', False, '#FFFFFF')
        score_rect = score_display.get_rect()
        score_rect.center = (10+WIDTH // 2, HEIGHT-50)

        self.screen.blit(score_display, score_rect)
        pygame.draw.rect(self.screen, 'White', (score_rect.left-10, score_rect.top-10, score_rect.width + 20, score_rect.height + 20), 3)

    def make_particles(self):
        for i in self.particle_list:
            if i.radius <= 0.1:
                self.particle_list.remove(i)
            i.draw_particle()
            i.update()

    def run(self):
        while True:            
            self.screen.blit(self.background, (0, 0))

            #Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if self.running:
                    if event.type == self.meteor_timer:
                        self.make_meteors()  
                    if event.type == self.fuel_timer:
                        self.make_fuel_pickups()
                    # Firing Laser (Costs 10 fuel status)
                    if event.type == pygame.KEYUP: 
                        if event.key == pygame.K_SPACE and self.player.can_fire_laser:
                            self.laser_sprites.add(Laser(self, self.player.rect.center))
                            self.player.update_fuel_status()
                            self.laser_sound.play().set_volume(0.4)
                    if event.type == self.score_timer:
                        self.player.score += 1
                else:
                    # Empty all sprite groups
                    self.player_sprite.empty()
                    self.meteor_sprites.empty()
                    self.fuel_sprites.empty()
                    self.laser_sprites.empty()
                    self.particle_list = []

                    # Reset Player Position
                    self.player = Player((WIDTH//2, HEIGHT-125))
                    self.player_sprite.add(self.player)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            self.running = True
                           
            if self.running:
                # Sprites (Drawing and Updating)
                self.laser_sprites.draw(self.screen)
                self.laser_sprites.update()

                self.player_sprite.draw(self.screen)
                self.player_sprite.update()

                self.meteor_sprites.draw(self.screen)
                self.meteor_sprites.update()

                self.fuel_sprites.draw(self.screen)
                self.fuel_sprites.update()

                # Score and Fuel Bar
                self.draw_fuel_bar()
                self.score_display()

                # Particle System
                self.particle_list.append(Particle((self.player.rect.centerx, self.player.rect.bottom), 2, 1, 5))
                self.make_particles()
            else:
                # Restart Screen
                self.screen.blit(self.restart_text, self.restart_rect)
 
            debug(self.player.rect.center)
            debug(len(self.particle_list), 40)
 
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
