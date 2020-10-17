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
BACKGROUND_IMG = "{0}background.jpg".format(IMG_PATH)
PLAYER_IMG = "{0}player.png".format(IMG_PATH)
BULLET_IMG = "{0}bullet.png".format(IMG_PATH)
ENEMY_X_CHANGE_VALUE = 2
NUMBER_OF_ENEMIES = 6
SCORE = 0

# Initialize the pygame
pygame.init()

# Caption and Icon
pygame.display.set_caption(GAME_TITLE)
icon = pygame.image.load(UFO_IMG)
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

# Background
background = pygame.image.load(BACKGROUND_IMG)

# Player
playerImg = pygame.image.load(PLAYER_IMG)
# Player horizontal position
player_X_position = 370
player_X_position_change = 0

# Player vertical position
player_Y_position = 480
player_Y_position_change = 0

# Enemies lists
enemies = []
enemies_X_position = []
enemies_Y_position = []
enemies_X_position_change = []
enemies_Y_position_change = []

# Create the enemies
for i in range(NUMBER_OF_ENEMIES):
    enemyImg = "{0}enemy_{1}.png".format(IMG_PATH, i)
    enemies.append(pygame.image.load(enemyImg))
    enemies_X_position.append(random.randint(0, 735))
    enemies_Y_position.append(random.randint(50, 150))
    enemies_X_position_change.append(2)
    enemies_Y_position_change.append(20)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load(BULLET_IMG)
bullet_X_position = 0
bullet_Y_position = 480
bullet_X_position_change = 0
bullet_Y_position_change = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    global enemies
    screen.blit(enemies[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def handle_keydown_event(eventType, eventKey):
    global player_X_position, player_X_position_change, player_Y_position_change, bullet_state, bullet_X_position, bullet_Y_position

    # if keystroke is pressed check whether its right or left
    if eventType == pygame.KEYDOWN:
        if eventKey == pygame.K_LEFT:
            player_X_position_change = -5
        if eventKey == pygame.K_RIGHT:
            player_X_position_change = 5
        if eventKey == pygame.K_UP:
            player_Y_position_change = -2.5
        if eventKey == pygame.K_DOWN:
            player_Y_position_change = 2.5
        if eventKey == pygame.K_SPACE:
            if bullet_state is "ready":
                # Get current x cordinate of the spaceship
                bullet_X_position = player_X_position
                bullet_Y_position = player_Y_position
                fire_bullet(bullet_X_position, bullet_Y_position)

    # if keystroke is released don't change the players position
    if eventType == pygame.KEYUP:
        if (
            eventKey == pygame.K_LEFT
            or eventKey == pygame.K_RIGHT
            or eventKey == pygame.K_DOWN
            or eventKey == pygame.K_UP
        ):
            player_X_position_change = 0
            player_Y_position_change = 0


def change_player_X_position():
    global player_X_position, player_X_position_change

    player_X_position += player_X_position_change
    if player_X_position <= 0:
        player_X_position = 0
    elif player_X_position >= (GAME_WIDTH - PLAYER_SIZE):
        player_X_position = GAME_WIDTH - PLAYER_SIZE


def change_player_Y_position():
    global player_Y_position, player_Y_position_change

    player_Y_position += player_Y_position_change
    if player_Y_position <= 0:
        player_Y_position = 0
    elif player_Y_position >= (GAME_HEIGHT - PLAYER_SIZE):
        player_Y_position = GAME_HEIGHT - PLAYER_SIZE


def move_bullet():
    global bullet_Y_position, bullet_Y_position_change, bullet_state, player_X_position

    if bullet_Y_position <= 0:
        bullet_Y_position = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(player_X_position, bullet_Y_position)
        bullet_Y_position -= bullet_Y_position_change


def calculate_distance(x1, x2, y1, y2):
    # Calculate the differences
    x = x1 - x2
    y = y1 - y2

    # Square the differences
    x = x ** 2
    y = y ** 2

    # Return the square root
    return (x + y) ** (1 / 2)


def isCollision(
    enemy_X_position, enemy_Y_position, bullet_X_position, bullet_Y_position
):
    distance = calculate_distance(
        enemy_X_position, bullet_X_position, enemy_Y_position, bullet_Y_position
    )

    if distance < 27:
        return True
    else:
        return False


def change_enemy_position(i):
    global enemies_X_position, enemies_Y_position

    enemies_X_position[i] = random.randint(0, 735)
    enemies_Y_position[i] = random.randint(50, 150)


def move_enemy():
    global enemies_X_position, enemies_X_position_change, enemies_Y_position, enemies_Y_position_change, bullet_Y_position, bullet_state, SCORE

    # Enemies Movement
    for i in range(NUMBER_OF_ENEMIES):
        enemies_X_position[i] += enemies_X_position_change[i]

        if enemies_X_position[i] <= 0:
            enemies_X_position_change[i] = ENEMY_X_CHANGE_VALUE
            enemies_Y_position[i] += enemies_Y_position_change[i]
        elif enemies_X_position[i] >= (GAME_WIDTH - PLAYER_SIZE):
            enemies_X_position_change[i] = -ENEMY_X_CHANGE_VALUE
            enemies_Y_position[i] += enemies_Y_position_change[i]

        # Collision
        collision = isCollision(
            enemies_X_position[i],
            enemies_Y_position[i],
            bullet_X_position,
            bullet_Y_position,
        )
        if collision:
            bullet_Y_position = player_Y_position
            bullet_state = "ready"
            SCORE += 1
            print(SCORE)
            change_enemy_position(i)

        enemy(enemies_X_position[i], enemies_Y_position[i], i)


"""
GAME LOOP INIT
"""
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

    # Change player X position
    change_player_X_position()

    # Change player Y position
    change_player_Y_position()

    # Enemy Movement
    move_enemy()

    # Bullet Movement
    move_bullet()

    # Update player and enemy positions
    player(player_X_position, player_Y_position)
    pygame.display.update()
