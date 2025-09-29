import pygame


def apply_harm(target):
    target.harm = True
    target.harm_countdown = 0
    target.speed -= 6
    target.jump_height -= 10
    target.harm_cooldown = pygame.time.get_ticks() + 1500


def apply_harm_hit(target):
    if not target.harm:
        target.harm_countdown += 1
        target.harm_hit = True
        target.harm_hit_cooldown = pygame.time.get_ticks() + 250


def apply_harm_damage(target):
    target.health -= .25


def recover_harm(target):
    target.speed += 6
    target.jump_height += 10
    target.harm = False
