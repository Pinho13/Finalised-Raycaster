import pygame
import math

from settings import *
from pygame import Vector2
from tools import *
from map import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        #Player Stats
        self.pos = Vector2(PLAYER_POS)
        self.angle = PLAYER_ANGLE
        self.rad_angle = math.radians(self.angle)
        self.health = PLAYER_MAX_HEALTH
            #physics
        self.dir = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.col_vector = Vector2(1, 1)
        #-----------#

        #Common Var
        self.game = game
        self.key = pygame.key.get_pressed()
        self.rel = 0
        #-----------#

        #Create FOV Lines
        if DIMENSION == 2:
            self.lines_pos = []
            for i in range(NUM_RAYS):
                self.lines_pos.append(Vector2(0, 0))
        # -----------#

        #Rays
        self.rays = []
        for i in range(NUM_RAYS):
            self.rays.append(Ray(game))
    def update(self):
        self.key = pygame.key.get_pressed()
        self.direction()
        self.movement()
        self.change_angle()
        self.check_wall()
        self.mouse_control()
        self.ray_casting()

    def movement(self):
        self.vel = self.dir * PLAYER_SPEED * self.game.delta_time
        self.pos += Vector2(self.vel.x * self.col_vector.x, self.vel.y * self.col_vector.y)

    def direction(self):
        dir = Vector2(0, 0)

        if self.key[pygame.K_w]:
            dir.y += 1
        if self.key[pygame.K_s]:
            dir.y += -1
        if self.key[pygame.K_a]:
            dir.x += 1
        if self.key[pygame.K_d]:
            dir.x += -1

        if dir:
            self.dir = dir.rotate(self.angle-90).normalize()
        else:
            self.dir = Vector2(0, 0)

    def change_angle(self):
        self.rad_angle = math.radians(self.angle)
        if self.key[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        if self.key[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time

        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle = 360 + self.angle

    def check_wall(self):
        if self.dir == Vector2(0, 0):
            col_dir = Vector2(0, 0)
        else:
            col_dir = Vector2(1, 1)

        for rects in walls_group:
            vector = Vector2(self.pos + self.vel)
            if rects.rect.collidepoint(vector.x, self.pos.y):
                col_dir.x = 0
            if rects.rect.collidepoint(self.pos.x, vector.y):
                col_dir.y = 0
            self.col_vector = Vector2(col_dir)

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def ray_casting(self):
        angle = self.rad_angle - HALF_FOV + 0.0001
        for i in range(NUM_RAYS):
            self.rays[i].ray_cast(self.pos, angle)
            if DIMENSION == 2:
                self.lines_pos[i] = self.rays[i].hit_point
            angle += DELTA_ANGLE

    def draw_player(self):
        pygame.draw.circle(self.game.screen, (200, 200, 200), self.pos, 20)
        #pygame.draw.line(self.game.screen, 'yellow', (self.pos.x, self.pos.y), Vector2(math.cos(self.rad_angle), math.sin(self.rad_angle)) * WALL_SIZE + self.pos, 2)
        for i in range(NUM_RAYS):
            pygame.draw.line(self.game.screen, 'orange', (self.pos.x, self.pos.y), self.lines_pos[i], 2)

    def draw_vision(self):
        for i in range(NUM_RAYS):
            pygame.draw.rect(self.game.screen, (self.rays[i].color_value, self.rays[i].color_value, self.rays[i].color_value),(i * SCALE, HALF_HEIGHT - self.rays[i].proj_height // 2, SCALE, self.rays[i].proj_height))
