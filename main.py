import pygame
import random
pygame.font.init()
pygame.init()


# screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("background.png")

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("asd.jpg")
pygame.display.set_icon(icon)

# Player
playerIcon = pygame.image.load("spaceship.png")
playerX = WIDTH // 2 - 32

playerY = HEIGHT // 2 + 200
PLAYER_VEL = 15
left = False
right = False

score_value = 0
font = pygame.font.SysFont("comicsans", 30)
txtX, txtY = 10, 10
game_over_font = pygame.font.SysFont("comicsans", 64)


bulletIcon = pygame.image.load("bullet.png")
enemyIcon = pygame.image.load("enemy.png")
over = False

def game_over(over):
    overText = game_over_font.render("GAME OVER", 1, (255, 255, 255))
    screen.blit(overText, ((WIDTH - overText.get_width()) // 2, (HEIGHT - overText.get_height()) // 2))

    pygame.mixer.music.load("Angry 60 02.mp3")
    pygame.mixer.music.play(-1)

    playAgainTxt = font.render("Press to play again",1, (255, 255, 255))
    paX = (WIDTH - playAgainTxt.get_width()) // 2
    paY = 200
    screen.blit(playAgainTxt, (paX, paY))
    pygame.display.update()


    while over:
        for nevent in pygame.event.get():

            if nevent.type == pygame.QUIT:
                return False
            if nevent.type == pygame.MOUSEBUTTONDOWN:
                if paX + playAgainTxt.get_width() >= pygame.mouse.get_pos()[0] >= paX and paY + playAgainTxt.get_height() >= pygame.mouse.get_pos()[1] >= paY:
                    return True




def player(x, y):
    screen.blit(playerIcon, (x, y))


def enemy(x, y):
    screen.blit(enemyIcon, (x, y))


def bullet(x, y):
    global bulletState
    screen.blit(bulletIcon, (x, y))


def score_text(x, y, score_value):
    score = font.render("Score: " + str(score_value), 1, (255, 255, 255))
    screen.blit(score, (x, y))


def enemy_hit(x1, y1, x2, y2):
    # 1 - enemy 2 - bullet
    global enemyIcon
    global bulletIcon
    if y1 <= y2 <= y1 + enemyIcon.get_height() and x2 + bulletIcon.get_width() >= x1 >= x2 - enemyIcon.get_width():
        return True
    else:
        return False


def main(playerX, playerY, score_value, left, right, bulletIcon, over):
    over = False
    # Enemy
    enemyIcon = pygame.image.load("enemy.png")
    enemyX = []
    enemyY = []
    enemyMovRight = []
    enemyNum = 6

    for i in range(enemyNum):
        enemyX.append(random.randint(0, WIDTH - enemyIcon.get_width()))
        enemyY.append(random.randint(0, 100))
        enemyMovRight.append(True)
    enemyVel = 8

    # Sounds
    pygame.mixer.music.load("Gaming.mp3")
    pygame.mixer.music.play(-1)
    shootSound = pygame.mixer.Sound("laserShoot.wav")
    explosionSound = pygame.mixer.Sound("explosion.wav")
    playerExplosion = pygame.mixer.Sound("playerexplosion.wav")

    # bullet
    bulletIcon = pygame.image.load("bullet.png")
    bulletX, bulletY = playerX + 16, playerY + 10
    bulletVel = 30
    bulletState = "ready"
    running = True
    while running:
        # start
        screen.blit(background, (0, 0))
        pygame.time.Clock().tick(60)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_SPACE and bulletState == "ready":
                    shootSound.play()
                    bulletState = "fire"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
        if right and playerX <= WIDTH - playerIcon.get_width():
            playerX += PLAYER_VEL
        if left and playerX >= 0:
            playerX -= PLAYER_VEL

        # bullet movement
        if bulletY > bulletIcon.get_height() and bulletState == "fire":
            bulletY -= bulletVel
        else:
            bulletState = "ready"
            bulletX = playerX + 16
            bulletY = playerY

        # sprites
        bullet(bulletX, bulletY)
        player(playerX, playerY)

        # score
        for i in range(enemyNum):
            if enemyY[i] >= playerY - 70:
                playerExplosion.play()
                for j in range(enemyNum):
                    enemyY[j] = 2000
                pygame.mixer.music.fadeout(1)
                over = True
                break

            if enemy_hit(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletState = "ready"
                score_value += 1
                bulletX = playerX + 16
                bulletY = playerY
                enemyX[i], enemyY[i] = random.randint(0, WIDTH - enemyIcon.get_width()), random.randint(0, 100)
                explosionSound.play()

            # Enemy movement
            if enemyMovRight[i]:
                if enemyX[i] < WIDTH - enemyIcon.get_width():
                    enemyX[i] += enemyVel
                else:
                    enemyMovRight[i] = False
            else:
                if enemyX[i] > 0:
                    enemyX[i] -= enemyVel
                else:
                    enemyMovRight[i] = True

            enemyY[i] += enemyVel / 7
            enemy(enemyX[i], enemyY[i])

        # display update
        score_text(txtX, txtY, score_value)
        pygame.display.update()
        if over:
            running = game_over(over)
            break
    if running == True:
        main(playerX, playerY, 0, left, right, bulletIcon, over)






main(playerX, playerY, score_value, left, right, bulletIcon, over)