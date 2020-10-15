import pygame

# Initialize the pygame
pygame.init()

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    player(playerX, playerY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
                print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
                print("Right arrow is pressed")
        if event.type == pygame.KEYUP:
            playerX_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Keystoke has been released")

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    player(playerX, playerY)
    pygame.display.update()
