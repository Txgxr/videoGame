from turtle import speed
import pygame as pg
import random
from pygame.sprite import Sprite

vec = pg.math.Vector2

#Define Screen Size and FPS

WIDTH = 900
HEIGHT = 600
FPS = 60


# Define player and mob movement speeds

PLAYER_FRIC = -0.2
PLAYER_GRAV = 0
MOB_GRAV = 0
MOB_FRIC = -0.2
PLAYER_SPEED = 4

# Global variables used to keep track of stats
mobCount = 1
points = 0
mobCap = 1
multi = 1
multiPrice = 5
mobPrice = 5
speedPrice = 10
score = 0


# Tuples for colors
WHITE = (255, 255, 255)
LIGHT = (170, 170, 170)
DARK = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (40, 40, 40)

# Function to draw text on the screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# Player Class
class Player(pg.sprite.Sprite):
    global FPS
    def __init__(self):
        global FPS
        Sprite.__init__(self)
        self.image = pg.Surface((100, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.yvel = 5
        self.xvel = 5
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_SPEED/2
        if keys[pg.K_d]:
            self.acc.x = PLAYER_SPEED/2
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_SPEED/2
        if keys[pg.K_s]:
            self.acc.y = PLAYER_SPEED/2
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        self.acc += self.vel * PLAYER_FRIC
        self.acc.x += self.vel.x * -0.2
        self.acc.y += self.vel.y * -0.2
        self.vel += self.acc
        self.pos += self.vel + 0.7 * self.acc
        self.rect.midbottom = self.pos

# Mob Class
class Mob(pg.sprite.Sprite):
    global mobCount
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.yvel = 0
        self.xvel = 0
    def randMove(self):
        self.acc.x = random.randint(-10, 10)
        self.acc.y = random.randint(-10, 10)
    def update(self):
        global mobCount, points, score
        hitsMob = pg.sprite.spritecollide(self, all_sprites, False)
        if hitsMob:
            pg.mixer.Sound.play(pop)
            score += 1
            points += 1 * multi
            self.pos.x = random.randint(0,WIDTH)
            self.pos.y = random.randint(0,HEIGHT)
        self.acc = vec(0, MOB_GRAV)
        if self.pos.y < 0:
            self.pos.y += 50
        if self.pos.y > HEIGHT:
            self.pos.y -= 50
        if self.pos.x < 0:
            self.pos.x += 50
        if self.pos.x > WIDTH:
            self.pos.x -= 50
        self.randMove()
        self.acc += self.vel * MOB_FRIC
        self.acc.x += self.vel.x * MOB_FRIC
        self.acc.y += self.vel.y * MOB_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.7 * self.acc
        self.rect.midbottom = self.pos

                

# Initialize pygame and sound 
pg.init()
pg.mixer.init()

# Game sounds
pop = pg.mixer.Sound('pop3.ogg')
purchase = pg.mixer.Sound('purchase.ogg')

# Create screen and window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Game!!!")
clock = pg.time.Clock()

# Create groups
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# Instantiate classes
player = Player()
mob = Mob()



# Add instances to groups
all_sprites.add(player)
all_mobs.add(mob)

smallfont = pg.font.SysFont('arial', 35)



# Game loop
running = True
while running:
    mouse = pg.mouse.get_pos()
    dt = clock.tick(FPS)
    
    #Check if player is out of bounds
    if player.rect.x > WIDTH:
        player.rect.x = WIDTH-50
    if player.rect.x < 0:
        player.rect.x = 0

    # Check if buttons are pressed
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
        elif ev.type == pg.MOUSEBUTTONDOWN:
            if WIDTH-300 <= mouse[0] <= WIDTH-300+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
                if points >= mobPrice:
                    pg.mixer.Sound.play(purchase)
                    mobCount += 1
                    points -= mobPrice
                    mobPrice *= 2
                    newMob = Mob()
                    all_mobs.add(newMob)
            elif WIDTH-600 <= mouse[0] <= WIDTH-600+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
                if points >= multiPrice:
                    pg.mixer.Sound.play(purchase)
                    multi += 1
                    points -= multiPrice
                    multiPrice += 5
            elif WIDTH-900 <= mouse[0] <= WIDTH-900+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
                if points >= speedPrice:
                    pg.mixer.Sound.play(purchase)
                    PLAYER_SPEED += 1
                    points -= speedPrice
                    speedPrice *= 2


    # Text for buttons
    buyMobtext = smallfont.render(f'Buy Mob ({mobPrice} Pts)', True, WHITE)
    buyMultiText = smallfont.render(f'Buy Multi ({multiPrice} Pts)', True, WHITE)
    buySpeedText = smallfont.render(f'Buy Speed ({speedPrice} Pts)', True, WHITE)   
      
    # Fill background
    screen.fill(BLACK)

    # Update all sprites
    all_sprites.update()
    all_platforms.update()
    all_mobs.update()
    # Draw all sprites
    all_sprites.draw(screen)
    all_platforms.draw(screen)
    all_mobs.draw(screen)

    # Draw statistics text
    draw_text(f"POINTS: {points}", 22, WHITE, 80, 5)
    draw_text(f"SPEED: {PLAYER_SPEED}", 22, WHITE, 80, 40)
    draw_text(f"MOBS: {mobCount} ", 22, WHITE, 80, 75)
    draw_text(f"MULTI: {multi} ", 22, WHITE, 80, 110)

    # Check if mouse is hovering button and draw button background
    if WIDTH-300 <= mouse[0] <= WIDTH-300+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
        pg.draw.rect(screen,LIGHT,[WIDTH-290,HEIGHT-100,280,60])
    else:
        pg.draw.rect(screen,DARK,[WIDTH-290,HEIGHT-100,280,60])

    if WIDTH-600 <= mouse[0] <= WIDTH-600+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
        pg.draw.rect(screen,LIGHT,[WIDTH-590,HEIGHT-100,280,60])
    else:
        pg.draw.rect(screen,DARK,[WIDTH-590,HEIGHT-100,280,60])

    if WIDTH-900 <= mouse[0] <= WIDTH-900+280 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+60:
        pg.draw.rect(screen,LIGHT,[WIDTH-890,HEIGHT-100,280,60])
    else:
        pg.draw.rect(screen,DARK,[WIDTH-890,HEIGHT-100,280,60])

    # Blit text to buttons
    screen.blit(buyMobtext, (WIDTH-280,HEIGHT-90))
    screen.blit(buyMultiText, (WIDTH-580,HEIGHT-90))
    screen.blit(buySpeedText, (WIDTH-880,HEIGHT-90))

  
    
    # Update the screen
    pg.display.flip()

pg.quit()