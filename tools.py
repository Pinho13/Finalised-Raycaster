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
        self.portals_passed = 0

    def ray_cast(self, pos, angle, additional_depth = 0, alpha = 0, tp = False):
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
            if wall_pos.x < ox:
                wall_angle = 0
                symmetry = -1
            else:
                wall_angle = 180
                symmetry = 1
            portal_offset = "y"
        else:
            self.depth, texture, wall_pos = depth_hor, texture_hor, Vector2(tile_hor)
            x_hor %= 1
            self.offset = (1 - x_hor) if sin_a > 0 else x_hor
            if wall_pos.y < oy:
                wall_angle = 270
                symmetry = 1
            else:
                wall_angle = -90
                symmetry = -1
            portal_offset = "x"
        self.texture = texture
        if DIMENSION == 3:
            self.depth += additional_depth
        no_fish_depth = self.depth * math.cos(-alpha)  # Correção do efeito fishbowl
        if DIMENSION == 3:
            self.depth = no_fish_depth
        self.hit_point = Vector2(ox + self.depth * cos_a, oy + self.depth * sin_a) * map.WALL_SIZE#Interceção
        self.proj_height = SCREEN_DIST / (self.depth + 0.0001)#Altura
        self.color_value = 1 / (1 + (abs(self.depth) ** 3) * 0.03)#Cor
        if DIMENSION == 2:
            pygame.draw.line(self.game.screen, 'orange', (pos.x, pos.y), (pos.x + 100 * self.depth * cos_a, pos.y + 100 * self.depth * sin_a), 2)
        if texture >= 20 and self.portals_passed <= 250:
            wall_pos = cord_to_pos(wall_pos)
            point = Vector2(self.hit_point - wall_pos)
            if portal_offset == "x":
                portal_offset = -point.x
            else:
                portal_offset = -point.y
            self.portals_passed += 1
            if not tp:
                self.portal(texture, angle, portal_offset, wall_angle, alpha, symmetry)
            elif Vector2(self.hit_point - self.game.player.pos).length() < 20:
                self.portal_tp(texture, angle, portal_offset, wall_angle, symmetry)
        if texture < 20:
            self.portals_passed = 0



    #https://www.cs.rpi.edu/~cutler/classes/advancedgraphics/S19/final_projects/max_sol.pdf
    def portal(self, num, angle, point, wall_angle, alpha, symmetry):
        map_walls = self.game.map.wall_cords
        for i in map_walls:
            if map_walls[i] >= 20:
                if map_walls[i] != num and str(map_walls[i])[1] == str(num)[1]:
                    wall_cords = i
                    wall_num = map_walls[i]

        alpha_angle = angle - math.radians(wall_angle)
        if wall_cords:
            wall_pos = Vector2(cord_to_pos(wall_cords))
        match str(wall_num)[0]:
            case "2":
                self.ray_cast(wall_pos + Vector2(map.WALL_SIZE/2, -point * symmetry), alpha_angle + 0.0001, self.depth, alpha)
                if DIMENSION == 2:
                    pygame.draw.circle(self.game.screen, (200, 200, 200), wall_pos + Vector2(map.WALL_SIZE/2, point * symmetry), 4)
            case "3":
                self.ray_cast(wall_pos + Vector2(-map.WALL_SIZE/2, point * symmetry), alpha_angle + math.radians(180) + 0.0001, self.depth, alpha)
                if DIMENSION == 2:
                    pygame.draw.circle(self.game.screen, (200, 200, 200), wall_pos + Vector2(-map.WALL_SIZE/2, point * symmetry), 4)
            case "4":
                self.ray_cast(wall_pos + Vector2(point * symmetry, map.WALL_SIZE/2), alpha_angle + math.radians(270) + 0.0001, self.depth, alpha)
                if DIMENSION == 2:
                    pygame.draw.circle(self.game.screen, (200, 200, 200), wall_pos + Vector2(point * symmetry, map.WALL_SIZE/2), 4)
            case "5":
                self.ray_cast(wall_pos + Vector2(point * -symmetry, -map.WALL_SIZE/2), alpha_angle - math.radians(90) * symmetry + 0.0001, self.depth, alpha)
                if DIMENSION == 2:
                    pygame.draw.circle(self.game.screen, (200, 200, 200), wall_pos + Vector2(point * symmetry, -map.WALL_SIZE/2), 4)

    def portal_tp(self, num, angle, point, wall_angle, symmetry):
        map_walls = self.game.map.wall_cords
        for i in map_walls:
            if map_walls[i] >= 20:
                if map_walls[i] != num and str(map_walls[i])[1] == str(num)[1]:
                    wall_cords = i
                    wall_num = map_walls[i]

        alpha_angle = angle - math.radians(wall_angle)
        print()
        if wall_cords:
            wall_pos = Vector2(cord_to_pos(wall_cords))
        match str(wall_num)[0]:
            case "2":
                self.game.player.pos = wall_pos + Vector2(map.WALL_SIZE / 2, -point * symmetry)
                self.game.player.angle = math.degrees(alpha_angle) + 0.0001
            case "3":
                self.game.player.pos = wall_pos + Vector2(-map.WALL_SIZE / 2, point * symmetry)
                self.game.player.angle = math.degrees(alpha_angle + math.radians(180)) + 0.0001
            case "4":
                self.game.player.pos = wall_pos + Vector2(point * symmetry, map.WALL_SIZE / 2)
                self.game.player.angle = math.degrees(alpha_angle + math.radians(270)) + 0.0001
            case "5":
                self.game.player.pos = wall_pos + Vector2(point * -symmetry,  -map.WALL_SIZE / 2)
                self.game.player.angle = math.degrees(alpha_angle - math.radians(90) * symmetry) + 0.0001
