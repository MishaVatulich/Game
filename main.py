import pygame
import os
import sys
import random
import sqlite3
import math

pygame.init()
size = width, height = 1100, 600
screen = pygame.display.set_mode(size)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
heroes = pygame.sprite.Group()

HERO_1 = 20
HERO_2 = 21
HERO_3 = 22
HERO_4 = 23
HERO_5 = 24

fps = 60
clock = pygame.time.Clock()
con = sqlite3.connect("Game.db")
cur = con.cursor()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Scp049Two(pygame.sprite.Sprite):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp/scp_049-2.png", -1), (170, 225)), True, False)

    def __init__(self, level):
        super().__init__(enemies)
        self.image = Scp049Two.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1100, 1500 + level * 50)
        if level < 7:
            self.rect.x = random.randrange(1100, 1500)
        self.rect.y = random.randrange(200, 375)
        self.x = self.rect.x  # Истиное положение по x
        self.money = 1
        self.hp = 100
        self.speed = 51  # пикселей в секунду

    def update(self, effect):
        global money
        if self.hp <= 0:
            money += self.money
            enemies.remove(self)
            return
        self.x -= self.speed * effect / fps  # не целое число
        self.rect.x = int(self.x)


class Scp049(Scp049Two):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp/scp_049.png", -1), (260, 200)), True, False)

    def __init__(self, level):
        super().__init__(level)
        self.image = Scp049.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1100, 1100 + level * 10)
        self.rect.y = random.randrange(200, 400)
        self.x = self.rect.x  # истиное положение
        self.money = 6
        self.hp = 200
        self.speed = 43  # пикселей в секунду


class Scp106(Scp049Two):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp/scp_106.png"), (90, 225)), True, False)

    def __init__(self, level):
        super().__init__(level)
        self.image = Scp106.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1100, 1100 + level * 20)
        self.rect.y = random.randrange(180, 375)
        self.x = self.rect.x
        self.money = 20
        self.hp = 300
        self.speed = 43  # пикселей в секунду


class Scp173(Scp049Two):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp/scp_173.png"), (90, 270)), True, False)

    def __init__(self, level):
        super().__init__(level)
        self.image = Scp173.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1300, 1700 + level * 10)
        self.rect.y = random.randrange(140, 330)
        self.x = self.rect.x
        self.money = 5
        self.hp = 70
        self.speed = 90  # пикселей в секунду


class Scp178One(Scp049Two):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp/scp_178-1.png", -1), (400, 225)), True, False)

    def __init__(self, level):
        super().__init__(level)
        self.image = Scp178One.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1100, 1100 + level * 10)
        self.rect.y = random.randrange(200, 375)
        self.x = self.rect.x
        self.money = 6
        self.hp = 100
        self.speed = 34  # пикселей в секунду


class Scp682(Scp049Two):
    image = pygame.transform.scale(load_image("scp/scp_682.png"), (350, 200))

    def __init__(self, level):
        super().__init__(level)
        self.image = Scp682.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(1100, 1100 + level * 5)
        self.rect.y = random.randrange(230, 420)
        self.x = self.rect.x
        self.money = 40
        self.hp = 700
        self.speed = 26  # пикселей в секунду


