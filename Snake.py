import pygame as pg #1.9.4
import random
import os

os.environ['SDL_VIDEO_CENTERED']='1'

WIDTH=800
HEIGHT=600
FPS=15

pg.init()

pg.display.set_caption("Pygame2")
screen=pg.display.set_mode((WIDTH,HEIGHT),pg.RESIZABLE,32)#|pg.FULLSCREEN

WIDTH,HEIGHT=screen.get_size()

running=True
clock=pg.time.Clock()

alpha=0

square_size=(20,20)

background=pg.Surface((WIDTH,HEIGHT))



for y in range(int(HEIGHT/square_size[0])+1):
    for x in range(int(WIDTH/square_size[1])+1):
        pg.draw.rect(background,(alpha,alpha,alpha),(x*square_size[0]-square_size[0],y*square_size[0]-square_size[1],x*square_size[0]+square_size[0],y*square_size[0]+square_size[1]))        
        alpha+=200/((WIDTH/square_size[0])*(HEIGHT/square_size[1]))
        #alpha=random.randint(10,230)

"""
def text(surface,text=""):
    pg.font.SysFont('mono',24,italic=True)
    fw,fh=pg.font.size(text)
    surface1=pg.font.render(text,True,(255,255,255))
    surface.blit(surface1,(50,150))
"""

class Snake:
    snake_location=[[80,80]]
    directions={"Left":(-1,0),"Right":(1,0),"Up":(0,-1),"Down":(0,1)}
    direction=directions["Right"]
    fruit_location=(80,40)
    length=3
    last_length=0
    size_of_increase=3

    def __init__(self,location=[[80,80]],direction=directions["Right"],size_of_increase=3):
        self.location=location
        self.direction=direction
        self.fruit_location=(random.randint(1,WIDTH/square_size[0]-1)*square_size[0],random.randint(1,HEIGHT/square_size[1]-1)*square_size[1])
        self.size_of_increase=size_of_increase

    def controlls(self):
        running=True
        i=0
        
        for events in pg.event.get(pg.KEYDOWN):
            if events.type==pg.QUIT:
                running=False

            elif events.type==pg.KEYDOWN:
                pg.event.clear()
                if events.key==pg.K_ESCAPE:
                    running=False
                if events.key==pg.K_LEFT and (self.direction!=self.directions["Right"] or self.length==0):
                    self.direction=self.directions["Left"]
                    break
                if events.key==pg.K_RIGHT and (self.direction!=self.directions["Left"] or self.length==0):
                    self.direction=self.directions["Right"]
                    break
                if events.key==pg.K_UP and (self.direction!=self.directions["Down"] or self.length==0):
                    self.direction=self.directions["Up"]
                    break
                if events.key==pg.K_DOWN and (self.direction!=self.directions["Up"] or self.length==0):
                    self.direction=self.directions["Down"]
                    break
        return running

    def update_location(self):
           if self.last_length!=self.length:
               self.snake_location.append(self.snake_location[self.last_length])
               self.last_length+=1
            
           for i in range(self.last_length,0,-1):
               self.snake_location[i]=self.snake_location[i-1]

           self.snake_location[0]=[self.direction[0]*square_size[0]+self.snake_location[0][0],self.direction[1]*square_size[1]+self.snake_location[0][1]]
     
          
           

    def draw(self,surface):
        pg.draw.rect(surface,(255,0,0),(self.fruit_location,square_size))

        for i in range(self.last_length+1):
           pg.draw.rect(surface,(255,255,255),(self.snake_location[i],square_size))
         

    def fruit(self):
           if self.fruit_location[0]==self.snake_location[0][0] and self.fruit_location[1]==self.snake_location[0][1]:

              self.fruit_location=(random.randint(1,WIDTH/square_size[0]-1)*square_size[0],random.randint(1,HEIGHT/square_size[1]-1)*square_size[1])
              i=0
              while i<self.last_length+1:
                 while self.fruit_location[0]==self.snake_location[i][0] and self.fruit_location[1]==self.snake_location[i][1]:
                    self.fruit_location=(random.randint(1,WIDTH/square_size[0]-1)*square_size[0],random.randint(1,HEIGHT/square_size[1]-1)*square_size[1])
                    i=0
                 i+=1

              self.length+=self.size_of_increase
             
    def collision(self,surface):
        if self.snake_location[0][0]<0 or self.snake_location[0][0]>WIDTH-square_size[0]:
            print("Score=",self.length)  
            if len(self.snake_location)!=1:
                pg.draw.rect(surface,(255,255,0),(self.snake_location[1],square_size))
                pg.display.update(pg.Rect(self.snake_location[1],square_size))
            #pg.display.quit()
            os.system("pause")
            quit() 

        if self.snake_location[0][1]<0 or self.snake_location[0][1]>HEIGHT-square_size[1]:
            print("Score=",self.length)
            if len(self.snake_location)!=1:
                  pg.draw.rect(surface,(255,255,0),(self.snake_location[1],square_size))
                  pg.display.update(pg.Rect(self.snake_location[1],square_size))
            #pg.display.quit()
            os.system("pause")
            quit() 
         
        for i in range(self.last_length,0,-1):
            if self.snake_location[0]==self.snake_location[i]:
                print("Score=",self.length)
                pg.draw.rect(surface,(255,255,0),(self.snake_location[0],square_size))
                pg.display.update(pg.Rect(self.snake_location[0],square_size))
                #pg.display.quit()
                os.system("pause")
                quit()         


snake=Snake([[400,300]])

while running==True:


    #screen.fill((0,0,0))
    screen.blit(background,(0,0))

    running=snake.controlls()
    
    snake.update_location()
    snake.collision(screen)
    snake.draw(screen)

   
    snake.fruit()


    pg.display.flip()
    clock.tick(FPS)
    #clock.tick_busy_loop(FPS)#It use more CPU for more accurate fps
