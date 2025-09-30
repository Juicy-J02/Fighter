from effects.harm import *
from items.projectile import Projectile
from items.vines import Vines
from movement import *


class Druid:
    def __init__(self, player, x, y, flip):
        self.player = player
        self.size = 162
        self.image_scale = 4
        self.offset = [72, 56]
        self.flip = flip
        self.animation_list = self.load_images(pygame.image.load("assets/images/druid/Sprites/druid.png")
                                               .convert_alpha(), [8, 5, 1, 8, 8, 3, 8, 8])
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 50
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.jump_height = 30
        self.jump_cooldown = 0
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        # self.attack_sound = pygame.mixer.Sound("assets/audio/sword.wav")
        # self.attack_sound.set_volume(0.5)
        self.attack_delay = 0
        self.hit = False
        self.small_hit = False
        self.health = 100
        self.alive = True
        self.speed = 13
        self.harm = False
        self.harm_hit = False
        self.harm_cooldown = 0
        self.harm_countdown = 0
        self.harm_hit_cooldown = 0
        self.projectiles = []
        self.heal = False
        self.heal_cooldown = 0
        self.trap = False
        self.trap_cooldown = 0

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size
                                                                       * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False

        key = pygame.key.get_pressed()

        if self.alive is True and round_over is False and self.hit is False:

            if self.player == 1:
                if key[pygame.K_a]:
                    dx = left_move(self)
                if key[pygame.K_d]:
                    dx = right_move(self)
                if key[pygame.K_w] and self.jump is False and self.jump_cooldown == 0:
                    jump(self)
                if self.attacking is False:
                    if key[pygame.K_r] or key[pygame.K_t]:
                        if key[pygame.K_r]:
                            attack_1(self, 1)
                        if key[pygame.K_t]:
                            attack_2(self, 7)

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = left_move(self)
                if key[pygame.K_RIGHT]:
                    dx = right_move(self)
                if key[pygame.K_UP] and self.jump is False and self.jump_cooldown == 0:
                    jump(self)
                if self.attacking is False:
                    if key[pygame.K_KP1] or key[pygame.K_KP2]:
                        if key[pygame.K_KP1]:
                            attack_1(self, 1)
                        if key[pygame.K_KP2]:
                            attack_2(self, 7)

        self.vel_y += GRAVITY
        dy += self.vel_y

        # left boundary
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        # right boundary
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        # ground boundary
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # if target.rect.centerx > self.rect.centerx and self.alive == True:
        #     self.flip = False
        # else:
        #     self.flip = True

        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # jump cooldown
        if self.jump_cooldown > 0 and self.rect.bottom == screen_height - 110:
            self.jump_cooldown -= 1

        # attack delay
        if self.attack_delay > 0 and self.attacking is True:
            if pygame.time.get_ticks() >= self.attack_delay and self.hit is False:
                self.throw_attack(surface, target)
                self.attack_delay = 0

        self.rect.x += dx
        self.rect.y += dy

        # harm conditions
        if self.harm_cooldown > 0 and self.harm is True:
            apply_harm_damage(self)
            if pygame.time.get_ticks() >= self.harm_cooldown:
                recover_harm(self)

        # harm hit conditions
        if self.harm_hit_cooldown > 0 and self.harm_hit is True:
            if pygame.time.get_ticks() >= self.harm_hit_cooldown:
                self.harm_hit = False

        if self.heal_cooldown > 0 and self.heal is True:
            if pygame.time.get_ticks() >= self.heal_cooldown:
                self.heal = False

        # projectile movement and drawing

        for projectile in self.projectiles:
            projectile.move(screen_width, target)
            projectile.draw(surface)
            if projectile.rect.colliderect(target.rect):
                if self.health <= 98:
                    self.health += 2
                    self.heal_cooldown = pygame.time.get_ticks() + 250
                    self.heal = True
            if projectile.active is False:
                self.projectiles.remove(projectile)

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6: death
        elif self.hit is True:
            self.update_action(5)  # 5: hit
        elif self.attacking is True:
            if self.attack_type == 1:
                self.update_action(3)  # 3: attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4: attack2
        elif self.jump is True:
            self.update_action(2)   # 2: jump
        elif self.running is True:
            self.update_action(1)  # 1: run
        else:
            self.update_action(0)  # 0: idle

        base_image = self.animation_list[self.action][self.frame_index]

        if self.harm is True or self.harm_hit is True:
            self.image = base_image.copy()
            self.image.fill((128, 0, 128), special_flags=pygame.BLEND_RGB_MULT)
        else:
            self.image = base_image

        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive is False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 2:
                    self.jump_cooldown = 10  # Jump Delay
                if self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 10  # Attack Delay
                    self.jump_cooldown = 5  # Jump Delay
                if self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20  # Attack Delay
                    self.jump_cooldown = 5  # Jump Delay
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20  # Hit Delay ##NOTE: Add Hit animation to correct attack_cooldown


    def throw_attack(self, surface, target):
        if self.attack_type == 1:
            if self.flip is False:
                twig = Projectile(self.rect.centerx, self.rect.centery, 1, 50, 5,
                                  pygame.image.load("assets/images/druid/Sprites/projectile.png").convert_alpha(), 3)
            else:
                twig = Projectile(self.rect.centerx, self.rect.centery, -1, 50, 5,
                                  pygame.image.load("assets/images/druid/Sprites/projectile.png").convert_alpha(), 3)
            self.projectiles.append(twig)

        if self.attack_type == 2:

            if self.flip is False:
                vine = Vines(self.rect.centerx + 250, 410, 5,
                                  pygame.image.load("assets/images/druid/Sprites/vines.png").convert_alpha(), 4)
            else:
                vine = Vines(self.rect.centerx - 250, 410, 5,
                                  pygame.image.load("assets/images/druid/Sprites/vines.png").convert_alpha(), 4)

            if self.flip is False:
                attacking_rect = pygame.Rect(self.rect.centerx + 250, 400,
                                             self.rect.width, self.rect.height // 2)
            else:
                attacking_rect = pygame.Rect(self.rect.centerx - 250, 400,
                                             self.rect.width, self.rect.height // 2)
            self.draw_debug(surface, attacking_rect)
            if attacking_rect.colliderect(target.rect) and target.trap is False:
                target.health -= 5
                target.trap = True
                target.trap_cooldown = pygame.time.get_ticks() + 2000


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale),
                           self.rect.y - (self.offset[1] * self.image_scale)))

    def draw_debug(self, surface, rect):
        pass
        pygame.draw.rect(surface, (0, 255, 0), rect)