class Bullet(pygame.sprite.Sprite):
    image_1 = pygame.transform.scale(load_image("bullets/bullet_1.png", -1), (20, 15))
    image_2 = pygame.transform.scale(load_image("bullets/bullet_2.png"), (30, 15))
    image_3 = pygame.transform.scale(load_image("bullets/bullet_3.png"), (40, 30))
    image_4 = pygame.transform.scale(load_image("bullets/bullet_4.png"), (40, 40))

    def __init__(self, x_0, y_0, x, y, level):
        super().__init__(bullets)
        if level <= 4:
            self.image = Bullet.image_1
        elif 4 < level <= 8:
            self.image = Bullet.image_2
        elif 8 < level <= 12:
            self.image = Bullet.image_3
        elif level > 12:
            self.image = Bullet.image_4
        self.rect = self.image.get_rect()
        self.rect.x = x_0  # начальное
        self.rect.y = y_0  # положение
        self.x = self.rect.x  # точные координаты, self.x  и self.y могут быть не целыми
        self.y = self.rect.y
        self.x_end = x  # конечное положение
        self.v_x = 20
        self.v_y = self.v_x * ((y - self.rect.height // 2 - y_0) / (x - self.rect.width - x_0))
        self.image = pygame.transform.rotate(self.image, -57.3 * math.atan(self.v_y / self.v_x))
        self.mask = pygame.mask.from_surface(self.image)
        self.level = level
        self.damage = self.no_effect_damage = 20 + level * 5

    def update(self, *effect):
        if effect:
            self.damage = self.no_effect_damage * effect[0]
            return
        self.x += self.v_x
        self.rect.x = self.x
        self.y += self.v_y
        self.rect.y = self.y
        if self.rect.x >= self.x_end:
            bullets.remove(self)
            for i in enemies.sprites():
                if pygame.sprite.collide_mask(self, i):
                    i.hp -= self.damage
                    break


class Hero(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("heroes/hero_2.png"), (145, 180))

    def __init__(self, level, pos):
        super().__init__(heroes)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 140 * (int(pos) % 2)
        self.rect.y = 200 + int(pos) // 2 * 200
        if int(pos) == 4:
            self.rect.x = 70
            self.rect.y = 300
        self.level = int(level)
        self.shooting = True
        self.shooting_speed = 100  # число для скорости стрельбы

    def shoot(self, x, y):
        if self.shooting is True:
            Bullet(self.rect.x + self.rect.width, self.rect.y + 30, x, y, self.level)
            self.shooting = False
            pygame.time.set_timer(20 + heroes.sprites().index(self), 1500 - self.shooting_speed)


def terminate():
    pygame.quit()
    sys.exit()


def generate_enemies(level):
    if level >= 18:
        for _ in range(20):
            Scp049Two(level)
    else:
        for _ in range(3 + level):
            Scp049Two(level)
    if level >= 24:
        for _ in range(7):
            Scp173(level)
    else:
        for _ in range(level // 3):
            Scp173(level)
    for _ in range(level // 7):
        Scp682(level)
    for _ in range(level // 6):
        Scp178One(level)
    for _ in range(level // 6):
        Scp049(level)
    for _ in range(level // 10):
        Scp106(level)
    sorted_enemies = sorted(enemies.sprites(), key=lambda scp: scp.rect.y + scp.rect.height)  # сортирует по низу
    enemies.empty()
    for i in sorted_enemies:
        enemies.add(i)


def save(level, money):
    cur.execute("""UPDATE save
                    SET level = ?,
                        money = ?""", (level, money))
    con.commit()
    cur.execute("""UPDATE save
                    SET hero_1 = ?""", (str(heroes.sprites()[0].level) + ' ' + '0',))
    con.commit()
    if len(heroes.sprites()) > 1:
        cur.execute("""UPDATE save
                        SET hero_2 = ?""", (str(heroes.sprites()[1].level) + ' ' + '1',))
        con.commit()
    if len(heroes.sprites()) > 2:
        cur.execute("""UPDATE save
                        SET hero_3 = ?""", (str(heroes.sprites()[2].level) + ' ' + '2',))
        con.commit()
    if len(heroes.sprites()) > 3:
        cur.execute("""UPDATE save
                        SET hero_4 = ?""", (str(heroes.sprites()[3].level) + ' ' + '3',))
        con.commit()
    if len(heroes.sprites()) > 4:
        cur.execute("""UPDATE save
                        SET hero_5 = ?""", (str(heroes.sprites()[4].level) + ' ' + '4',))
        con.commit()


def play(args):
    global money
    fon_sprites = pygame.sprite.Group()
    fon_sprite = pygame.sprite.Sprite()
    fon_sprite.image = pygame.transform.scale(load_image("fon/fon_1.png"), (1100, 600))
    fon_sprite.rect = fon_sprite.image.get_rect()
    fon_sprites.add(fon_sprite)

    barricade_sprites = pygame.sprite.Group()
    barricade_sprite = pygame.sprite.Sprite()
    barricade_sprite.image = pygame.transform.scale(load_image("fon/barricade.png"), (150, 150))
    barricade_sprite.rect = barricade_sprite.image.get_rect()
    barricade_sprite.mask = pygame.mask.from_surface(barricade_sprite.image)
    barricade_sprite.rect.x = 210
    barricade_sprite.rect.y = 290
    barricade_sprites.add(barricade_sprite)

    barricade_2_sprite = pygame.sprite.Sprite()
    barricade_2_sprite.image = barricade_sprite.image
    barricade_2_sprite.rect = barricade_2_sprite.image.get_rect()
    barricade_2_sprite.rect.x = 210
    barricade_2_sprite.rect.y = 380
    barricade_sprites.add(barricade_2_sprite)

    barricade_3_sprite = pygame.sprite.Sprite()
    barricade_3_sprite.image = barricade_sprite.image
    barricade_3_sprite.rect = barricade_3_sprite.image.get_rect()
    barricade_3_sprite.rect.x = 210
    barricade_3_sprite.rect.y = 470
    barricade_sprites.add(barricade_3_sprite)

    pygame.mixer.music.load('sounds_and_music/level.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    level = args[1]
    money = args[2]

    for i in range(3, 8):
        if args[i] != '':
            Hero(args[i].split()[0], args[i].split()[1])

    attack = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(level, money)
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save(level, money)
                    heroes.empty()
                    enemies.empty()
                    bullets.empty()
                    pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    return
                if event.key == pygame.K_w and not attack:
                    attack = True
                    generate_enemies(level)
                if event.key == pygame.K_s:
                    enemies.empty()
            if event.type == HERO_1:
                heroes.sprites()[0].shooting = True
                pygame.time.set_timer(HERO_1, 0)
            if event.type == HERO_2:
                heroes.sprites()[1].shooting = True
                pygame.time.set_timer(HERO_2, 0)
            if event.type == HERO_3:
                heroes.sprites()[2].shooting = True
                pygame.time.set_timer(HERO_3, 0)
            if event.type == HERO_4:
                heroes.sprites()[3].shooting = True
                pygame.time.set_timer(HERO_4, 0)
            if event.type == HERO_5:
                heroes.sprites()[4].shooting = True
                pygame.time.set_timer(HERO_5, 0)
        if pygame.mouse.get_pressed()[0] == 1:  # стрельба
            for i in heroes.sprites():
                i.shoot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if attack:
            if len(enemies.sprites()) == 0:  # проверка на победу
                attack = False
                level += 1
            scp_049 = scp_106 = scp_178 = 0
            for i in enemies.sprites():  # считается кол-во врагов, которые могут накладывать эффекты
                if isinstance(i, Scp049):
                    scp_049 += 1
                elif isinstance(i, Scp106):
                    scp_106 += 1
                elif isinstance(i, Scp178One):
                    scp_178 += 1
            enemies.update(scp_049 * 0.05 + 1)  # scp 049 увеличивает скорость на 5 %. Эффект сумируется
            bullets.update(1 - scp_178 * 0.05)  # scp 178-1 уменьшает урон на 5 %. Эффект сумируется
        fon_sprites.draw(screen)
        barricade_sprites.draw(screen)
        enemies.draw(screen)
        heroes.draw(screen)
        bullets.draw(screen)
        bullets.update()

        text_money = font.render("money: {}$".format(money), 1, (0, 0, 0))
        text_money_x = width - 20 - text_money.get_width()
        text_money_y = 60
        screen.blit(text_money, (text_money_x, text_money_y))

        text_level = font.render("level: {}".format(level), 1, (0, 0, 0))
        text_level_x = text_money_x
        text_level_y = 20
        screen.blit(text_level, (text_level_x, text_level_y))

        for i in barricade_sprites.sprites():  # проверка на проигрыш
            for k in enemies.sprites():
                if pygame.sprite.collide_mask(k, i):
                    attack = False
                    enemies.empty()
                    bullets.empty()
                    text_lose = font.render("Вы проиграли", 1, (0, 0, 0))
                    text_lose_x = width // 2 - text_lose.get_width() // 2
                    text_lose_y = 100
                    screen.blit(text_lose, (text_lose_x, text_lose_y))
                    pygame.display.flip()
                    restart = True
                    while restart:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                save(level, money)
                                terminate()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    save(level, money)
                                    heroes.empty()
                                    enemies.empty()
                                    bullets.empty()
                                    pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
                                    pygame.mixer.music.set_volume(0.3)
                                    pygame.mixer.music.play(-1)
                                    return
                                if event.key == pygame.K_SPACE:
                                    restart = False
        clock.tick(fps)
        pygame.display.flip()


menu_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Sprite()
menu_sprite.image = pygame.transform.scale(load_image("fon/main_menu.png"), (1100, 600))
menu_sprite.rect = menu_sprite.image.get_rect()
menu_sprites.add(menu_sprite)

pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and text_y <= event.pos[1] <= text_y + text.get_height() + 20:
                if text_x <= event.pos[0] <= text_x + text.get_width() + 20:  # кнопка НОВАЯ ИГРА
                    cur.execute("""UPDATE save
                                    SET level = '1',
                                        money = '0',
                                        hero_1 = '1 0',
                                        hero_2 = '',
                                        hero_3 = '',
                                        hero_4 = '',
                                        hero_5 = ''""")
                    con.commit()
                    play(cur.execute("""SELECT * FROM save""").fetchone())
                elif text_2_x <= event.pos[0] <= text_2_x + text_2.get_width() + 20:  # кнопка ЗАГРУЗИТЬ ИГРУ
                    play(cur.execute("""SELECT * FROM save""").fetchone())
                elif text_3_x <= event.pos[0] <= text_3_x + text_3.get_width() + 20:  # кнопка ВЫХОД
                    running = False

    menu_sprites.draw(screen)

    font = pygame.font.Font(None, 50)  # кнопка ИГРАТЬ
    text = font.render("Новая игра", 1, (0, 0, 0))
    text_x = 100
    text_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_x, text_y, text.get_width() + 20, text.get_height() + 20))
    screen.blit(text, (text_x + 10, text_y + 10))

    text_2 = font.render("Загрузить игру", 1, (0, 0, 0))  # кнопка ЗАГРУЗИТЬ ИГРУ
    text_2_x = 450
    text_2_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_2_x, text_2_y, text_2.get_width() + 20, text_2.get_height() + 20))
    screen.blit(text_2, (text_2_x + 10, text_2_y + 10))

    text_3 = font.render("Выход", 1, (0, 0, 0))  # кнопка ВЫХОД
    text_3_x = 850
    text_3_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_3_x, text_3_y, text_3.get_width() + 20, text_3.get_height() + 20))
    screen.blit(text_3, (text_3_x + 10, text_3_y + 10))

    pygame.display.flip()
