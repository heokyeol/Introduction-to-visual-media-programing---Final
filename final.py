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
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    # text_rect.x = x
    # text_rect.y = y
    text_rect.center = (x,y)
    surf.blit(text_surface, text_rect)

def degitToDot(num, size, x, y):
    cod_x = x
    cod_y = y
    str_num = str(num)
    for i in str_num:
        filename = 'dot_{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        img = pygame.transform.scale(img, (size, size))
        screen.blit(img, (cod_x, cod_y))
        cod_x = cod_x + 10
    

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
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def core_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 4.3) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def button(txt, x, y, w, h, tc, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w/2>mouse[0]>x-w/2 and y+h/2>mouse[1]>y-h/2:
        pygame.draw.rect(screen, ac, (x-w/2,y-h/2,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x-w/2,y-h/2,w,h))
    draw_text(screen, txt, 30, WHITE, x, y)

def CGPAcalculator(CGPA, mob, count):
    score = CGPA
    if count==0:
        # score = (score*(count-1) + mob.score)/count
        score = 4.3-mob.ident*0.3
    else:
        score = (CGPA+(4.3-mob.ident*0.3))/2
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


    def update(self, bullets):
        self.slot = np.zeros((self.row,self.column), dtype=int) #0:null, 1:core, 2:bolck, 3:player
        # self.slot[self.row/2+1,self.column/2+1] = 1
        self.slot[self.corePos.row, self.corePos.column] = 1
        # for block in self.blockedSlot:
        #     self.slot[block[0], block[1]] = 2
        for bullet in bullets:
            self.slot[int(bullet.rect.y/gap), int(bullet.rect.x/gap)] = 2
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
        self.shield = 4.3


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
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    
    def posUpdate(self):
        self.rect.x = array.playerPos.column*gap
        self.rect.y = array.playerPos.row*gap
        if self.dir == "left":
            self.image =  pygame.transform.scale(player_opend_img, (gap, gap))
        elif self.dir == "right":
            self.image = pygame.transform.flip(pygame.transform.scale(player_opend_img, (gap, gap)), True, False)

    def eat(self):
        if self.dir == "left":
            self.image =  pygame.transform.scale(player_closed_img, (gap, gap))
        elif self.dir == "right":
            self.image = pygame.transform.flip(pygame.transform.scale(player_closed_img, (gap, gap)), True, False)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.x, self.rect.y)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = -10
        self.slot = [int(self.rect.y/gap), int(self.rect.x/gap)]
        if self.slot[1] > self.slot[0] :
            if self.slot[0]+self.slot[1] < int(HEIGHT/(gap*2))*2:
                self.image = pygame.transform.rotate(self.image, 90)
        elif self.slot[1] < self.slot[0] :
            if self.slot[0]+self.slot[1] > int(HEIGHT/(gap*2))*2+1 :
                self.image = pygame.transform.rotate(self.image, 90)
    def update(self):
        if self.rect.bottom < 0:
            self.kill()

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

        self.dist = 1
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
        self.frame_rate = 50

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
core_img = pygame.image.load(path.join(img_dir, "monitor.png")).convert_alpha()
player_opend_img = pygame.image.load(path.join(img_dir, "player_opened.png")).convert_alpha()
player_closed_img = pygame.image.load(path.join(img_dir, "player_closed.png")).convert_alpha()
bullet_img = pygame.image.load(path.join(img_dir, "wall.png")).convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (gap,gap))
core_img = pygame.transform.scale(core_img, (gap,gap))
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
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'throw.ogg'))
expl_sounds = pygame.mixer.Sound(path.join(snd_dir, 'crash.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'hold the line.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
array = posArray()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
core = Core()

all_sprites.add(player)
all_sprites.add(core)
newmob()


CGPA = 0
score = 0
count = 0
time = 0
levelUpTiming = 1200
pygame.mixer.music.play(loops=-1)
# Game loop
running = True
clear = False

while running:
    time += 1
    if time%levelUpTiming == 0:
        levelUpTiming *= 2
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
                player.shoot()
            array.update(bullets=bullets)

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
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
        core.shield -= 1
        expl = Explosion(hit.rect.x, hit.rect.y, hit.ident)
        player.eat()
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            running = False
    
    # check to see if a mob hit the core
    hits = pygame.sprite.spritecollide(core, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        hit.tail.kill()
        core.shield -= (hit.ident-1)*0.3
        # expl = Explosion(hit.rect.x, hit.rect.y, hit.ident)
        # all_sprites.add(expl)
        expl = Scored(hit.rect.center, hit.ident, hit.rot)
        all_sprites.add(expl)
        CGPA = CGPAcalculator(CGPA, hit, count)
        count += random.randint(1,3)
        newmob()
        # if core.shield <= 0:
            # running = False
    if count >= 130:
        clear = True
        
        
        
    # Draw / render
    screen.fill((150,150,150))
    # screen.blit(background, background_rect)
    

    if clear == True:
        button("Game Clear", CENTER[0], CENTER[1], 200, 100, BLACK, BLUE, RED, gameClose)
    else:
        all_sprites.draw(screen)
        #CGPA
        degitToDot(round(CGPA,2), 17, CENTER[0]-24, CENTER[1]-7)
        # draw_text(screen, str(round(CGPA, 2)), 25, BLACK, CENTER[0], CENTER[1]-5)
        #credit earned
        draw_text(screen, str(count), 18, BLACK, 5,100)
        player_shield_bar(screen, 5, 5, player.shield)
        core_shield_bar(screen, 5, 50, core.shield)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()