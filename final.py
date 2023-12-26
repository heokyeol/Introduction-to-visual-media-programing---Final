import pygame
import random
import numpy as np
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

gap = 50
WIDTH = gap*17
HEIGHT = gap*17
CENTER = [WIDTH/2, HEIGHT/2]
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("INeedHighCGPA")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def backgroundMaker():
    screen.fill((0,0,30))    
    for i in range(array.row):
        for j in range(array.column):
            screen.blit(background_img, (i*gap, j*gap))
    pygame.draw.rect(screen,BLACK,(CENTER[0]-gap/2-5,CENTER[1]-gap/2-5,gap+10,gap+10))

def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    surf.blit(text_surface, text_rect)

def degitToDot(num, size, space, x, y):
    cod_x = x
    cod_y = y
    str_num = str(num)
    for i in str_num:
        filename = 'words/dot_{}.png'.format(i.upper())
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        img = pygame.transform.scale(img, (size, size))
        screen.blit(img, (cod_x, cod_y))
        cod_x = cod_x + space

    
def WarningMessage(state, time):
    size = 40
    if state == 'Attending':
        return 'Attending'
    elif state == 'Academic Probation':
        timeGap = pygame.time.get_ticks()- time
        if (timeGap < 500) or (800 < timeGap < 1300) or (1600 < timeGap < 2100):
            pygame.draw.rect(screen,RED,(0,CENTER[1]-400,WIDTH,200))
            text = 'Academic Probation'
            degitToDot(text, size/2, size/2, CENTER[0]-size/2*len(text)/2, CENTER[1]-360)
            text = 'warning:Three F'
            degitToDot(text, size, size, CENTER[0]-size*len(text)/2, CENTER[1]-300)
            return 'Academic Probation'
        elif timeGap<2100 :
            return 'Academic Probation'
        else: 
            return 'first warning announced'
    elif state == 'Dismissal Warning':
        timeGap = pygame.time.get_ticks()- time
        if (timeGap < 500) or (800 < timeGap < 1300) or (1600 < timeGap < 2100):
            pygame.draw.rect(screen,RED,(0,CENTER[1]-400,WIDTH,200))
            text = 'Dismissal Warning'
            degitToDot(text, size/2, size/2, CENTER[0]-size/2*len(text)/2, CENTER[1]-360)
            text = 'No more F!!!'
            degitToDot(text, size, size, CENTER[0]-size*len(text)/2, CENTER[1]-300)
            return 'Dismissal Warning'
        elif timeGap<2100 :
            return 'Dismissal Warning'
        else: 
            return 'second warning announced'
    elif state == 'Dismissal':
        button("Dismissal", CENTER[0], CENTER[1], 400, 100, BLACK, YELLOW, RED, gameClose)
        return 'Dismissal'
    else: return state

def endingScene(text):
    button(text, CENTER[0], CENTER[1]+200, 400, 100, BLACK, YELLOW, RED, gameClose)
    pygame.draw.rect(screen,YELLOW,(0,CENTER[1]-200,WIDTH,200))
    size = 50
    text = 'A+:'+str(score_count[0])+' a:'+str(score_count[1])+' b:'+str(score_count[2])+' c:'+str(score_count[3])+' f:'+str(score_count[4])
    degitToDot(text, size/2, size/2, CENTER[0]-size/2*len(text)/2, CENTER[1]-170)
    text = 'CGPA:'+str(round(CGPA, 2))+'  earned:'+str(count)
    degitToDot(text, size/2, size/2, CENTER[0]-size/2*len(text)/2, CENTER[1]-130)
    
    if clear == True:
        text = 'doctor. sogang univ.'
    elif doctor == True:
        text = 'master. sogang univ.'
    elif master == True:
        text = 'bachelor. sogang univ'
    else :
        text = 'undergraduate'
    degitToDot(text, size/3*2, size/3*2, CENTER[0]-size/3*2*len(text)/2, CENTER[1]-70)

