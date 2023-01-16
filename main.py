import pygame
import button
import os
import cv2

pygame.init()

#create game window
win_width = 800
win_height = 480

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dog VS Zombie")

# Load and Size Images
# Hero (Player)
left = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L1.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L2.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L3.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L4.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L5.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L6.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L7.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L8.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "L9.png")), (82, 60))
        ]
right =[pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R1.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R2.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R3.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R4.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R5.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R6.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R7.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R8.png")), (82, 60)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "R9.png")), (82, 60))
        ]
# Enemy
left_enemy = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L1E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L2E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L3E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L4E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L5E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L6E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L7E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L8E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L9P.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L10P.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "L11P.png")), (100, 99)),
        ]
right_enemy = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R1E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R2E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R3E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R4E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R5E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R6E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R7E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R8E.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R9P.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R10P.png")), (100, 99)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Enemy", "R11P.png")), (100, 99))
        ]
# Bullet
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (15, 15))
# Background
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "BG.png")), (win_width, win_height))
# Tower
tower = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Group 25.png")), (225,181))
# Music/Sounds
music = pygame.mixer.music.load(os.path.join("Assets/Audio", "music.ogg"))
pop_sound = pygame.mixer.Sound(os.path.join("Assets/Audio", "pop.ogg"))
pygame.mixer.music.play(-1)

class Hero:
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 14
        self.vely = 8
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # Jump
        self.jump = False
        # Bullet
        self.bullets = []
        self.cool_down_count = 0
        # Health
        self.hitbox = (self.x, self.y, 129, 94)
        self.health = 30
        self.lives = 1
        self.alive = True

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x + 15, self.y + -100, 60, 94)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y, 30, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y, self.health, 10))
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        if userInput[pygame.K_UP] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely * 4
            self.vely -= 1
        if self.vely < -8:
            self.jump = False
            self.vely = 8

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def cooldown(self):
        if self.cool_down_count >= 10:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shoot(self):
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_SPACE] and self.cool_down_count == 0):
            pop_sound.play()
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < \
                        enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    player.bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 60
        self.y = y + 30
        self.direction = direction

    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 10
        if self.direction == -1:
            self.x -= 15

    def off_screen(self):
        return not (self.x >= 0 and self.x <= win_width)


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.stepIndex = 0
        # Health
        self.hitbox = (self.x, self.y, 155, 155)
        self.health = 40

    def step(self):
        if self.stepIndex >= 33:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x + 60, self.y + 0, 30, 155)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y, 40, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y, self.health, 10))
        self.step()
        win.blit(left_enemy[self.stepIndex // 3], (self.x, self.y))
        self.stepIndex += 1

    def move(self):
        self.hit()
        self.x -= speed


    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < \
                player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False

    def off_screen(self):
        return not (self.x >= -50 and self.x <= win_width + 50)

#Intro 
def intro():
    # importing libraries
    cap = cv2.VideoCapture('Assets\Tic Tac Toe Video.mp4')
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")
    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            cv2.imshow('Video', frame)
        # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    # Break the loop
        else:
            break
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

intro()

def draw_game():
    global tower_health, speed
    win.fill((0, 0, 0))
    win.blit(background, (0, 0))
    # Draw Player
    player.draw(win)
    # Draw Bullets
    for bullet in player.bullets:
        bullet.draw_bullet()
    # Draw Enemies
    for enemy in enemies:
        enemy.draw(win)
    # Draw Tower
    win.blit(tower, (-25, 270))
    # Player Health
    if player.alive == False:
        win.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You Died! Press R to restart', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (win_width // 2, win_height // 2)
        win.blit(text, textRect)
        if userInput[pygame.K_r]:
            player.alive = True
            player.lives = 1
            player.health = 30
            tower_health = 5
            speed = 5
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('Lives: ' + str(player.lives) + ' | Tower Health: '+ str(tower_health) + ' |Kills: '+ str(kills) + '|High Score:' + str(kills), True, (0, 0, 0, 0))
    win.blit(text, (50, 20))
    # Delay and Update
    pygame.time.delay(30)
    pygame.display.update()

# Instance of Hero-Class
player = Hero(160, 385)

# Instance of Enemy-Class
enemies = []
speed = 5
kills = 0

# Tower
tower_health = 5

#game variables
game_paused = True
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
play_img = pygame.image.load("Assets/button-img/button_play.png").convert_alpha()
quit_img = pygame.image.load("Assets/button-img/button_quit.png").convert_alpha()
back_img = pygame.image.load('Assets/button-img/button_back.png').convert_alpha()
tutorial_img = pygame.image.load('Assets/button-img/button_tutorial.png').convert_alpha()

#create button instances
play_button = button.Button(304, 70, play_img, 1)
quit_button = button.Button(336, 330, quit_img, 1)
back_button = button.Button(332, 375, back_img, 1)
tutorial_button = button.Button(297, 200, tutorial_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  win.blit(img, (x, y))

#game loop
run = True
while run:

  win.fill((0, 0, 0))
  win.blit(background, (0, 0))
  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause win buttons
      if play_button.draw(win):
        game_paused = False
      if tutorial_button.draw(win):
        menu_state = "tutorial"
      if quit_button.draw(win):
        run = False
    #check if the options menu is open
    if menu_state == "tutorial":
      #draw the different options buttons
      win.fill((0, 0, 0))
      win.blit(background, (0, 0))
      if back_button.draw(win):
        menu_state = "main"
  else:
    # Input
    userInput = pygame.key.get_pressed()

    # Shoot
    player.shoot()

    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)

    # Tower Health
    if tower_health == 0:
        player.alive = False

    # Enemy
    if len(enemies) == 0:
        enemy = Enemy(800, 345, speed)
        enemies.append(enemy)
        if speed <= 10:
            speed += 0.25
    for enemy in enemies:
        enemy.move()
        if enemy.off_screen() or enemy.health == 0:
            enemies.remove(enemy)
        if enemy.x < 50:
            enemies.remove(enemy)
            tower_health -= 1
        if enemy.health == 0:
            kills +=1

    # Draw Game in Window
    draw_game()
    
  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False
  
  pygame.display.update()

pygame.quit()