import pygame
import os

from settings import *
from map import *
from tools import *
from collections import deque


class SpriteObject:
    def __init__(self, game, path='Art/props/props1.png', pos=(8, 4), scale=0.5, shift=0.5, rect_size=0):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HEIGHT = self.image.get_height()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.IMAGE_HEIGHT
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        if rect_size > 0:
            self.rect = pygame.Rect((0, 0), (rect_size, rect_size))
            self.rect.center = (self.x * WALL_SIZE, self.y * WALL_SIZE)
            collision_objects.append(self.rect)

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pygame.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        self.game.player.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.pos.x/WALL_SIZE
        dy = self.y - self.player.pos.y/WALL_SIZE
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.rad_angle
        if (dx > 0 and self.player.rad_angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        if self.game.dimension == 3:
            self.get_sprite()
        else:
            pygame.draw.circle(self.game.screen, "green", (self.x * WALL_SIZE, self.y * WALL_SIZE), 10)


class Animator:
    def __init__(self, path='Art/fullres/1.png', animation_time=120, loop=False):
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.frame_names = deque()
        self.images = self.get_images(self.path)
        self.animation_time_prev = pygame.time.get_ticks()
        self.animation_trigger = False
        self.playing = False
        self.loop = loop
        self.current_image = self.images[0]

    def update(self):
        if self.playing:
            self.check_animation_time()
            self.animate()

    def animate(self):
        if self.animation_trigger:
            self.images.rotate(-1)
            self.frame_names.rotate(-1)
            self.current_image = self.images[0]
            if self.frame_names[0] == "1":
                if not self.loop:
                    self.playing = False

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        items = os.listdir(path)
        for i in range(len(items)):
            file_name = str(i + 1) + (".png")
            if os.path.isfile(os.path.join(path, file_name)):
                img = pygame.image.load(path + '/' + file_name).convert_alpha()
                self.frame_names.append(file_name.rsplit(".", 1)[0])
                images.append(img)
        return images