def gameClose():
    pygame.quit()

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def player_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x-1, y-1, BAR_LENGTH+2, BAR_HEIGHT+2)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, YELLOW, outline_rect)
    pygame.draw.rect(surf, (100,0,100), fill_rect)

def button(txt, x, y, w, h, tc, ic, ac, action = None):
    textSize = 30
    backgroundMaker()  
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w/2>mouse[0]>x-w/2 and y+h/2>mouse[1]>y-h/2:
        pygame.draw.rect(screen, ac, (x-w/2,y-h/2,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x-w/2,y-h/2,w,h))
    # draw_text(screen, txt, 30, WHITE, x, y)
    degitToDot(txt, textSize, textSize, CENTER[0]-textSize*len(txt)/2, y-textSize/2)



def CGPAcalculator(CGPA, mob, count):
    score = CGPA
    if count==0:
        # score = (score*(count-1) + mob.score)/count
        score = score_list[mob.ident]
    else:
        score = (CGPA+score_list[mob.ident])/2
    if score>4.3:
        score = 4.3
    return score

class position():
    def __init__(self):
        self.row = 0
        self.column = 0

class posArray():
    def __init__(self):
        self.row = int(HEIGHT/(gap*2))*2+1
        self.column = int(WIDTH/(gap*2))*2+1
        self.slot = np.zeros((self.row,self.column), dtype=int) #0:null, 1:core, 2:bolck, 3:player
        self.blockedSlot = []

        self.playerPos = position()
        self.playerPos.row = int(self.row/2)-1
        self.playerPos.column = int(self.column/2)
        
        self.corePos = position()
        self.corePos.row = int(self.row/2)
        self.corePos.column = int(self.column/2)
        self.slot[self.corePos.row, self.corePos.column] = 1


    def update(self, walls):
        self.slot = np.zeros((self.row,self.column), dtype=int) #0:null, 1:core, 2:bolck, 3:player
        # self.slot[self.row/2+1,self.column/2+1] = 1
        self.slot[self.corePos.row, self.corePos.column] = 1
        # for block in self.blockedSlot:
        #     self.slot[block[0], block[1]] = 2
        for wall in walls:
            self.slot[int(wall.rect.y/gap), int(wall.rect.x/gap)] = 2
        self.slot[self.playerPos.row,self.playerPos.column] = 3

        player.posUpdate()

class Core(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(core_img, (gap, gap))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = array.corePos.column*gap
        self.rect.y = array.corePos.row*gap


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_opend_img, (gap, gap))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.dir = "left"

        self.rect.x = array.corePos.column*gap
        self.rect.y = array.playerPos.row*gap

        self.speedx = 0
        self.shield = 100
        self.eat = False
        self.eatTime = pygame.time.get_ticks()
    
    def posUpdate(self):
        self.rect.x = array.playerPos.column*gap
        self.rect.y = array.playerPos.row*gap
        if self.dir == "left":
            self.image =  pygame.transform.scale(player_opend_img, (gap, gap))
        elif self.dir == "right":
            self.image = pygame.transform.flip(pygame.transform.scale(player_opend_img, (gap, gap)), True, False)

    def update(self):
        if self.eat == True:
            timeGap = pygame.time.get_ticks() - self.eatTime
            if timeGap < 100 or 200<timeGap<300 or 300<timeGap<400:
                if self.dir == "left":
                    self.image =  pygame.transform.scale(player_closed_img, (gap, gap))
                elif self.dir == "right":
                    self.image = pygame.transform.flip(pygame.transform.scale(player_closed_img, (gap, gap)), True, False)
            elif timeGap<400:
                if self.dir == "left":
                    self.image =  pygame.transform.scale(player_opend_img, (gap, gap))
                elif self.dir == "right":
                    self.image = pygame.transform.flip(pygame.transform.scale(player_opend_img, (gap, gap)), True, False)
            else:
                if self.dir == "left":
                    self.image =  pygame.transform.scale(player_opend_img, (gap, gap))
                elif self.dir == "right":
                    self.image = pygame.transform.flip(pygame.transform.scale(player_opend_img, (gap, gap)), True, False)
                self.eat = False

    def eat(self):
        if self.dir == "left":
            self.image =  pygame.transform.scale(player_closed_img, (gap, gap))
        elif self.dir == "right":
            self.image = pygame.transform.flip(pygame.transform.scale(player_closed_img, (gap, gap)), True, False)

    def block(self):
        wall = Wall(self.rect.center)
        all_sprites.add(wall)
        walls.add(wall)
        block_sound.play()

