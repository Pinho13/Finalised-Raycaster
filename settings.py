import math

#Window
RES = WIDTH, HEIGHT = (1600, 1000)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
WINDOW_NAME = "FinalProject"
BACKGROUND_COLOR = (0, 0, 0)
DIMENSION = 2
FPS = 60


#Player
PLAYER_POS = (WIDTH/2, HEIGHT/2)
PLAYER_ANGLE = -90
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 100
PLAYER_MAX_HEALTH = 100


#Mouse
MOUSE_SENSITIVITY = 10
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = (WIDTH/2) - 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

#Raycasting
FOV = math.radians(60)
HALF_FOV = FOV / 2
NUM_RAYS = int(WIDTH // 2)
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
RAY_SIZE = 1500
MAX_DEPTH = 20
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

#Textures
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2