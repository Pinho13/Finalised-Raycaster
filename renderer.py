import pygame

from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()

    def draw(self):
        self.render_game_objects()

    def render_game_objects(self):
        list_objects = sorted(self.game.player.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            color_value = 255 * (1 / (1 + (abs(depth) ** 2) * 0.03))
            image.fill((color_value, color_value, color_value), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            4: self.get_texture('Castlewall_01_medium.png'),
            #2: self.get_texture(''),
        }
