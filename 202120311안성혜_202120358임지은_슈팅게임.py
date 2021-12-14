import pygame
import sys
import random
from time import sleep


padWidth = 480
padHeight = 640
virusImage = ['코로나.png', '보로나.png','큰보로나.png','큰코로나.png']
explosionSound = ['때리는 전자 효과음3.mp3','곤장 맞는 소리.mp3']

def writeScore(count):
    global gamePad
    font = pygame.font.Font('MaruBuri-Bold.ttf', 20)
    text = font.render('Score: ' + str(count), True, (0, 0, 0))
    gamePad.blit(text,(10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('MaruBuri-Bold.ttf', 20)
    text = font.render('miss : ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360,0))

def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('MaruBuri-Bold.ttf',80)
    text = textfont.render(text, True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage('돌파 감염!')

def gameOver():
    global gamePad
    writeMessage('Game Over!')

def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj, (x,y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('병원배경1.png')
    fighter = pygame.image.load('주사기3.png')
    missile = pygame.image.load('물방울1.png')
    explosion = pygame.image.load('터지는 바이러스.png')
    pygame.mixer.music.load('긴장-어두운 빠른 템포-A003.mp3')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('권총발사.mp3')
    gameOverSound = pygame.mixer.Sound('실패.mp3')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.8
    fighterX = 0

    missileXY = []

    virus = pygame.image.load(random.choice(virusImage))
    virusSize = virus.get_rect().size
    virusWidth = virusSize[0]
    virusHeight = virusSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    virusX = random.randrange(0,padWidth - virusWidth)
    virusY = 0
    virusSpeed = 2

    isShot = False
    shotCount = 0
    virusPassed = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0,0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        if y < virusY + virusHeight:
            if(virusX > x and virusX < x + fighterWidth) or \
                      (virusX + virusWidth > x and virusX + virusWidth < x + fighterWidth):
                crash()
                     
            

        drawObject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < virusY:
                    if bxy[0] > virusX and bxy[0] < virusX + virusWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        virusY += virusSpeed

        if virusY > padHeight:
            virus = pygame.image.load(random.choice(virusImage))
            virusSize = virus.get_rect().size
            virusWidth = virusSize[0]
            virusHeight = virusSize[1]
            virusX = random.randrange(0,padWidth - virusWidth)
            virusY = 0
            virusPassed += 1

        if virusPassed == 3:
            gameOver()

        writePassed(virusPassed)

        if isShot:
            drawObject(explosion,virusX, virusY)
            destroySound.play()

            virus = pygame.image.load(random.choice(virusImage))
            virusSize = virus.get_rect().size
            virusWidth = virusSize[0]
            virusHeight = virusSize[1]
            virusX = random.randrange(0,padWidth - virusWidth)
            virusY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

        drawObject(virus, virusX, virusY)
                
        pygame.display.update()

        clock.tick(60)
    pygame.quit()

initGame()
runGame()
