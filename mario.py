import os
import sys

import pygame

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, dx, dy):
        if self.pos_x == 0 and dx == -1 or self.pos_y == 0 and dy == -1:
            return
        if self.pos_x == level_width - 1 and dx == 1 or self.pos_y == level_height - 1 and dy == 1:
            return
        self.pos_x += dx
        self.pos_y += dy
        for t in tiles_group:
            if t.tile_type == 'wall' and t.pos_x == self.pos_x and t.pos_y == self.pos_y:
                self.pos_x -= dx
                self.pos_y -= dy
                break
        else:
            self.rect.x += dx * tile_width
            self.rect.y += dy * tile_height


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Используйте стрелки для перемещения", ]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


size = width, height = 700, 500
tile_width = tile_height = 50


def load_level(filename):
    global level_width, level_height, size
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    level_width = max_width
    level_height = len(level_map)
    # size = width, height

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


m = input("Введите название уровня (без .txt): ")
player, level_x, level_y = generate_level(load_level(m + '.txt'))
# player, level_x, level_y = generate_level(load_level('map.txt'))
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

start_screen()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        # obj.rect.x += self.dx
        # obj.rect.y += self.dy
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()

# camera.update(player)
#
# for sprite in all_sprites:
#     camera.apply(sprite)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1)
            if event.key == pygame.K_DOWN:
                player.move(0, 1)
            if event.key == pygame.K_RIGHT:
                player.move(1, 0)
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)

    screen.fill(pygame.Color((0, 0, 0)))

    camera.update(player)
    for elem in all_sprites:
        camera.apply(elem)

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
