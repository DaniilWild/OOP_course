import pygame
from os import path

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, height=50, width=50, speed=5, color=(0, 0, 0), image=False):
        pygame.sprite.Sprite.__init__(self)

        self.height = height
        self.width = width

        if not image:
            self.image = pygame.Surface((height, width))
            self.image.fill(color)
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.speed = speed
        self.moving_left = False  # Двигается ли персонаж налево
        self.moving_right = False  # Двигается ли персонаж направо
        self.moving_up = False  # Двигается ли персонаж вверх
        self.moving_down = False  # Двигается ли персонаж вниз
        self.shoting = False # Стерялет ли пероснаж

class Player(GameSprite):

    # Движение персонажа
    def update(self, screen):
        global running, start_ticks  #рубим главный цикл

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # нажатие на крестик: выход
                running = False
            # Клавиша нажата
            if event.type == pygame.KEYDOWN:  # тип события - нажатие на кнопку
                if event.key == 27:
                    running = False
                if event.key == pygame.K_d:
                    self.moving_right = True
                if event.key == pygame.K_a:
                    self.moving_left = True
                if event.key == pygame.K_s:
                    self.moving_down = True
                if event.key == pygame.K_w:
                    self.moving_up = True
                if event.key == pygame.K_SPACE and (pygame.time.get_ticks() - start_ticks) > TIME_SHOOT * 100:
                    self.shoot()
                    start_ticks = pygame.time.get_ticks()

            # Клавиша отпушена
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.moving_right = False
                if event.key == pygame.K_a:
                    self.moving_left = False
                if event.key == pygame.K_s:
                    self.moving_down = False
                if event.key == pygame.K_w:
                    self.moving_up = False

        # непосредсвенно само движение
        if self.moving_up and self.rect.y > 0:
            self.rect.y -= self.speed
        if self.moving_left and self.rect.x > 0:
            self.rect.x -= self.speed
        if self.moving_down and self.rect.y + self.height < sc.get_height():
            self.rect.y += self.speed
        if self.moving_right and self.rect.x + self.width < sc.get_width():
            self.rect.x += self.speed

        # обработка движений в случае препядсвтий
        for wall in walls:
            if self.rect.colliderect(wall):
                #правая сторона стены
                if self.moving_right and wall.rect.left < self.rect.right < wall.rect.left +10:
                    self.rect.right = wall.rect.left
                # левая сторона стены
                elif self.moving_left and wall.rect.right > self.rect.left > wall.rect.right - 10:
                    self.rect.left = wall.rect.right
                # нижняя сторона стены
                elif self.moving_down and wall.rect.top < self.rect.bottom < wall.rect.top + 10:
                    self.rect.bottom = wall.rect.top
                # верхняя сторона стены
                elif self.moving_up and wall.rect.bottom > self.rect.top > wall.rect.bottom - 10:
                    self.rect.top = wall.rect.bottom

    # cтрельба, ввдется из правой стороны спрайта
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery-5, width=10, height=20, color=BLACK)
        all_sprites.add(bullet)
        all_bullets.add(bullet)

class Enemy(GameSprite):
    def range(self,min , max, rotation = "x"):
        self.min = min
        self.max = max
        self.rotation = rotation

    def update(self, screen):
        if self.rotation == "x":
            if self.rect.x > self.max or self.rect.x < self.min:
                self.speed = -self.speed
            self.rect.x += self.speed

        elif self.rotation == "y":
            pass
        # Убить бота если его застрелили
        for bullet in all_bullets:
            if self.rect.colliderect(bullet):
                self.kill()
                bullet.kill()

# class Bullet(GameSprite):  # https://pythonru.com/primery/streljalka-s-pygame-3-stolknovenija-i-strelba
class Bullet(GameSprite):

    def update(self, scren):
        self.rect.x += self.speed

        hit = pygame.sprite.spritecollide(self, walls, False)
        #hits = pygame.sprite.spritecollide(player, mobs, False)
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.x > sc.get_width() or len(hit) != 0: #or self.rect.colliderect(enemy1):
            self.kill()




# Основные цвета в программе
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

# Параметры игры
width = 360  # ширина игрового окна
height = 480  # высота игрового окна
running = True  # переменная главного цикла

FPS = 30  # частота каодров в игре
ALL_SPEED = 5 # cкорость движения всех обьектов в игре по умолчанию
TIME_SHOOT = 3 # задержка перед выстрелом в секундах
start_ticks = 0

# Первичная настройка окна
sc = pygame.display.set_mode((height, width))
pygame.display.set_caption('Best Game')
clock = pygame.time.Clock()

# Загрузка картинок
img_dir = path.dirname(__file__)
background = pygame.image.load(path.join(img_dir, '9046OT_06_02.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "tanks.png")).convert()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()

# Cпрайт главного героя
hero = Player(50, 50, 50, 50, color=YELLOW)
all_sprites.add(hero)

# Стены
wall1 = GameSprite(150, 150, 150, 20)
wall2 = GameSprite(150, 150, 20, 80)
wall3 = GameSprite(300, 150, 20, 80)
walls = [wall1, wall2, wall3]

enemy1 = Enemy(100, 50, 50, 50, color=PINK)
enemy1.range(100,200)

all_enemy.add([enemy1])

all_sprites.add(walls)
all_sprites.add(all_enemy)

bullets = []

# https://younglinux.info/pygame/sprite
while running:  # бесконечный игровой цикsл

    sc.fill(WHITE)

    sc.blit(background, background_rect)

    all_sprites.update(sc)
    all_sprites.draw(sc)

    pygame.display.update()
    clock.tick(FPS)