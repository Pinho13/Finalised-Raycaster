import pygame
import sys

from settings import *
from map import *
from tools import *
from player import *
from renderer import *
from sprites import *
from weapon import *
from sound import *

#CONTROLOS
#W - mover frente
#S - mover trás
#D - mover direita
#A - mover esquerda
#F - mudar entre 2d e 2.5d

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption(WINDOW_NAME)
        pygame.mouse.set_visible(False)
        self.delta_time = 0
        self.clock = pygame.Clock()
        self.weapon_active = WEAPON_ACTIVE
        self.game_initializer()

    def game_initializer(self):
        self.sprites = []
        self.sound = Sound(self)
        self.dimension = DIMENSION
        self.renderer = ObjectRenderer(self)
        self.map = Map(self, self.renderer)
        self.player = Player(self)
        self.sprites.append(SpriteObject(self, pos=(8, 1.5), rect_size=100))
        self.weapon = Weapon(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.change_dimension()

    def update(self):
        self.control_game()
        self.player.update()
        for sprite in self.sprites:
            if isinstance(sprite, SpriteObject):
                sprite.update()
        if self.weapon_active:
            self.weapon.update()
        pygame.display.update()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        match self.dimension:
            case 2:
                walls_group.draw(self.screen)
                self.player.draw_player()
            case 3:
                self.renderer.draw()
                if self.weapon_active:
                    self.weapon.draw_weapon()

    def control_game(self):
        self.clock.tick(FPS)
        pygame.display.set_caption(WINDOW_NAME + "-" + str(int(self.clock.get_fps())) + "FPS")
        self.delta_time = pygame.Clock().tick(60) / 1000

    def change_dimension(self):
        if self.dimension == 2:
            self.dimension = 3
        else:
            self.dimension = 2

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
