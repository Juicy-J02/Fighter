import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

clock = pygame.time.Clock()
FPS = 60

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
round_over_time = 0
ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.5)

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior_3.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

victory_image = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7, 8, 1]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 10)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 12)

run = True
while run:

    clock.tick(FPS)

    draw_bg()

    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P: " + str(score[1]), score_font, RED, 580, 60)

    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over is False:
        if fighter_1.alive is False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive is False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_image, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 10)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 14)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
