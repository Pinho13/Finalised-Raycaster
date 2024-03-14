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
        self.walls = []
        self.number_of_cells = 25
        self.cell_size = WIDTH/self.number_of_cells
        self.build_grid()

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
        print(len(self.walls))
        pygame.display.update()

    def build_grid(self):
        cell_size = self.cell_size
        for j in range(self.number_of_cells):
            for i in range(self.number_of_cells):
                rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)
                rect.center = (i * cell_size + cell_size/2, j * cell_size + cell_size/2)
                self.grid.append(rect)

    def place_walls(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(len(self.grid)):
            if self.grid[i].collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, "white", self.grid[i])
                if mouse_button[0]:
                    self.walls.append(Wall(self.grid[i].center, "white", self.cell_size, self))

    def draw(self):
        for square in self.walls:
            if isinstance(square, Wall):
                square.update()

    def run(self):
        while True:
            self.check_events()
            self.update()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, color, size, game):
        super().__init__()
        self.game = game
        self.pos = Vector2(pos)
        self.size = Vector2(size, size)
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.pos)
        for i in self.game.walls:
            if isinstance(i, Wall):
                if i.pos == self.pos and i != self:
                    i.kill()

    def update(self):
        self.game.screen.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_button[1]:
            self.kill()


if __name__ == "__main__":
    game = Game()
    game.run()