import pygame
import random
pygame.init()

screen = pygame.display.set_mode([450, 600])
w, h = pygame.display.get_surface().get_size()
pygame.display.set_caption('Flappy Bird')
flappy_bird = pygame.image.load('bird.png')
bg = pygame.image.load('background.jpg')
top_pipe = pygame.image.load('top_pipe.png')
bottom_pipe = pygame.image.load('bottom_pipe.png')
flap = pygame.mixer.Sound('flap.wav')
point = pygame.mixer.Sound('point.wav')

class Bird(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.jumpCount = 3
        self.isJump = False

    def draw(self, screen):
        screen.blit(bg, (0, 0))
        screen.blit(flappy_bird, (self.x, self.y))

class Pipes(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8

    def draw(self, screen):
        screen.blit(top_pipe, (self.x, self.y))
        screen.blit(bottom_pipe, (self.x, self.y + 650))
        self.x -= self.vel

def redrawGameWindow():
    global score, running, neg
    bird.draw(screen)
    text = pygame.font.SysFont('comicsans', 40)
    data = text.render(str(score), 1, (255, 255, 255))
    screen.blit(data, (w // 2 - 40, h // 4 - 30))
    for pipe in pipes:
        pipe.draw(screen)
        if(pipe.x + 50 <= 0):
            pipes.pop(pipes.index(pipe))
        if (pipe.x == bird.x + bird.width):
            if((bird.y >= pipe.y + pipe.height) and (bird.y + bird.height <= pipe.y + pipe.height + 150)):
                score += 1
                point.play()
                break
            else:
                running = False

        if((bird.x + bird.width >= pipe.x) and (bird.x <= pipe.x + pipe.width)):
            if ((bird.y - 2 <= pipe.y + pipe.height) or (bird.y + bird.height + 2 >= pipe.y + pipe.height + 150)):
                running = False

running = True
game_over = False
bird = Bird(50, 300, 40, 40)
pipes = []
score = 0
neg = 1
font = pygame.font.SysFont('comicsans', 40, True)

def main_function():
    global running
    while running:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
        if(len(pipes) == 0):
            y = random.randrange(-450, -200, 1)
            pipes.append(Pipes(410, y, 50, 500))
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            bird.isJump = True
            flap.play()
            bird.jumpCount = 7
        else:
            neg = 1
            if (bird.jumpCount <= 0):
                neg = -1
            bird.y -= int((bird.jumpCount ** 2) * 0.5 * neg)
            bird.jumpCount -= 1
        if(bird.y + bird.height >= 570):
            running = False
        redrawGameWindow()
        pygame.display.update()

def start_game():
    global game_over, score
    run = True
    text = pygame.font.SysFont('comicsans', 40)
    data = text.render("Click space to start the game!", 1, (255, 255, 255))
    tutorial = text.render("Use space to jump", 1, (255, 255, 255))
    while run and not game_over:
        screen.blit(bg, (0, 0))
        screen.blit(data, (w // 2 - 200, h // 2 - 20))
        screen.blit(tutorial, (w // 2 - 200, h // 2 + 20))
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            main_function()
            game_over = True
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                game_over = True
                run = False
        pygame.display.update()

    game_over = False
    while not game_over:
        screen.blit(bg, (0, 0))
        go = text.render("Game Over!", 1, (255, 255, 255))
        screen.blit(go, (w // 2 - 200, h // 2 - 20))
        start_again = text.render("Press q to quit", 1, (255, 255, 255))
        score_text = text.render("Score: " + str(score), 1, (255, 255, 255))
        screen.blit(start_again, (w // 2 - 200, h // 2 + 20))
        screen.blit(score_text, (w // 2 - 200, h // 2 + 50))
        keys1 = pygame.key.get_pressed()
        if (keys1[pygame.K_q]):
            game_over = True
        pygame.event.pump()
        pygame.display.update()

if(not game_over):
    start_game()
pygame.quit()