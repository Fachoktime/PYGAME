import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Mario", "mariorun(1).png")),
           pygame.image.load(os.path.join("Assets/Mario", "mariorun(2).png")),
           pygame.image.load(os.path.join("Assets/Mario", "mariorun(3).png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Mario", "mariorun(1).png"))

GOOOMBA = [pygame.image.load(os.path.join("Assets/DONT TOUCH IT!!!", "goomba(11).png")),
           pygame.image.load(os.path.join("Assets/DONT TOUCH IT!!!", "goomba(21).png"))]
PIPE = [pygame.image.load(os.path.join("Assets/DONT TOUCH IT!!!", "pipe(4).png")),
        pygame.image.load(os.path.join("Assets/DONT TOUCH IT!!!", "bananas(1).png")),]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud(3).png"))

BG = pygame.image.load(os.path.join("Assets/Other", "background.png"))


class Mario:
    X_POS = 80
    Y_POS = 488
    JUMP_VEL = 10

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.mario_run = True
        self.mario_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_POS
        self.mario_rect.y = self.Y_POS

    def update(self, userInput):
        if self.mario_run:
            self.run()
        if self.mario_jump:
            self.jump()

        if self.step_index >= 15:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.mario_jump:
            self.mario_run = False
            self.mario_jump = True
        elif not self.mario_jump :
            self.mario_run = True
            self.mario_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_POS
        self.mario_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.mario_jump:
            self.mario_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.6
        if self.jump_vel < - self.JUMP_VEL:
            self.mario_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.mario_rect.x, self.mario_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH +random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image =CLOUD
        self.width = self.image.get_width()
    def update (self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Gooombas(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 570

class Pipes(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 580

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Mario()
    game_speed = 12
    x_pos_bg=0
    y_pos_bg=0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Gooombas(GOOOMBA))
            elif random.randint(0, 2) == 1:
                obstacles.append(Pipes(PIPE))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.mario_rect.colliderect(obstacle.rect):#pygame.draw.rect(SCREEN, (255,0,0), player.mario_rect, 2)
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        player.draw(SCREEN)
        player.update(userInput)

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(60)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 -40, SCREEN_HEIGHT // 2 - 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


menu(death_count=0)
