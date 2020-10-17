import pygame
import random

# Constants
GAME_TITLE = "Space Invader"
GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_SIZE = 64
BLACK_COLOR = (0, 0, 0)
IMG_PATH = "images/"
UFO_IMG = "{0}ufo.png".format(IMG_PATH)
BACKGROUNG_IMG = "{0}background.jpg".format(IMG_PATH)
PLAYER_IMG = "{0}player.png".format(IMG_PATH)
ENEMY_IMG = "{0}enemy.png".format(IMG_PATH)
BULLET_IMG = "{0}bullet.png".format(IMG_PATH)

# Initialize the pygame
pygame.init()

# Caption and Icon
pygame.display.set_caption(GAME_TITLE)
icon = pygame.image.load(UFO_IMG)
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

# Background
background = pygame.image.load(BACKGROUNG_IMG)

# Player
playerImg = pygame.image.load(PLAYER_IMG)
# Player horizontal position
playerX = 370
playerX_change = 0

# Player vertical position
playerY = 480
playerY_change = 0

# Enemy
enemyImg = pygame.image.load(ENEMY_IMG)
enemyX = random.randint(0, GAME_WIDTH)
enemyY = random.randint(50, 150)
enemyX_change = 2.5
enemyY_change = 20

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load(BULLET_IMG)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def handle_keydown_event(eventType, eventKey):
    global playerX, playerX_change, playerY_change, bullet_state, bulletX, bulletY

    # if keystroke is pressed check whether its right or left
    if eventType == pygame.KEYDOWN:
        if eventKey == pygame.K_LEFT:
            playerX_change = -5
        if eventKey == pygame.K_RIGHT:
            playerX_change = 5
        if eventKey == pygame.K_UP:
            playerY_change = -2.5
        if eventKey == pygame.K_DOWN:
            playerY_change = 2.5
        if eventKey == pygame.K_SPACE:
            if bullet_state is "ready":
                # Get current x cordinate of the spaceship
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)

    # if keystroke is released don't change the players position
    if eventType == pygame.KEYUP:
        if (
            eventKey == pygame.K_LEFT
            or eventKey == pygame.K_RIGHT
            or eventKey == pygame.K_DOWN
            or eventKey == pygame.K_UP
        ):
            playerX_change = 0
            playerY_change = 0


def apply_playerX_change():
    global playerX, playerX_change

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= (GAME_WIDTH - PLAYER_SIZE):
        playerX = GAME_WIDTH - PLAYER_SIZE


def apply_playerY_change():
    global playerY, playerY_change

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= (GAME_HEIGHT - PLAYER_SIZE):
        playerY = GAME_HEIGHT - PLAYER_SIZE


def move_enemy():
    global enemyX, enemyX_change, enemyY, enemyY_change

    # Enemy Movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= (GAME_WIDTH - PLAYER_SIZE):
        enemyX_change = -4
        enemyY += enemyY_change


def move_bullet():
    global bulletY, bulletY_change, bullet_state, playerX

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill(BLACK_COLOR)

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            handle_keydown_event(
                event.type, (event.key if hasattr(event, "key") else None)
            )  # if keystroke is pressed check whether its right or left

    # Add playerX_change to the current playerX position
    apply_playerX_change()

    # Add playerY_change to the current playerY position
    apply_playerY_change()

    # Enemy Movement
    move_enemy()

    # Bullet Movement
    move_bullet()

    # Update player and enemy positions
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
