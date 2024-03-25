#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as t
mixer.init()
mixer_music.load('space.mp3')
mixer_music.play()
window = display.set_mode((885, 557))
display.set_caption('Star Wars')
background = transform.scale(image.load('background.jpg'), (885, 557))
clock = time.Clock()
FPS = 60
game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (90, 85))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 800:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        laser = Laser('laser.png', self.rect.x, self.rect.top, 5)
        lasers.add(laser)
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 557:
            self.rect.y = 0
            self.rect.x = randint(50, 800)
            lost = lost + 1
class Laser(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
finish = False
space_ship = Player('ship.png', 400, 410, 10)
monster1 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
monster2 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
monster3 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
monster4 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
monster5 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
monster6 = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
asteroid1 = Enemy('asteroid.png', randint(50, 835), 0, randint(1, 3))
asteroid2 = Enemy('asteroid.png', randint(50, 835), 0, randint(1, 3))
monsters = sprite.Group()
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
monsters.add(monster6)
lasers = sprite.Group()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 100)
fire = mixer.Sound('fire.wav')
win = font2.render('YOU WON!', True, (118, 187, 203))
lose = font2.render('YOU LOSE!', True, (255, 76, 61))
lives = 3
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire.play()
                    space_ship.fire()
                    num_fire +=1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    reload_time = t()
    if finish != True:
        window.blit(background, (0, 0))
        if rel_time == True:
            reload_timer = t()
            if reload_timer - reload_time < 3:
                reload = font1.render('Wait. Reloading...', True, (193, 239, 1))
                window.blit(reload, (400, 410))
            else:
                rel_time = False
                num_fire = 0
        lasers.update()
        lasers.draw(window)
        collide = sprite.spritecollide(space_ship, asteroids, True)
        sprites_list = sprite.groupcollide(monsters, lasers, True, True)
        for element in collide:
            lives -=1
            asteroid = Enemy('asteroid.png', randint(50, 835), 0, randint(1, 3))
            print(lives)
            asteroids.add(asteroid)
        for element in sprites_list:
            score += 1
            monster = Enemy('enemy.png', randint(50, 835), 0, randint(1, 3))
            monsters.add(monster)
        text_lose = font1.render('Missed: ' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 35))
        window.blit(text_score, (10, 10))
        space_ship.reset()
        space_ship.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if score >= 10:
            finish = True
            window.blit(win, (300, 250))
        if lost >= 5 or lives == 0:
            finish = True
            window.blit(lose, (300, 250))
    display.update()
    clock.tick(FPS)