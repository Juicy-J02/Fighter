import pygame

class Fighter:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.image = None
        self.effects = []  # List of active effects like projectiles or vines

    def add_effect(self, effect):
        """Add an effect to this fighter (vine, projectile, etc.)"""
        self.effects.append(effect)

    def update_effects(self, target):
        """Update and apply all effects"""
        for effect in self.effects[:]:  # iterate over a copy
            effect.update()
            effect.throw_attack(target)  # or apply damage/interaction
            if not getattr(effect, "active", True):
                self.effects.remove(effect)

    def draw_effects(self, surface, target):
        """Draw all effects on top of the fighter"""
        for effect in self.effects:
            effect.draw(surface, target)
