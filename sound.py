import pygame

from settings import *

class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = "Sounds/"
        self.steps = []
        for i in range(4):
            self.steps.append(pygame.mixer.Sound(self.path + "Footstep_" + str(i+1) + ".wav"))
            self.steps[i].set_volume(GLOBAL_SOUNDS_VOLUME)
        self.sword_swing = pygame.mixer.Sound(self.path + "Sword_Swing.wav")
        self.hit = pygame.mixer.Sound(self.path + "Hit.wav")
        self.sword_swing.set_volume(GLOBAL_SOUNDS_VOLUME)
        self.music = pygame.mixer.music.load("Sounds/Ambient Music Track(2).wav")
        pygame.mixer.music.set_volume(GLOBAL_SOUNDS_VOLUME)

