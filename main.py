# Lava_Rope
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

# initialize pygame
pygame.init()

#music
music = pygame.mixer.music.load('music/lavafrog.mp3')

# tile and grid size
TILE_SIZE = 32 # 32 by 32 squares

# screen width and height
SCREEN_WIDTH = TILE_SIZE*27
SCREEN_HEIGHT = TILE_SIZE*27

# rope class
class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Rope, self).__init__()
        """
        self.surf = pygame.Surface((32,34))
        self.surf.fill((170, 25, 25))
        """
        #picture
        self.surf = pygame.image.load("img/Rope.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center= (self.x, self.y))
        
    def update(self, direction):
        self.x = self.x + direction
        #temp = pygame.sprite.spritecollide(self, ropes, False)
        #print(temp)
        #if len(temp) < 2:
        #    self.x = self.x - direction
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# ropes group
ropes = pygame.sprite.Group()

# lava class
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Lava, self).__init__()
        self.surf = pygame.image.load(random.choice(lava_sprites)).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center= (self.x, self.y))
    def update(self):
        self.surf = pygame.image.load(random.choice(lava_sprites)).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

# lava sprites
lava_sprites = ("img/Lava1.png","img/Lava2.png")

# lavas group
lavas = pygame.sprite.Group()

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("img/frog1.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        self.x = int(SCREEN_WIDTH/2-16)
        self.y = SCREEN_HEIGHT-16
        self.rect = self.surf.get_rect(center= (self.x, self.y))
        
        self.land = True
        
    def update(self,x,y):
        self.surf = pygame.image.load("img/frog2.png").convert_alpha()
        self.land = False
        move_y = y-self.y
        move_x = x-self.x
        if move_y>0:
            move_y = min(y-self.y, 4)
        else:
            move_y = max(y-self.y, -4)
        if move_x > 0:
            move_x = min(x-self.x, 4)
        else:
            move_x = max(x-self.x, -4)
        
        self.x = self.x + move_x
        self.y = self.y + move_y
        #print(move_y)
        self.rect = self.surf.get_rect(center= (self.x, self.y))
        if (x!=self.x) or (y!=self.y):
            pygame.event.post(MOVE_P)
        else:
            self.surf = pygame.image.load("img/frog1.png").convert_alpha()
            self.land = True

# big frog
class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super(Frog, self).__init__()
        self.surf = pygame.image.load("img/bigFrog.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        self.x = int(SCREEN_WIDTH/2-16)
        self.y = SCREEN_HEIGHT-300
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# draw text
def draw_text(surface, text, size, color, x, y):  
    font = pygame.font.SysFont ("Times", size, bold = True)
    label = font.render (text, 1, color)
    
    surface.blit(label,(x,y))
    
# remove sprites
def remove_sprites():
    for lava in lavas:
        lava.kill()
    for rope in ropes:
        rope.kill()

# clock stuff
clock = pygame.time.Clock()
MOVE_ROPE = pygame.USEREVENT + 1
MOVE = pygame.event.Event(MOVE_ROPE)
LAVA_CHANGE = pygame.USEREVENT + 2
LAVA = pygame.event.Event(LAVA_CHANGE)
MOVE_PLAYER = pygame.USEREVENT + 3
MOVE_P = pygame.event.Event(MOVE_PLAYER)

def main(screen):
    # display screen
    #screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    for i in range(0,SCREEN_HEIGHT+1,32):
        for j in range(int(SCREEN_WIDTH/4-16), SCREEN_WIDTH-16, int(SCREEN_WIDTH/4)):
            rope = Rope(j,i)
            ropes.add(rope)
    for i in range(0,SCREEN_HEIGHT+17,32):
        for j in range(0,SCREEN_WIDTH+17,32):
            lava = Lava(j,i)
            lavas.add(lava)
    player = Player()
    
    running = True
    
    clicked=(0,0)
    
    while running:
        # mouse
        mouse = pygame.mouse.get_pos()
        # /mouse
        pygame.event.post(MOVE)
        if random.randint(1,10) < 4:
            pygame.event.post(LAVA)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return "quit"
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    return "neutral"
            if event.type == pygame.MOUSEBUTTONUP:
                #print('h')
                #print(mouse[0])
                if player.x - 72 < mouse[0] < player.x + 72:
                    if player.y - 72 < mouse[1] < player.y + 72:
                        #print("hi")
                        if player.land == True:
                            clicked = mouse
                            pygame.event.post(MOVE_P)
            if event.type == MOVE_PLAYER:
                #print('hi2')
                player.update(clicked[0], clicked[1])
            if event.type == MOVE_ROPE:
                for rope in ropes:
                    if rope.y>=SCREEN_HEIGHT:
                        continue
                    direction = random.choice((-5,-4,-3,-2,-1,0,1,2,3,4,5))
                    rope.update(direction)
            #"""
            if event.type == LAVA_CHANGE:
                #print("hi")
                for lava in lavas:
                    if random.randint(1,4) == 2:
                        lava.update()
            #"""
        #print (pygame.sprite.spritecollideany(player, ropes))
        if player.land == True:
            if not pygame.sprite.spritecollideany(player, ropes):
                running = False
                return "lost"
            elif player.y < 50:
                return "win"
        screen.fill((179,70,20))
        for lava in lavas:
            screen.blit(lava.surf,lava.rect)
        for rope in ropes:
            screen.blit(rope.surf,rope.rect)
        screen.blit(player.surf,player.rect)
        pygame.display.flip()
        clock.tick(32)
    #pygame.quit()

def main_menu():
    # display screen
    status = "neutral"
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    run = True
    frog = Frog()
    pygame.mixer.music.play(-1)
    while run:
        # mouse
        mouse = pygame.mouse.get_pos()
        # /mouse
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if int(SCREEN_WIDTH/2)-155 < mouse[0] < int(SCREEN_WIDTH/2)-155+300:
                    if 700 < mouse[1] < 800:
                        status = main(screen)
                        remove_sprites()
        
        if status == "quit":
            run = False
        screen.fill((179,70,20))
        b_surf = pygame.Surface((300,100))
        b_surf.fill((18,150,150))
        screen.blit(b_surf,(int(SCREEN_WIDTH/2)-155,700))
        if status == "lost":
            draw_text(screen, "YOU LOST!", 100, (0,0,0), 50, 20)
        elif status == "win":
            draw_text(screen, "YOU WIN!!!", 100, (0,0,0), 50, 20)
        else:
            draw_text(screen, "LAVA FROG", 100, (0,0,0), 50, 20)
        draw_text(screen, "WARNING: ACTIVE VOLCANO AND UNSTABLE PLATFORMS", 25, (200,200,0), 20, 140)
        draw_text(screen, "To play:", 40, (50,50,50), 100, 200)
        draw_text(screen, "Click near the frog", 40, (50,50,50), 150, 250)
        draw_text(screen, "The frog will jump to the mouse", 40, (50,50,50), 150, 300)
        draw_text(screen, "Stay on the platforms", 40, (50,50,50), 150, 350)
        draw_text(screen, "Guide to frog to the end!", 40, (50,50,50), 150, 400)
        draw_text(screen, "PLAY", 40, (0,0,150), 370, 725)
        screen.blit(frog.surf,frog.rect)
        pygame.display.flip()
    pygame.mixer.music.stop()
    pygame.quit()

pygame.display.set_caption('Lava Frog')
main_menu()






















