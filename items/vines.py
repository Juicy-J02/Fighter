import pygame

class Vines:
    def __init__(self, x, y, flip):
        self.flip = flip
        self.x = x
        self.y = y
        self.size = 25
        self.image_scale = 4

        sprite_sheet = pygame.image.load("assets/images/druid/Sprites/vines_sheet2.png").convert_alpha()
        self.animation_list = self.load_images(sprite_sheet, [1, 7, 7])

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 50

        self.vine_cooldown = 0
        self.grow = False
        self.dissolve = False
        self.active = False

        self.vine_attack_timer = 0

        self.image = self.animation_list[self.action][self.frame_index]

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                )
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                )
            animation_list.append(temp_img_list)
        return animation_list

    def update(self, surface, target, player):
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):

            if self.action == 1:
                self.throw_attack(surface, target)

            elif self.action == 2:
                player.vine = None
            else:
                self.frame_index = 0


    def throw_attack(self, surface, target):
        # attacking_rect = self.image.get_rect(topleft=(self.x, 402))
        attacking_rect = pygame.Rect(self.x + 30, 402, target.rect.width // 1.5, self.image.get_rect().height)

        # self.draw_debug(surface, attacking_rect)

        if attacking_rect.colliderect(target.rect) and not target.trap:
            target.health -= 5
            target.trap = True
            target.hit = True
            target.trap_cooldown = pygame.time.get_ticks() + 2000

            self.vine_cooldown = pygame.time.get_ticks() + 2000
            self.update_action(0)
        else:
            self.update_action(2)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface, target):
        surface.blit(self.image, (self.x, 402))

    def draw_debug(self, surface, rect):
        pygame.draw.rect(surface, (0, 255, 0), rect)
        pass
