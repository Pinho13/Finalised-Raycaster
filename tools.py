import pygame
import math
import map

from pygame import Vector2
from settings import *

walls_group = pygame.sprite.Group()
collision_objects = []


def cord_to_pos(vector):
    return (vector + Vector2(0.5, 0.5)) * map.WALL_SIZE


def pos_to_cord(vector):
    return (vector/map.WALL_SIZE) - Vector2(0.5, 0.5)


def pos_to_cord_snap_to_grid(vector):
    vec = Vector2((vector/map.WALL_SIZE) - Vector2(0.5, 0.5))
    return Vector2(int(vec.x), int(vec.y))


class Ray:
    def __init__(self, game):
        self.game = game
        self.depth = 0
        self.texture = 0
        self.offset = 0
        self.proj_height = 0
        self.color_value = 0
        self.hit_point = Vector2(0, 0)

    def ray_cast(self, pos, angle):
        ox, oy = pos/map.WALL_SIZE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        map_x, map_y = int(ox), int(oy)
        texture_vert, texture_hor = 1, 1
        #Interceções horinzontais

        y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1) #y_hor distância no y até a primeira interseção, dy direção (cima ou baixo)
        depth_hor = (y_hor - oy) / sin_a #distãncia diagonal até a primeira interceção

        x_hor = ox + depth_hor * cos_a #x_hor distância no x até a primeira interseção
        delta_depth = dy / sin_a #delta_depth interceção entre os pontos apos a primeira
        dx = delta_depth * cos_a #direção no x (esquerda, direita)
        #soma dos valores até se colidir com uma parede
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in self.game.map.wall_cords:
                texture_hor = self.game.map.wall_cords[tile_hor]
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        #Interceções Verticais (tudo igual mas para as interceções com os eixos verticais)
        x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in self.game.map.wall_cords:
                texture_vert = self.game.map.wall_cords[tile_vert]
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        #Escolha se a primeira interceção é com o eixo vertical ou horizontal, offset do sitio em que a textura da parede é intercetada
        if depth_vert < depth_hor:
            self.depth, texture, wall_pos = depth_vert, texture_vert, Vector2(tile_vert)
            y_vert %= 1
            self.offset = y_vert if cos_a > 0 else (1 - y_vert)
            if wall_pos.y > oy:
                wall_angle = 270
            else:
                wall_angle = 90
        else:
            self.depth, texture, wall_pos = depth_hor, texture_hor, Vector2(tile_hor)
            x_hor %= 1
            self.offset = (1 - x_hor) if sin_a > 0 else x_hor
            if wall_pos.x > ox:
                wall_angle = 0
            else:
                wall_angle = 180
        if DIMENSION == 3:
            self.depth *= math.cos(self.game.player.rad_angle - angle)  # Correção do efeito fishbowl
        self.hit_point = Vector2(ox + self.depth * cos_a, oy + self.depth * sin_a) * map.WALL_SIZE#Interceção
        self.proj_height = SCREEN_DIST / (self.depth + 0.0001)#Altura
        self.color_value = 255 / (1 + (abs(self.depth) ** 3) * 0.03)#Cor
        pygame.draw.line(self.game.screen, 'orange', (pos.x, pos.y), (pos.x + 100 * self.depth * cos_a, pos.y + 100 * self.depth * sin_a), 2)
        if texture >= 20:
            wall_pos = cord_to_pos(wall_pos)
            point = wall_pos - self.hit_point
            self.portal(texture, angle, point, wall_angle)

    #https://www.cs.rpi.edu/~cutler/classes/advancedgraphics/S19/final_projects/max_sol.pdf
    def portal(self, num, angle, hit_point, wall_angle):
        map_walls = self.game.map.wall_cords
        for i in map_walls:
            if map_walls[i] >= 20:
                if map_walls[i] != num and str(map_walls[i])[1] == str(num)[1]:
                    wall_cords = i
                    wall_num = map_walls[i]

        match str(wall_num)[0]:
            case "2":
                self.ray_cast(cord_to_pos(wall_cords) + Vector2(0, map.WALL_SIZE/2) + Vector2(0, hit_point.y), angle + (wall_angle))
            case "3":
                self.ray_cast(cord_to_pos(wall_cords) - Vector2(0, map.WALL_SIZE/2) + Vector2(0, hit_point.y), angle + (wall_angle - math.radians(180)))
            case "4":
                self.ray_cast(cord_to_pos(wall_cords) - Vector2(0, map.WALL_SIZE/2) + Vector2(hit_point.x, 0), angle + (wall_angle - math.radians(270)))
            case "5":
                self.ray_cast(cord_to_pos(wall_cords) + Vector2(0, map.WALL_SIZE/2) + Vector2(hit_point.x, 0), angle + (wall_angle - math.radians(90)))


