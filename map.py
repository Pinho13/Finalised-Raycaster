import pygame

from pygame import Vector2
from tools import *
from settings import *
#20 - direita ->
#30 - esquerda <-
#40 - cima ^
#50 - baixo
map_struct = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [40, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [41, 0, 0, 0, 0, 0, 0, 0, 0, 51],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 30, 1, 1, 1, 1, 1]
]
WALL_SIZE = HEIGHT/len(map_struct[0])


class Map:
    def __init__(self, game):
        self.game = game
        self.grid = []
        self.map_struct = map_struct
        self.rows = len(self.map_struct)
        self.col = len(self.map_struct[0])
        self.wall_cords = {}
        self.wall_size = WALL_SIZE
        self.get_cords()

    def get_cords(self):
        for j, row in enumerate(self.map_struct):
            for i, value in enumerate(row):
                self.grid.append(Vector2(j, i))
                if value:
                    self.wall_cords[(j, i)] = value
        self.build_map()

    def build_map(self):
        for cord in self.wall_cords:
            if self.wall_cords[cord] < 10:
                walls_group.add(Wall(cord_to_pos(cord), "white"))
            else:
                walls_group.add(Wall(cord_to_pos(cord), "black"))


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pos
        self.size = (WALL_SIZE, WALL_SIZE)
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.pos)
        collision_objects.append(self.rect)

