import pygame
from time import sleep
from pygame.locals import *
import random
#this imports the modules that are needed for the game 

pygame.init() #pygame is initialised 

clock = pygame.time.Clock()#timer is used to lock a frame rate so that the game runs at the same speed 
fps = 60 #frame rate for how fast the ground is moving 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#this is the height and width of the game screen in pixels 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#implements the screen 
pygame.display.set_caption("Flappy Bird")#gives the name of the game  

#all my game variables
ground_scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #miliseconds
last_pipe = pygame.time.get_ticks()



#load images
bg = pygame.image.load(r"sprites\bg.png") #the background image
ground = pygame.image.load(r"sprites\ground.png")#the ground image

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4): #pastes all my images of the flappy bird (i have 2)
           img = pygame.image.load(rf"sprites\flappybird{num}.png")
           self.images.append(img) 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0 #this is the velocity the bird will be travelling at
        self.clicked = False

    def update(self):
        #gravity
        if flying == True:
            self.velocity += 0.5
            if self.velocity >8:
                self.velocity =8
            if self.rect.bottom < 800:
                self.rect.y += int(self.velocity)

        if game_over ==False:
            #jumping motion
            if pygame.mouse.get_pressed()[0]==1 and self.clicked is False:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False

            #handle the animation, limits or controls the rate at which the animation cycles through
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]


            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index],self.velocity* -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)
        
#class for the pipes, or in my case the icicle
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"sprites\pipe.png")
        self.rect = self.image.get_rect()
        #positiion 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y- int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right <0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100,int(SCREEN_HEIGHT/2))
bird_group.add(flappy)

bg = pygame.image.load(r'sprites\bg.png')
ground_img = pygame.image.load(r'sprites\ground.png')


run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    bird_group.draw(screen)#calls function draw
    bird_group.update() #calls function update
    screen.blit(pygame.image.load(r'sprites\ground.png'), (ground_scroll,768)) #supposed to paste the ground
    pipe_group.draw(screen)#


    #collision with the pipes
    if pygame.sprite.groupcollide(bird_group, pipe_group,False, False) or flappy.rect.top < 0:
        game_over = True

    #check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False



    if game_over is False:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height,-1)  # this is the coordinates of where the bottom pipe is going to be
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)  # this is where the top pipe is going to be
            pipe_group.add(btm_pipe)  # prints the bottom icicle
            pipe_group.add(top_pipe)  # prints the top icicle
            last_pipe = time_now
        #draw background
        ground_scroll -= scroll_speed
        if abs(ground_scroll)> 35:   #moves the ground to the left making it seem like its scrolling
            ground_scroll = 0

        pipe_group.update()
    else:
        # Game over sequence


        sleep(1)
        run = False

    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()#updates the game every time I add something new

    



pygame.quit()




