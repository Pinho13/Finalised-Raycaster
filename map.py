import pygame

from pygame import Vector2
from tools import *
from settings import *

map_struct = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
            walls_group.add(Wall(cord_to_pos(cord)))


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.size = (WALL_SIZE, WALL_SIZE)
        self.image = pygame.Surface(self.size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)
        collision_objects.append(self.rect)

