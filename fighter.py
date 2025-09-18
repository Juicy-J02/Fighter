import pygame


class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, speed):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 50
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.jump_cooldown = 0
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.attack_delay = 0
        self.crouch = False
        self.hit = False
        self.health = 100
        self.alive = True
        self.speed = speed
        self.harm = False
        self.harm_hit = False
        self.harm_cooldown = 0
        self.harm_countdown = 0
        self.harm_hit_cooldown = 0

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
                if key[pygame.K_a] and (self.attacking is False or self.jump is True):
                    dx = -self.speed
                    self.running = True
                    self.flip = True
                if key[pygame.K_d] and (self.attacking is False or self.jump is True):
                    dx = self.speed
                    self.running = True
                    self.flip = False
                if key[pygame.K_w] and self.jump is False and self.jump_cooldown == 0:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_s] and self.jump is False:
                    dx = 0
                    self.crouch = True
                else:
                    self.crouch = False
                if self.attacking is False:
                    if key[pygame.K_r] or key[pygame.K_t]:
                        if key[pygame.K_r]:
                            self.attack_type = 1
                            self.attack_delay = pygame.time.get_ticks() + (self.animation_cooldown * 5) + 5
                        if key[pygame.K_t]:
                            self.attack_type = 2
                            self.attack_delay = pygame.time.get_ticks() + (self.animation_cooldown * 3) + 5
                        self.attack()

            if self.player == 2:
                if key[pygame.K_LEFT] and (self.attacking is False or self.jump is True):
                    dx = -self.speed
                    self.running = True
                    self.flip = True
                if key[pygame.K_RIGHT] and (self.attacking is False or self.jump is True):
                    dx = self.speed
                    self.running = True
                    self.flip = False
                if key[pygame.K_UP] and self.jump is False and self.jump_cooldown == 0:
                    self.vel_y = -35
                    self.jump = True
                if self.attacking is False:
                    if key[pygame.K_KP1] or key[pygame.K_KP2]:
                        if key[pygame.K_KP1]:
                            self.attack_type = 1
                            self.attack_delay = pygame.time.get_ticks() + (self.animation_cooldown * 4) + 5
                        if key[pygame.K_KP2]:
                            self.attack_type = 2
                            self.attack_delay = pygame.time.get_ticks() + (self.animation_cooldown * 5) + 5
                        self.attack()

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
            if pygame.time.get_ticks() >= self.attack_delay:
                self.throw_attack(surface, target)
                self.attack_delay = 0

        self.rect.x += dx
        self.rect.y += dy

        # harm conditions

        if self.harm_cooldown > 0 and self.harm is True:
            self.health -= .15
            if pygame.time.get_ticks() >= self.harm_cooldown:
                self.speed += 6
                self.harm = False

        # harm hit conditions

        if self.harm_hit_cooldown > 0 and self.harm_hit is True:
            if pygame.time.get_ticks() >= self.harm_hit_cooldown:
                self.harm_hit = False

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
        elif self.crouch is True:
            self.update_action(8)
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
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20  # Attack Delay
                    self.jump_cooldown = 10  # Jump Delay
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 30  # Hit Delay

    def attack(self):
        if self.attack_cooldown == 0 and self.hit is False:
            self.attacking = True
            self.attack_sound.play()

    def throw_attack(self, surface, target):
        if self.player == 1:

            if self.attack_type == 1:
                self.update_time = pygame.time.get_ticks()
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                             self.rect.y, 2 * self.rect.width + 35, self.rect.height)
                if attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    target.hit = True
                self.draw_debug(surface, attacking_rect)

            if self.attack_type == 2:
                attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width // 2),
                                             self.rect.y + self.rect.height / 2, 3 * self.rect.width,
                                             self.rect.height / 1.5)
                self.draw_debug(surface, attacking_rect)
                if self.flip is False:
                    attacking_rect_2 = pygame.Rect(self.rect.centerx + 120, self.rect.y, self.rect.width,
                                                   self.rect.height)
                    self.draw_debug(surface, attacking_rect_2)
                else:
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - 200, self.rect.y, self.rect.width,
                                                   self.rect.height)
                    self.draw_debug(surface, attacking_rect_2)

                if self.flip is False:
                    attacking_rect_3 = pygame.Rect(self.rect.centerx - 235, self.rect.y - 65, self.rect.width + 35,
                                                   self.rect.height + 40)
                    self.draw_debug(surface, attacking_rect_3)
                else:
                    attacking_rect_3 = pygame.Rect(self.rect.centerx + 120, self.rect.y - 65, self.rect.width + 35,
                                                   self.rect.height + 40)
                    self.draw_debug(surface, attacking_rect_3)

                if attacking_rect_3.colliderect(target.rect):
                    target.health -= 15
                    target.hit = True
                elif attacking_rect.colliderect(target.rect) or attacking_rect_2.colliderect(target.rect):
                    target.health -= 5
                    target.hit = True

        if self.player == 2:
            if self.attack_type == 1:

                if self.flip is False:
                    attacking_rect = pygame.Rect(self.rect.centerx + 90, self.rect.y - 40, self.rect.width,
                                                   self.rect.height / 1.25)
                    self.draw_debug(surface, attacking_rect)
                else:
                    attacking_rect = pygame.Rect(self.rect.centerx - 170, self.rect.y - 40, self.rect.width,
                                                   self.rect.height / 1.25)
                    self.draw_debug(surface, attacking_rect)

                if self.flip is False:
                    attacking_rect_2 = pygame.Rect(self.rect.centerx + 220, self.rect.y - 60, self.rect.width + 20,
                                                   self.rect.height / 1.25)
                    self.draw_debug(surface, attacking_rect_2)
                else:
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - 300, self.rect.y - 60, self.rect.width + 20,
                                                   self.rect.height / 1.25)
                    self.draw_debug(surface, attacking_rect_2)

                if attacking_rect_2.colliderect(target.rect):
                    target.hit = True
                    target.health -= 5
                    self.apply_harm_hit(target)
                    if target.harm is False and target.harm_countdown == 3:
                        self.apply_harm(target)
                elif attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    target.hit = True

            if self.attack_type == 2:

                if self.flip is False:
                    attacking_rect = pygame.Rect(self.rect.centerx + 200, self.rect.y - 100, self.rect.width * 2,
                                                 self.rect.height * 1.6)
                    self.draw_debug(surface, attacking_rect)
                else:
                    attacking_rect = pygame.Rect(self.rect.centerx - 350, self.rect.y - 100, self.rect.width * 2,
                                                 self.rect.height * 1.6)
                    self.draw_debug(surface, attacking_rect)

                if attacking_rect.colliderect(target.rect):
                    target.hit = True
                    target.health -= 5
                    self.apply_harm_hit(target)
                    if target.harm is False and target.harm_countdown == 3:
                        self.apply_harm(target)

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
        #  pygame.draw.rect(surface, (0, 255, 0), rect)

    @staticmethod
    def apply_harm(target):
        target.harm = True
        target.harm_countdown = 0
        target.speed -= 6
        target.harm_cooldown = pygame.time.get_ticks() + 1500

    @staticmethod
    def apply_harm_hit(target):
        target.harm_countdown += 1
        target.harm_hit = True
        target.harm_hit_cooldown = pygame.time.get_ticks() + 250

