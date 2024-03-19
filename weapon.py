import pygame

from pygame import Vector2
from settings import *
from sprites import *


class Weapon:
    def __init__(self, game):
        self.game = game
        self.pos = Vector2(0, 0)
        self.image = pygame.image.load("Art/fullres/1.png").convert_alpha()
        self.animator = Animator("Art/fullres/1.png", 35)
        for i, image in enumerate(self.animator.images):
            self.animator.images[i] = pygame.transform.scale(image, (self.image.get_width() + 110, self.image.get_height() + 110))
        self.animator.current_image = self.animator.images[0]

    def update(self):
        self.attack()

    def attack(self):
        button = pygame.mouse.get_pressed()
        if self.animator.frame_names[0] == "1" and button[0]:
            self.animator.playing = True
            self.game.sound.sword_swing.play()

    def draw_weapon(self):
        self.animator.update()
        self.game.screen.blit(self.animator.current_image, self.pos)
