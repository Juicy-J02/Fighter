import pygame

class Lightning:
    def __init__(self, x, y, direction, speed, damage, image=None):
        self.image = image
        self.rect = pygame.Rect(x, y, 40, 20)  # size of the projectile (tweak as needed)
        self.direction = direction  # 1 for right, -1 for left
        self.speed = speed
        self.damage = damage
        self.active = True  # so we can remove it once it goes off-screen

    def move(self, screen_width, target):
        # move projectile
        self.rect.x += self.speed * self.direction

        # deactivate if it leaves screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.active = False

        # check collision
        if self.rect.colliderect(target.rect):
            target.health -= self.damage
            target.hit = True
            self.active = False

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)  # debug red box
