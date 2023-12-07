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
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

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
        self.shield = 100


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (gap, gap))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20

        self.rect.x = array.corePos.column*gap
        self.rect.y = array.playerPos.row*gap

        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    
    def posUpdate(self):
        self.rect.x = array.playerPos.column*gap
        self.rect.y = array.playerPos.row*gap

    # def update(self):
    #     self.rect.x = self.array.row*gap
        # self.speedx = 0
        # keystate = pygame.key.get_pressed()
        # # if keystate[pygame.K_LEFT]:
        # #     self.speedx = -8
        # # if keystate[pygame.K_RIGHT]:
        # #     self.speedx = 8
        # if keystate[pygame.K_SPACE]:
        #     self.shoot()
        # # self.rect.x += self.speedx
        # # if self.rect.right > WIDTH:
        # #     self.rect.right = WIDTH
        # # if self.rect.left < 0:
        # #     self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.x, self.rect.y)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image_orig = random.choice(meteor_images)
        self.ident = np.random.randint(0,5)
        self.image_orig = meteor_images[self.ident]
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.dist = 1
        self.ang = random.uniform(0, 2*np.pi)
        self.rect.x = CENTER[0] + (WIDTH/2)*np.cos(self.ang)*self.dist
        self.rect.y = CENTER[1] + (WIDTH/2)*np.sin(self.ang)*self.dist

        # self.rect.x = random.randrange(WIDTH - self.rect.width)
        # self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.speed = random.randrange(5,10)*0.001
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

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
        # self.rotate()
        self.rect.x += self.speedx
        # self.rect.y += self.speedy
        self.dist -= self.speed
        self.rect.centerx = CENTER[0] + (WIDTH/2)*np.cos(self.ang)*self.dist
        self.rect.centery = CENTER[1] + (WIDTH/2)*np.sin(self.ang)*self.dist

        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            # self.rect.x = random.randrange(WIDTH - self.rect.width)
            # self.rect.y = random.randrange(-100, -40)
            # self.speedy = random.randrange(1, 8)

            # self.dist = 1
            # self.ang = random.uniform(0, 2*np.pi)
            # self.rect.x = CENTER[0] + (WIDTH/2)*np.cos(self.ang)*self.dist
            # self.rect.y = CENTER[1] + (WIDTH/2)*np.sin(self.ang)*self.dist
            all_sprites.remove(self)
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = -10

    def update(self):
        # self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Load all game graphics
# background = pygame.image.load(path.join(img_dir, "Toon Road Texture.png")).convert()
# background = pygame.transform.scale(background, (1000,800))
# background_rect = background.get_rect()
core_img = pygame.image.load(path.join(img_dir, "monitor.png")).convert_alpha()
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert_alpha()
bullet_img = pygame.image.load(path.join(img_dir, "block.png")).convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (gap,gap))
core_img = pygame.transform.scale(core_img, (gap,gap))
meteor_images = []
meteor_list = ['A+.png', 'A.png', 'B.png',
               'C.png', 'F.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    # meteor_images[-1] = pygame.transform.rotate(meteor_images[-1], 180)
    meteor_images[-1] = pygame.transform.scale(meteor_images[-1], (gap,gap))
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
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
for i in range(1):
    newmob()


score = 0
pygame.mixer.music.play(loops=-1)
# Game loop
running = True
time = 0
while running:
    time += 1
    if time%1200 == 0:
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
                target = array.playerPos.column - 1
                if array.slot[array.playerPos.row, target] == 0:
                    array.playerPos.column = target
            if event.key == pygame.K_RIGHT:
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
                # array.blockedSlot.append([array.playerPos.row, array.playerPos.column])
                player.shoot()
            # player.posUpdate(array=array)
            array.update(bullets=bullets)

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        expl_sounds.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        # if player.shield <= 0:
        #     running = False
    
    # check to see if a mob hit the core
    hits = pygame.sprite.spritecollide(core, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        # core.shield -= hit.radius * 2
        core.shield -= (hit.ident-1)*10
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        # if core.shield <= 0:
        #     running = False

    # Draw / render
    screen.fill(WHITE)
    # screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_shield_bar(screen, 5, 50, core.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()