class Cap(pygame.sprite.Sprite):
    def __init__(self, ident):
        pygame.sprite.Sprite.__init__(self)
        self.ident = ident
        self.image = pygame.transform.scale(cap_image, (gap, gap))
        self.rect = self.image.get_rect()
        self.rect.centerx = -100
        self.rect.bottom = -100
    def update(self):
        if (master == True) and (self.ident == 'master'):
            self.rect.centerx = player.rect.centerx
            self.rect.bottom = player.rect.y
        elif (doctor == True) and (self.ident == 'doctor'):
            self.rect.centerx = player.rect.centerx
            self.rect.bottom = player.rect.y - 20


class Wall(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall_img
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -10
        self.corner = False
        self.slot = [int(self.rect.y/gap), int(self.rect.x/gap)]
        self.surround = [0, 0, 0, 0]
        if  (self.slot[1] == self.slot[0]):
            self.image = pygame.transform.rotate(self.image, -45)
        elif (self.slot[0]+self.slot[1] == int(HEIGHT/(gap*2))*2):
            self.image = pygame.transform.rotate(self.image, 45)
        elif (self.slot[1] > self.slot[0]) and (self.slot[0]+self.slot[1] < int(HEIGHT/(gap*2))*2):
            self.image = pygame.transform.rotate(self.image, 90)
        elif (self.slot[1] < self.slot[0]) and (self.slot[0]+self.slot[1] > int(HEIGHT/(gap*2))*2):
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect.center = center

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ident = np.random.randint(0,5)
        self.image_orig = meteor_images[self.ident]
        # self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.score = 4.3-self.ident*0.3
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)

        self.dist = 1.5
        self.ang = random.uniform(0, 2*np.pi)
        self.rect.x = CENTER[0] + (WIDTH/2)*np.cos(self.ang)*self.dist
        self.rect.y = CENTER[1] + (WIDTH/2)*np.sin(self.ang)*self.dist
        self.speed = random.randrange(5,10)*0.001
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)
        self.last_update = pygame.time.get_ticks()
        self.tail = Tail(np.rad2deg(self.ang), self.ident, self.rect.center)
        all_sprites.add(self.tail)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.tail.rect.centerx = self.rect.centerx+(self.image.get_width()/2+self.tail.image.get_width()/4)*np.cos(self.ang)
        self.tail.rect.centery = self.rect.centery+(self.image.get_height()/2+self.tail.image.get_height()/4)*np.sin(self.ang)
        
        self.dist -= self.speed
        self.rect.centerx = CENTER[0] + (WIDTH/2)*np.cos(self.ang)*self.dist
        self.rect.centery = CENTER[1] + (WIDTH/2)*np.sin(self.ang)*self.dist

