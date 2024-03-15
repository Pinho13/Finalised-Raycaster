import pygame
import sys

from settings import *
from pygame import Vector2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption("Map Builder")
        self.grid = []
        self.number_of_cells = 25
        self.cell_size = WIDTH/self.number_of_cells
        self.sprites = pygame.sprite.Group()
        self.build_grid()
        self.get_map()


    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.screen.fill("black")
        self.place_walls()
        self.draw()
        pygame.display.update()

    def build_grid(self):
        cell_size = self.cell_size
        for j in range(self.number_of_cells):
            for i in range(self.number_of_cells):
                rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)
                rect.center = (j * cell_size + cell_size/2, i * cell_size + cell_size/2)
                self.grid.append(rect)

    def place_walls(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        for i in range(len(self.grid)):
            if self.grid[i].collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (150, 150, 150), self.grid[i])
                if mouse_button[0]:
                    self.sprites.add(Wall(self.grid[i].center, "white", self.cell_size, self, self.sprites))

    def draw(self):
        self.sprites.draw(self.screen)
        for square in self.sprites:
            if isinstance(square, Wall):
                square.update()

    def get_map(self):
        cell_size = self.cell_size
        print("[")
        for j in range(self.number_of_cells):
            str = "["
            for i in range(self.number_of_cells):
                for spr in self.sprites:
                    if isinstance(spr, Wall) and spr.pos == (j * cell_size + cell_size/2, i * cell_size + cell_size/2):
                        str += "1, "

                str += "0, "
            str += "]"
            print(str)
        print("]")


    def run(self):
        while True:
            self.check_events()
            self.update()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, color, size, game, sprite_group):
        super().__init__()
        self.game = game
        self.group = sprite_group
        self.pos = Vector2(pos)
        self.size = Vector2(size, size)
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.pos)
        for i in self.group:
            if isinstance(i, Wall):
                if i.pos == self.pos and i != self:
                    self.group.remove(i)

    def update(self):
        self.game.screen.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_button[2]:
            self.group.remove(self)


if __name__ == "__main__":
    game = Game()
    game.run()
