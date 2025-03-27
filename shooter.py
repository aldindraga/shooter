from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

img_back = "spacesfond.png"
img_player = "rocket.png"
img_enemy = "alien.png"

window = display.set_mode((700,500))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back),(700,500))
lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def move(self):
        global lost
        self.rect.y +=self.speed
        if self.rect.y >500:
            self.rect.y =0
            self.rect.x = randint(70,630)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y <0:
            self.kill()


ship = Player(img_player,7,400,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
font.init()
font2 = font.SysFont('Ariel',36)
font1 = font.SysFont('Ariel',80)

for i in range(5):
    monster = Enemy(img_enemy,randint(70,630),-30,80,50,randint(1,3))
    monsters.add(monster)

for i in range(1,3):
    asteroid = Enemy("asteroid.png",randint(30,470),-30,80,50,randint(1,3))
    asteroids.add(asteroid)


finish = False
game = True
clock = time.Clock()

fitore = font2.render("Urimeee!",True,(255,255,255))
humbje = font2.render("Humbeee!",True,(180,0,0))
rel_time = False
num_fire = 0
life = 3

from time import time as timer
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire+=1
                if num_fire>= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Score:" + str(score),1,(255,255,255))
        window.blit(text,(10,10))

        text_lose = font2.render("Missed:"+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        ship.move()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        for asteroid in asteroids:
            asteroid.move()
            asteroid.reset()
        for monster in monsters:
            monster.move()
            monster.reset()

        if rel_time == True:
            now_time = timer()
            if now_time-last_time<3:
                reload = font2.render("Wait, reload...",True,(190,0,0))
                window.blit(reload,(260,450))
            else:
                num_fire=0
                rel_time= False

        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        
        for s in sprites_list:
            score+=1
            monster = Enemy(img_enemy,randint(70,630),-30,80,50,randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True) 
            sprite.spritecollide(ship,asteroids,True)
            life -= 1
          
        if life == 0 or lost >10:
            finish=True
            window.blit(humbje,(300,200))

        if score >=20:
            finish = True
            window.blit(fitore,(300,200))
        
        if life == 3:
            life_color = (0,180,0)
        if life == 2:
            life_color = (160,160,0)
        if life == 1:
            life_color = (160,0,0)

        text_life = font1.render(str(life),True,life_color)
        window.blit(text_life,(650,10))

        display.update()


    else:
        finish = False
        score = 0
        lost = 0
        life= 3
        num_fire=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        
        time.delay(3000)

        for i in range(5):
            monster = Enemy(img_enemy,randint(70,630),-30,80,50,randint(1,3))
            monsters.add(monster)
        for i in range(randint(1,3)):
            asteroid = Enemy("asteroid.png",randint(30,490),-30,80,50,randint(1,3))
            asteroids.add(asteroid)

    clock.tick(60)