class Tail(pygame.sprite.Sprite):
    def __init__(self, angle, ident, center):
        pygame.sprite.Sprite.__init__(self)
        # self.angle = angle
        self.ident = ident-1
        if self.ident == -1:
            self.ident = 0
        self.anim = []
        for i in range(len(tail_anim[self.ident])):
            self.anim.append(pygame.transform.rotate(tail_anim[self.ident][i], 90-angle).convert_alpha())
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        # self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim):
                self.frame = 0
            else:
                self.image = self.anim[self.frame]
                self.rect = self.image.get_rect()
        
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x,y, ident):
        pygame.sprite.Sprite.__init__(self)
        self.ident = ident-1
        if self.ident == -1:
            self.ident = 0
        self.image = crash_anim[self.ident][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(crash_anim[self.ident]):
                self.kill()
            else:
                x = self.rect.x
                y = self.rect.y
                self.image = crash_anim[self.ident][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

class Scored(pygame.sprite.Sprite):
    def __init__(self, center, ident, ang):
        pygame.sprite.Sprite.__init__(self)
        self.ang = ang
        self.ident = ident
        self.origImage = pygame.transform.rotate(meteor_images[self.ident], self.ang)
        self.whiteImage = pygame.transform.rotate(white_images[self.ident], self.ang)
        self.image = self.origImage
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 5:
                self.kill()
            else:
                center = self.rect.center
                if self.frame % 2 == 1:
                    self.image = self.whiteImage
                else :
                    self.image = self.origImage
                self.rect = self.image.get_rect()
                self.rect.center = center

# Load all game graphics
# background = pygame.image.load(path.join(img_dir, "Toon Road Texture.png")).convert()
# background = pygame.transform.scale(background, (1000,800))
# background_rect = background.get_rect()
background_img = pygame.image.load(path.join(img_dir, "dot_background.png")).convert_alpha()
background_img = pygame.transform.scale(background_img, (gap,gap))
core_img = pygame.image.load(path.join(img_dir, "monitor.png")).convert_alpha()
player_opend_img = pygame.image.load(path.join(img_dir, "player_opened.png")).convert_alpha()
player_closed_img = pygame.image.load(path.join(img_dir, "player_closed.png")).convert_alpha()
cap_image = pygame.image.load(path.join(img_dir, "cap.png")).convert_alpha()
wall_img = pygame.image.load(path.join(img_dir, "wall.png")).convert_alpha()
wall_corner_img = pygame.image.load(path.join(img_dir, "wall_corner.png")).convert_alpha()
wall_img = pygame.transform.scale(wall_img, (gap,gap))
wall_corner_img = pygame.transform.scale(wall_corner_img, (gap,gap))
core_img = pygame.transform.scale(core_img, (gap,gap))
score_list = [4.3, 4.0, 3.4, 2.8, 1.0]
meteor_images = []
meteor_list = ['dot_A+.png', 'dot_A.png', 'dot_B.png',
               'dot_C.png', 'dot_F.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    meteor_images[-1] = pygame.transform.scale(meteor_images[-1], (gap,gap))

white_images = []
white_list = ['white_A+.png', 'white_A.png', 'white_B.png',
               'white_C.png', 'white_F.png']
for img in white_list:
    white_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    white_images[-1] = pygame.transform.scale(white_images[-1], (gap,gap))


crash_anim = []
list = "ABCF"
for i, credit in enumerate(list):
    filename = 'crash_{}'.format(credit)
    crash_anim.append([])
    tail_dir = path.join(img_dir, filename)
    for j in range(5):
        filename = 'crash_{}.png'.format(j+1)
        img = pygame.image.load(path.join(tail_dir, filename)).convert_alpha()
        img.set_colorkey(BLACK)
        img = pygame.transform.scale(img, (gap, gap*2))
        crash_anim[i].append(img)

tail_anim = []
list = "ABCF"
for i, credit in enumerate(list):
    filename = 'tail_{}'.format(credit)
    tail_anim.append([])
    tail_dir = path.join(img_dir, filename)
    for j in range(5):
        filename = 'tail_{}.png'.format(j+1)
        img = pygame.image.load(path.join(tail_dir, filename)).convert_alpha()
        img.set_colorkey(BLACK)
        img = pygame.transform.scale(img, (75, 75))
        tail_anim[i].append(img)

# Load all game sounds
block_sound = pygame.mixer.Sound(path.join(snd_dir, 'block.wav'))
expl_sounds = pygame.mixer.Sound(path.join(snd_dir, 'expl.wav'))
eat_sound = pygame.mixer.Sound(path.join(snd_dir, 'Punch2__009.wav'))
scored_sound = pygame.mixer.Sound(path.join(snd_dir, 'scored.wav'))
scored_F_sound = pygame.mixer.Sound(path.join(snd_dir, 'scored_F.wav'))

pygame.mixer.music.load(path.join(snd_dir, 'Long Away Home.wav'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
array = posArray()
mobs = pygame.sprite.Group()
walls = pygame.sprite.Group()
player = Player()
master_cap = Cap(ident='master')
doctor_cap = Cap(ident='doctor')
core = Core()

all_sprites.add(player)
all_sprites.add(core)
all_sprites.add(master_cap)
all_sprites.add(doctor_cap)
newmob()


CGPA = 0
score = 0
count = 0
time = 0
F_count = 0
score_count = [0, 0, 0, 0, 0]
warning_time = 0
levelUpTiming = 1000
pygame.mixer.music.play(loops=-1)
# Game loop
running = True
clear = False
die = False
master = False
doctor = False
warning_state = 'Attending'

while running:
    time += 1
    if time%levelUpTiming == 0:
        levelUpTiming *= 3
        newmob()
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.dir = "left"
                target = array.playerPos.column - 1
                if array.slot[array.playerPos.row, target] == 0:
                    array.playerPos.column = target
            if event.key == pygame.K_RIGHT:
                player.dir = "right" 
                target = array.playerPos.column + 1
                if array.slot[array.playerPos.row, target] == 0:
                    array.playerPos.column = target
            if event.key == pygame.K_UP:
                target = array.playerPos.row - 1
                if array.slot[target, array.playerPos.column] == 0:
                    array.playerPos.row = target
            if event.key == pygame.K_DOWN:
                target = array.playerPos.row + 1
                if array.slot[target, array.playerPos.column] == 0:
                    array.playerPos.row = target
            if event.key == pygame.K_SPACE:
                player.block()
            array.update(walls=walls)

    # Update
    all_sprites.update()

    # check to see if a wall hit a mob
    hits = pygame.sprite.groupcollide(mobs, walls, True, True)
    for hit in hits:
        hit.tail.kill()
        score += 50 - hit.radius
        expl_sounds.play()
        expl = Explosion(hit.rect.x, hit.rect.y, hit.ident)
        all_sprites.add(expl)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        hit.tail.kill()
        eat_sound.play()
        player.shield -= 10
        expl = Explosion(hit.rect.x, hit.rect.y, hit.ident)
        player.eatTime = pygame.time.get_ticks()
        player.eat = True
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            die = True
    
    # check to see if a mob hit the core
    hits = pygame.sprite.spritecollide(core, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        hit.tail.kill()
        if hit.ident == 4:
            scored_F_sound.play()
        else:
            scored_sound.play()
            count += random.randint(1,3)
        expl = Scored(hit.rect.center, hit.ident, hit.rot)
        all_sprites.add(expl)
        score_count[hit.ident] += 1
        CGPA = CGPAcalculator(CGPA, hit, count)
        newmob()
    if (score_count[4] == 3) and (warning_state == 'Attending'):
        warning_time = pygame.time.get_ticks()
        warning_state = 'Academic Probation'
    elif (score_count[4] == 5) and (warning_state == 'first warning announced'):
        warning_time = pygame.time.get_ticks()
        warning_state = 'Dismissal Warning'
    elif (score_count[4] == 6) and (warning_state == 'second warning announced'):
        warning_state = 'Dismissal'
    
    if count >= 390:
        clear = True
    elif count >= 260:
        doctor = True
    elif count >= 130:
        master = True
    
        
    # Draw / render
    backgroundMaker()
    if warning_state == 'Dismissal':
        all_sprites.empty()
        endingScene("Dismissal")
    elif die == True:
        all_sprites.empty()
        endingScene("game over")
    elif clear == True:
        all_sprites.empty()
        endingScene("game clear")
    else:
        all_sprites.draw(screen)
        #CGPA
        degitToDot(round(CGPA,2), 17, 10, CENTER[0]-24, CENTER[1]-7)
        #credit earned
        pygame.draw.rect(screen, YELLOW, (CENTER[0]-125,10,250,30))
        degitToDot('earned:'+str(count), 20, 20, CENTER[0]-len('earned:   ')*17/2, 15)
        warning_state = WarningMessage(warning_state, warning_time)
        player_shield_bar(screen, 5, 5, player.shield)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
