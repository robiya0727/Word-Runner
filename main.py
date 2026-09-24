import pygame
import random
from sys import exit

pygame.init() #start the module

#Game setup
screen = pygame.display.set_mode((800, 400)) #create a screen object
pygame.display.set_caption("Wild or Pet?") #creates title
clock = pygame.time.Clock() #creates timing.

#Fonts
score_font = pygame.font.Font(None, 30)

#Game variable
game_screen = 0
score = 0
health = 5

WIN_SCORE = 10

#Animal lists
wild_animals = ["capybara", "chimpanzee", "crocodile", "fox", "hedgehog", "lion", "otter", "owl", "raccoon", "skunk", "sloth", "snake", "tiger", "wolf", "turtle"]

pet_animals = ["camel", "cat", "chameleon", "chicken", "cow", "dog", "duck", "fish", "goat", "hamster", "horse", "parrot", "rabbit", "rooster", "sheep"]

#Background
background = pygame.image.load("assets/background.png").convert()

#Start and ending screens
start_screen = pygame.image.load("assets/start_screen.png").convert()
win_screen = pygame.image.load("assets/you_win.png").convert()
game_over_screen = pygame.image.load("assets/game_over.png").convert()

#Buttons
play_btn = pygame.image.load("assets/play.png").convert_alpha()
replay_btn = pygame.image.load("assets/replay.png").convert_alpha()
exit_btn = pygame.image.load("assets/exit.png").convert_alpha()

#Button positions
play_rect = play_btn.get_rect(center =(400, 300))

replay_rect = replay_btn.get_rect(center =(200, 320))

exit_rect = exit_btn.get_rect(center = (620, 320))

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom= (100, 345))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 345:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 345:
            self.rect.bottom = 345
            self.gravity = 0
    
    def update(self):
        self.player_input()
        self.apply_gravity()

#Target class
class Target(pygame.sprite.Sprite):
    def __init__(self, animal, animal_type):
        super().__init__()

        self.animal = animal
        self.animal_type = animal_type
        self.checked = False
        self.start = random.randint(800, 1000)

        self.image = pygame.image.load("assets/" + animal + ".png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom = (self.start, 345))
    def update(self):
        self.rect.x -= 3
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

#Sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

target_group = pygame.sprite.Group()

#Score display
def display_score():
    score_surf = score_font.render("Score: " + str(score), True, (50, 50, 50))
    screen.blit(score_surf, (20, 20))

#Health display
def display_health():
    health_surf = score_font.render("Health: " + str(health), True, (50, 50, 50))
    screen.blit(health_surf, (650, 20))

#Create new target
def create_target():
    if not target_group:
        if random.randint(0, 1) == 0:
            animal = random.choice(wild_animals)
            animal_type = "wild"

        else:
            animal = random.choice(pet_animals)
            animal_type = "pet"

        target_group.add(Target(animal, animal_type))

#Check animal action
def check_animal_action():

    global score
    global health

    if not player.sprite:
        return

    player_sprite = player.sprite

    for target in list(target_group):

        #PET
        #Player must touch the pet.

        if target.animal_type == "pet":
            if pygame.sprite.collide_mask(player_sprite, target):
                score += 1
                target.kill()

            elif target.rect.right < player_sprite.rect.left:
                if not target.checked:
                    health -= 1
                    target.checked = True

        #WILD
        #Player must jump over the wild animal.

        elif target.animal_type == "wild":
            if target.rect.right < player_sprite.rect.left:
                if not target.checked:
                    if player_sprite.rect.bottom < 345:
                        score += 1
                    else:
                        health -= 1

                    target.checked = True
                    target.kill()

#Reset game
def reset_game():

    global score
    global health

    score = 0
    health = 5

    target_group.empty()

    player.sprite.rect.midbottom = (100, 345)
    player.sprite.gravity = 0

#Draw start screen
def draw_start_screen():
    screen.blit(start_screen, (0, 0))
    screen.blit(play_btn, play_rect)

#Draw win screen
def draw_win_screen():
    screen.blit(win_screen, (0, 0))
    screen.blit(replay_btn, replay_rect)
    screen.blit(exit_btn, exit_rect)
    
#Draw game over screen
def draw_game_over_screen():
    screen.blit(game_over_screen, (0, 0))
    screen.blit(replay_btn, replay_rect)
    screen.blit(exit_btn, exit_rect)

#Game loop
while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()

        #Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #PLAY button
                if game_screen == 0:
                    if play_rect.collidepoint(event.pos):
                        reset_game()
                        game_screen = 1

                #REPLAY button
                elif game_screen == 2 or game_screen == 3:
                    if replay_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()

    #Start screen
    if game_screen == 0:
        draw_start_screen()

    #Main game
    elif game_screen == 1:
        #Background
        screen.blit(background, (0, 0))

        #create animals
        create_target()

        #Targets
        target_group.draw(screen)
        target_group.update()

        #Player
        player.draw(screen)
        player.update()

        #Check actions
        check_animal_action()

        #Display information
        display_score()
        display_health()

        #Check win
        if score >= WIN_SCORE:
            game_screen = 2

        #Check game over
        elif health <= 0:
            game_screen = 3

    #Win screen
    elif game_screen == 2:
        draw_win_screen()

    #Game over screen
    elif game_screen == 3:
        draw_game_over_screen()

    #Update screen
    pygame.display.update()
    clock.tick(60)
    