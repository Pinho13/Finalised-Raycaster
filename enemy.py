import pygame

from sprites import *
from tools import *
from map import *


class Enemy:
    def __init__(self, game, pos):
        self.game = game
        self.player = game.player
        self.pos = pos * WALL_SIZE
        self.sprite = SpriteObject(game, "Art/enemy/idle/front.png", pos, 1, 0.2, 100)
        self.ray = Ray(game)
        self.vector_to_player = Vector2(self.player.pos - self.pos)

    def update(self):
        self.sprite.update()
        self.sprite.x, self.sprite.y = self.pos/WALL_SIZE
        self.follow_player()

    def follow_player(self):
        dx = self.player.pos.x - self.pos.x
        dy = self.player.pos.y - self.pos.y
        rads = math.atan2(-dy, dx) + 0.0001
        rads %= 2 * math.pi
        self.vector_to_player = Vector2(dx, dy)
        self.ray.ray_cast(self.pos, -rads)
        if self.vector_to_player.length() < Vector2(self.ray.hit_point - self.pos).length():
            self.pos += self.vector_to_player.normalize() * self.game.delta_time * 100