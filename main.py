import pygame
import random

# Initialize the pygame
pygame.init()

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Player
playerImg = pygame.image.load("player.png")
# Player horizontal position
playerX = 370
playerX_change = 0

# Player vertical position
playerY = 480
playerY_change = 0

# Enemy
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 2.5
enemyY_change = 20

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
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


def handle_keydown_event(event):
    global playerX, playerX_change, playerY_change, bullet_state, bulletX, bulletY

    # if keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_UP:
            playerY_change = -2.5
        if event.key == pygame.K_DOWN:
            playerY_change = 2.5

        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                # Get current x cordinate of the spaceship
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)

    # if keystroke is released don't change the players position
    if event.type == pygame.KEYUP:
        if (
            event.key == pygame.K_LEFT
            or event.key == pygame.K_RIGHT
            or event.key == pygame.K_DOWN
            or event.key == pygame.K_UP
        ):
            playerX_change = 0
            playerY_change = 0


def apply_playerX_change():
    global playerX, playerX_change

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


def apply_playerY_change():
    global playerY, playerY_change

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536


def move_enemy():
    global enemyX, enemyX_change, enemyY, enemyY_change

    # Enemy Movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
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
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            handle_keydown_event(
                event
            )  # if keystroke is pressed check whether its right or left

    # Add playerX_change to the current playerX position
    apply_playerX_change()

    # Add playerY_change to the current playerY position
    apply_playerY_change()

    # Enemy Movement
    move_enemy()

    # Bullet Movement
    move_bullet()

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
