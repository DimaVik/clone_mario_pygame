import pygame
import os
import sys
from pygame.locals import *
import time


total_level_width = 3392
total_level_height = 224
size = w, h = (600, 224)  # (3392, 224)
FPS = 60
speed = 3
jump = 7
gravity = 0.35

# Инициация PyGame, обязательная строчка
pygame.init()
pygame.font.init()
pygame.mixer.init()


font1 = pygame.font.Font('data\\font\\Fixedsys500c.ttf', 120)
music = pygame.mixer.music.load('data\\music\\01 - Super Mario Bros.mp3')
pygame.mixer.music.play(-1, 0.0)
game_over_sound = pygame.mixer.Sound('data\\music\\18 - Game Over (alternate).mp3')
game_win_sound = pygame.mixer.Sound('data\\music\\04 - Area Clear.mp3')

pygame.display.set_caption("Super Mario")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == -1:
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def start_screen():
    intro_text = ["MARIO GAME",
                  "Rules of the game:",
                  "Move with arrows, reach the castle",
                  "and don't fall into the abyss",
                  "Press any key to start playing"]

    fon = pygame.transform.scale(load_image('data\\screen\\fon.jpg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data\\font\\Fixedsys500c.ttf', 20)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    k = 1
    while k:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                k = 0
                break
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    screen.fill((0, 0, 0))
    label = font1.render("Game Over", 1, (255, 0, 0))
    screen.blit(label, (0, 0))
    # остонавливаем музыку
    pygame.mixer.music.stop()
    #ставим музыку проиграша
    game_over_sound.play()
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()



def win():
    screen.fill((255, 255, 255))
    label = font1.render("Winner", 1, (0, 255, 0))
    screen.blit(label, (0, 0))
    # остонавливаем музыку
    pygame.mixer.music.stop()
    game_win_sound.play()
    pygame.display.flip()
    time.sleep(6)
    pygame.quit()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.total = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.rect.x - w // 2)
        if self.total + self.dx > 0:
            self.dx = 0
        elif self.total < -(total_level_width) + w + 3:
            self.dx = 0
        else:
            self.total += self.dx


class Mario(pygame.sprite.Sprite):
    def __init__(self, fl):
        super().__init__(player, all_sprites)
        self.image = load_image(
            "data\\sprites\\mario_sprites\\mario_stand.png", -1)
        self.image.convert()
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = w // 2 + 1
        self.rect.y = 100
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False

    def update(self, l, r, u, fl):
        if up:
            # прыгаем, только когда можем оттолкнуться от земли
            if self.on_ground:
                self.yvel = -jump

        if left:
            self.xvel = -speed

        if right:
            # Право = x + n
            self.xvel = speed

        if not(left or right):
            # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.on_ground:
            self.yvel += gravity

        self.on_ground = False
        # Мы не знаем, когда мы на земле
        self.rect.y += self.yvel
        self.collide(0, self.yvel, fl)

        self.rect.x += self.xvel
        # переносим свои положение на xvel
        self.collide(self.xvel, 0, fl)

    def pos(self):
        return [self.rect.x, self.rect.y]

    def collide(self, xvel, yvel, fl):
        # если есть пересечение платформы с игроком
        if pygame.sprite.collide_mask(self, fl):

            if xvel > 0:
                self.rect.x -= self.xvel
                self.xvel = 0
                # если движется вправо ==> то не движется вправо

            if xvel < 0:
                # если движется влево ==> то не движется влево
                self.rect.x -= self.xvel
                self.xvel = 0
            if yvel > 0:
                # если падает вниз ==> то не падает вниз
                self.on_ground = True
                self.rect.y -= self.yvel - 1
                # и становится на что-то твердое
                self.yvel = 0

            if yvel < 0:
                # если движется вверх# то не движется вверх
                self.rect.y += self.yvel - 1
                # и энергия прыжка пропадает
                self.yvel = 0


class BG(pygame.sprite.Sprite):
    def __init__(self, location=[0, 0]):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image("data\\sprites\\bg.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Floor(pygame.sprite.Sprite):
    def __init__(self, location=[0, 0]):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image("data\\sprites\\bg_fl.png", -1)
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player = pygame.sprite.Group()
bg = BG()
fl = Floor()
mario = Mario(fl)
tiles_group.add(bg)
tiles_group.add(fl)
player.add(mario)
left, up, right = False, False, False

camera = Camera()
# Цикл игры
start_screen()
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            up = True
        else:
            up = False
        if keystate[pygame.K_LEFT]:
            left = True
        else:
            left = False
        if keystate[pygame.K_RIGHT]:
            right = True
        else:
            right = False

    # Обновление
    tiles_group.draw(screen)
    player.draw(screen)
    camera.update(mario)
    # изменяем ракурс камеры
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    player.update(left, up, right, fl)
    x, y = mario.pos()
    if y >= h - 2:
        running = False
        terminate()
    if x >= w - 150:
        running = False
        win()
    # Рендеринг
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
