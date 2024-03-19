import random

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
        self.rounded_angle = PLAYER_ANGLE
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
        self.last_step = pygame.time.get_ticks()
        #-----------#

        #Create FOV Lines
        self.lines_pos = []
        for i in range(NUM_RAYS):
            self.lines_pos.append(Vector2(0, 0))
        #------------#

        #Rays
        self.rays = []
        self.ray = Ray(self.game)
        for i in range(NUM_RAYS):
            self.rays.append(Ray(game))
        #------------#

        #Rendering
        self.objects_to_render = []
        self.ray_casting_result = []
        self.textures = self.game.renderer.wall_textures
        # ------------#

    def update(self):
        self.key = pygame.key.get_pressed()
        self.direction()
        self.movement()
        self.change_angle()
        self.check_wall()
        self.mouse_control()
        self.ray_casting()
        self.get_objects_to_render()
        self.foot_steps()

    def movement(self):
        self.vel = self.dir * PLAYER_SPEED * self.game.delta_time
        self.check_for_portal()
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

        match int(self.angle/100):
            case 0:
                if self.angle > 90:
                    self.rounded_angle = self.angle - 90
                else:
                    self.rounded_angle = self.angle
            case 1:
                if self.angle > 180:
                    self.rounded_angle = self.angle - 180
                else:
                    self.rounded_angle = self.angle - 90
            case 2:
                if self.angle > 270:
                    self.rounded_angle = self.angle - 270
                else:
                    self.rounded_angle = self.angle - 180
            case 3:
                self.rounded_angle = self.angle - 270

    def check_wall(self):
        if self.dir == Vector2(0, 0):
            col_dir = Vector2(0, 0)
        else:
            col_dir = Vector2(1, 1)

        for rects in walls_group:
            vector = Vector2(self.pos + self.vel)
            if isinstance(rects, Wall):
                if rects.rect.collidepoint(vector.x, self.pos.y):
                    if not rects.can_cross:
                        col_dir.x = 0
                if rects.rect.collidepoint(self.pos.x, vector.y):
                    if not rects.can_cross:
                        col_dir.y = 0
                #if rects.can_cross and rects.rect.collidepoint(vector):
                    #math.atan2(self.pos.x - rects.pos.x, rects.pos.y - self.pos.y)
                    #if self.vel != Vector2(0, 0):
                    #    vel = self.vel.normalize()
                    #    angle_between = math.atan2(vel.y, vel.x)
                    #else:
                    #    angle_between = math.atan2(self.pos.x - rects.pos.x, rects.pos.y - self.pos.y)
                    #ray = Ray(self.game)
                    #ray.ray_cast(self.pos, angle_between, 0, 0, True)
            self.col_vector = Vector2(col_dir)
        for rects in collision_objects:
            vector = Vector2(self.pos + self.vel)
            if rects.collidepoint(vector.x, self.pos.y):
                col_dir.x = 0
            if rects.collidepoint(self.pos.x, vector.y):
                col_dir.y = 0
            self.col_vector = Vector2(col_dir)

    def check_for_portal(self):
        if self.vel != Vector2(0, 0):
            vel = self.vel.normalize()
            angle_between = math.atan2(vel.y, vel.x)
            self.ray.ray_cast(self.pos, angle_between, 0, 0, True)

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def ray_casting(self):
        self.ray_casting_result = []
        angle = self.rad_angle - HALF_FOV + 0.0001
        for i in range(NUM_RAYS):
            self.rays[i].ray_cast(self.pos, angle, 0, angle - self.rad_angle)
            if self.game.dimension == 2:
                self.lines_pos[i] = self.rays[i].hit_point
            else:
                self.ray_casting_result.append((self.rays[i].depth, self.rays[i].proj_height, self.rays[i].texture, self.rays[i].offset))
            angle += DELTA_ANGLE

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if texture in self.textures:
                if proj_height < HEIGHT:
                    wall_column = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                    )
                    wall_column = pygame.transform.scale(wall_column, (abs(SCALE), abs(proj_height)))
                    wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
                else:
                    texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                    wall_column = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                        SCALE, texture_height
                    )
                    wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                    wall_pos = (ray * SCALE, 0)
                self.objects_to_render.append((depth, wall_column, wall_pos))
            else:
                color_value = 255 * (1 / (1 + (abs(depth) ** 2) * 0.03))
                if texture == 1:
                    pygame.draw.rect(self.game.screen, (color_value, color_value, color_value), (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE,proj_height))
                elif texture == 2:
                    pygame.draw.rect(self.game.screen, (color_value, 0, 0), (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
                elif texture == 3:
                    pygame.draw.rect(self.game.screen, (0, 0, color_value), (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))


    def draw_player(self):
        pygame.draw.circle(self.game.screen, (200, 200, 200), self.pos, 20)
        pygame.draw.line(self.game.screen, 'yellow', (self.pos.x, self.pos.y), Vector2(math.cos(self.rad_angle), math.sin(self.rad_angle)) * WALL_SIZE + self.pos, 2)
        #for i in range(NUM_RAYS):
        #    pygame.draw.line(self.game.screen, 'orange', (self.pos.x, self.pos.y), self.lines_pos[i], 2)

    def foot_steps(self):
        time_now = pygame.time.get_ticks()
        if self.dir != Vector2(0, 0):
            if time_now - self.last_step > STEP_COOLDOWN_SOUND:
                self.last_step = time_now
                self.game.sound.steps[random.randint(0, len(self.game.sound.steps)-1)].play()
