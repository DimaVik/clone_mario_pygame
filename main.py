import pygame
import os
import sys

size = (3392, 224)
FPS = 60

pygame.init() # Инициация PyGame, обязательная строчка 
pygame.display.set_caption("Super Mario") # Пишем в шапку
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

class Mario(pygame.sprite.Sprite):
    def __init__(self, pos, fl):
        super().__init__()
        self.image = load_image("data\\sprites\\mario_sprites\\mario_stand.png", -1)
        self.image.convert()
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, fl):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, fl):
            self.rect = self.rect.move(0, 1)
    

class BG(pygame.sprite.Sprite):
    def __init__(self, location=[0, 0]):
        super().__init__()
        self.image = load_image("data\\sprites\\bg.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Floor(pygame.sprite.Sprite):
    def __init__(self, location=[0, 0]):
        super().__init__()
        self.image = load_image("data\\sprites\\bg_floor.png", -1)
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        # crate mask of floor
        self.mask = pygame.mask.from_surface(self.image)


all_sprites = pygame.sprite.Group()
bg = BG()
fl = Floor()
all_sprites.add(bg)
all_sprites.add(fl)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pers = Mario(event.pos, fl)
            all_sprites.add(pers)
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.draw(screen)
    all_sprites.update(fl)
    # Рендеринг
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
        
