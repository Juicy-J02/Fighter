import pygame


class Projectile:
    def __init__(self, x, y, direction, speed, damage, image, scale):
        self.image = image
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.active = True

        if direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, screen_width, target):
        self.rect.x += self.speed * self.direction

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.active = False

        if self.rect.colliderect(target.rect):
            target.health -= self.damage
            target.small_hit = True
            self.active = False

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)
