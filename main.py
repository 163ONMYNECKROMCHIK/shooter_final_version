from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, speed, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


font.init()
font1 = font.Font(None, 40)
font2 = font.Font(None, 60)

win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 700 - 65 - 5:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', -15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)


lost = 0
count = 0


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.width - 5)


bullets = sprite.Group()


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('педро.jpg', randint(1, 7), randint(30, 700 - 30), -40, 80, 50)
    asteroids.add(asteroid)





monster1 = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)
monster2 = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)
monster3 = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)
monster4 = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)
monster5 = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

rocket = Player('rocket.png', 5, 300, 400, 60, 80)
clock = time.Clock()
FPS = 60
game = True
finish = False

rel_time = False
num_fire = 0

while game:
    if finish != True:
        window.blit(background, (0, 0))

        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))

            else:
                num_fire = 0
                rel_time = False



        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprite_list:
            count += 1
            enemy = Enemy("ufo.png", randint(1, 5), randint(0, 700 - 60 - 5), 0, 60, 50)
            monsters.add(enemy)

        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose, (200, 200))



        text_lost = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (5, 5))

        text_lost = font1.render('Счёт: ' + str(count), True, (255, 255, 255))
        window.blit(text_lost, (5, 40))

        if lost >= 3:
            finish = True
            window.blit(lose, (200, 200))

        if count >= 7:
            finish = True
            window.blit(win, (200, 200))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire < 5 and rel_time == False:
                    fire.play()
                    rocket.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    display.update()
    clock.tick(FPS)
