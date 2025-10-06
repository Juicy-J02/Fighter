import pygame


def left_move(player):
    dx = -player.speed
    player.running = True
    player.flip = True
    return dx


def right_move(player):
    dx = player.speed
    player.running = True
    player.flip = False
    return dx


def jump(player):
    player.vel_y = -player.jump_height
    player.jump = True


def attack_1(player, hit_delay):
    player.attack_type = 1
    player.attack_delay = pygame.time.get_ticks() + (player.animation_cooldown * hit_delay) + 5
    if player.attack_cooldown == 0 and player.hit is False:
        player.attacking = True
        if player.attack_sound:
            player.attack_sound.play()


def attack_2(player, hit_delay):
    player.attack_type = 2
    player.attack_delay = pygame.time.get_ticks() + (player.animation_cooldown * hit_delay) + 5
    if player.attack_cooldown == 0 and player.hit is False:
        player.attacking = True
        if player.attack_sound:
            player.attack_sound.play()
