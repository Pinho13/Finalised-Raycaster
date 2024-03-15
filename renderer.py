import pygame

from settings import *


def get_objects_to_render(ray_casting_result, textures):
    objects_to_render = []
    for ray, values in enumerate(ray_casting_result):
        depth, proj_height, texture, offset = values

        if proj_height < HEIGHT:
            wall_column = textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
            )
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
        else:
            texture_height = TEXTURE_SIZE * HEIGHT / proj_height
            wall_column = textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                SCALE, texture_height
            )
            wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)

        objects_to_render.append((depth, wall_column, wall_pos))
    return objects_to_render
