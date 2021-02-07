import pygame
import random
from os import path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'sounds')

WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

font_01 = pygame.font.match_font('aesthetic')


#начальный экран
def first_ecran():
    screen.blit(field, field_02)
    all_text(screen, "Space Shooter", 64, WIDTH / 2, HEIGHT / 4)
    all_text(screen, "Нажимайте на стрелки для передвижения, пробел для стрельбы.", 20,
              WIDTH / 2, HEIGHT / 2)
    all_text(screen, "Нажмите любую кнопку, что бы продолжить.", 25, WIDTH / 2, HEIGHT / 1.5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


#счёткик жизней
def lives_score(surf, x, y, lives):
    if lives < 0:
        lives = 0
    length = 100
    height = 10
    fill = (lives / 100) * length
    fill_rect = pygame.Rect((WIDTH / 2) - 45, 65, fill, height)
    outline_rect = pygame.Rect((WIDTH / 2) - 45, 65, length, height)
    pygame.draw.rect(surf, WHITE, outline_rect, 3)
    pygame.draw.rect(surf, GREEN, fill_rect)


def all_text(surf, text, size, x, y):
    font = pygame.font.Font(font_01, size)
    txt_first = font.render(text, True, WHITE)
    txt_second = txt_first.get_rect()
    txt_second.midtop = (x, y)
    surf.blit(txt_first, txt_second)


def newsprites():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


#Класс модельки игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP]:
            self.speedy = - 5
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.speedx = 0

        if keystate[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        shoot_sound.play()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


#Класс выстрела, модельки пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


#Класс врагов(астероидов)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    #Функция вращения астероидов
    def turn_around(self):
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
        self.turn_around()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

#Игровое поле
field = pygame.image.load(path.join(img_dir, "startfield.jpg")).convert()
field_02 = field.get_rect()
#Изображение игрока
player_img = pygame.image.load(path.join(img_dir, "cosmo-corabl.png")).convert()
#Изображение пули
bullet_img = pygame.image.load(path.join(img_dir, "blaster.png")).convert()
#Изображения астероидов
meteor_images = []
meteor_list = ['meteor_03.png', 'meteor_02.png', 'meteor_01.png',
               'meteor_04.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#Звуки выстрелов
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'bam.wav'))
other_sounds = []
for snd in ['boom_01.wav', 'boom_02.wav']:
    other_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#Загрузка музыки
pygame.mixer.music.load(path.join(snd_dir, 'Король и Шут - Кукла колдуна.mp3'))
pygame.mixer.music.set_volume(5.5)
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
pygame.mixer.music.play(loops=-1)

game_over = True
running = True
while running:
    if game_over:
        first_ecran()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newsprites()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    #Начилсение очков, за уничтожение астероида
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 75 - hit.radius
        random.choice(other_sounds).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #Столкновение игрока и врага
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius * 1.5
        newsprites()
        if player.health <= 0:
            running = False

    #Восстановление жизней каждые 1000 очков
    if 1000 <= score <= 1100:
        player.health = 100

    if 2000 <= score <= 2100:
        player.health = 100

    if 3000 <= score <= 3100:
        player.health = 100

    if 4000 <= score <= 4100:
        player.health = 100

    if 4900 <= score <= 5000:
        player.health = 100

    #Конец игры на 5000 очках
    if score >= 5000:
        game_over = True

    screen.fill(BLACK)
    screen.blit(field, field_02)
    all_sprites.draw(screen)
    all_text(screen, str(score), 40, WIDTH / 2, 10)
    lives_score(screen, 5, 5, player.health)
    pygame.display.flip()

pygame.quit()
