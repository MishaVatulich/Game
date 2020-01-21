import pygame
import os
import sys
import random
import sqlite3
import math

pygame.init()
size = width, height = 1100, 700
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


def sorting(group):  # сортирует группу, чтобы спрайты не накладывались
    sorted_group = sorted(group.sprites(), key=lambda x: x.rect.y + x.rect.height)  # сортирует по низу
    group.empty()
    for i in sorted_group:
        group.add(i)


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
        self.hero = random.choice(heroes.sprites())
        heroes.remove(self.hero)

    def update(self, effect):
        global money
        if self.hp <= 0:
            money += self.money
            enemies.remove(self)
            heroes.add(self.hero)
            sorting(heroes)
            heroes.sprites()[-1].shooting = True
            return
        self.x -= self.speed * effect / fps  # не целое число
        self.rect.x = int(self.x)


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
        self.money = 20
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
        if int(pos) < 2:
            self.rect.x = 140 * (int(pos) % 2)
            self.rect.y = 200 + int(pos)  # чтобы 1 герой был на пиксель нижу другого для сортировки
        elif int(pos) == 2:
            self.rect.x = 70
            self.rect.y = 300
        else:
            self.rect.x = 140 * ((int(pos) - 1) % 2)
            self.rect.y = 400 + int(pos) // 4  # чтобы 1 герой был на пиксель нижу другого для сортировки
        self.level = int(level)
        self.buy_cost = 10 + int(pos) * 30  # цена покупки следующего героя
        self.upgrade_cost = self.level * 5  # цена улучшения
        self.shooting = True

    def shoot(self, x, y):
        if self.level < 20:
            shooting_speed = 1000 - 50 * self.level
        else:
            shooting_speed = 50
        if self.shooting is True:
            Bullet(self.rect.x + self.rect.width, self.rect.y + 30, x, y, self.level)
            self.shooting = False
            pygame.time.set_timer(20 + heroes.sprites().index(self), shooting_speed)


def terminate():
    pygame.quit()
    sys.exit()


def generate_enemies(level):  # генерация врагов
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
    for _ in range(level // 15):
        Scp106(level)
    sorting(enemies)


def save(level, money):  # сохранение игры
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


def information():
    size_2 = 1500, 825
    screen = pygame.display.set_mode(size_2)

    inform_text_1 = ["Здравствуй, дорогой игрок!", "",
                     "Ты играешь в игру под названием SCP-Defence",
                     "В секретном комплексе произошла авария, из-за которой многие монстры вырвались наружу.",
                     "Твоя задача – не дать им выбраться за территорию зоны. ",
                     "Управление:",
                     "1)Для стрельбы удерживайте левую кнопку мыши",
                     "!Помни, что монстры двигаются и тебе нужно стрелять на упреждение",
                     "2)Нажми SPACE для перезапуска уровня, когда ты проиграл",
                     "3)Нажми ESCAPE для выхода в главное меню",
                     "Игра автоматически сохраняется, когда ты выходишь",
                     "Приятной игры!", "",
                     "Информация про монстров:",
                     "SCP 049",
                     "Здоровье: 200",
                     "Скорость: 43",
                     "Деньги за убийстово: 6",
                     "Способности: увеличивает",
                     "скорость всех SCP на 5%", "",
                     "SCP 049-2",
                     "Здоровье: 100",
                     "Скорость: 51",
                     "Деньги за убийстово: 1"]

    inform_text_2 = ["SCP 106",
                     "Здоровье: 300",
                     "Скорость: 43",
                     "Деньги за убийстово: 20",
                     "Способности: забирает одного",
                     "твоего персонажа до своей смерти", "",
                     "SCP 173",
                     "Здоровье: 70",
                     "Скорость: 90",
                     "Деньги за убийстово: 5"]

    inform_text_3 = ["SCP 178-1",
                     "Здоровье: 100",
                     "Скорость: 34",
                     "Деньги за убийстово: 6",
                     "Способности: уменьшает урон",
                     "твоих персонажей на 5%", "",
                     "SCP 682",
                     "Здоровье: 700",
                     "Скорость: 26",
                     "Деньги за убийстово: 20"]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode(size)
                    run = False
        screen.blit(pygame.transform.scale(load_image("fon/fon_2.png"), (1500, 825)), (0, 0))
        screen.blit(Scp049.image, (240, 430))
        screen.blit(pygame.transform.scale(Scp049Two.image, (151, 200)), (240, 620))
        screen.blit(Scp106.image, (810, 390))
        screen.blit(pygame.transform.scale(Scp173.image, (67, 200)), (780, 620))
        screen.blit(Scp178One.image, (1160, 400))
        screen.blit(pygame.transform.scale(Scp682.image, (260, 150)), (1230, 650))

        font = pygame.font.Font(None, 30)
        text_coord = 0
        for line in inform_text_1:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        text_coord = 430
        for line in inform_text_2:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            inform_rect = string_rendered.get_rect()
            text_coord += 10
            inform_rect.top = text_coord
            inform_rect.x = 450
            text_coord += inform_rect.height
            screen.blit(string_rendered, inform_rect)

        text_coord = 430
        for line in inform_text_3:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            inform2_rect = string_rendered.get_rect()
            text_coord += 10
            inform2_rect.top = text_coord
            inform2_rect.x = 975
            text_coord += inform2_rect.height
            screen.blit(string_rendered, inform2_rect)

        pygame.display.flip()


def play(args):  # 'окно' игры
    global money
    fon_sprites = pygame.sprite.Group()
    fon_sprite = pygame.sprite.Sprite()
    fon_sprite.image = pygame.transform.scale(load_image("fon/fon_1.png"), (width, height - 100))
    fon_sprite.rect = fon_sprite.image.get_rect()
    fon_sprites.add(fon_sprite)

    fon_sprite_2 = pygame.sprite.Sprite()
    fon_sprite_2.image = pygame.transform.scale(load_image("fon/fon_2.png"), (width, 100))
    fon_sprite_2.rect = fon_sprite.image.get_rect()
    fon_sprite_2.rect.y = 600
    fon_sprites.add(fon_sprite_2)

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
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    level = args[1]
    money = args[2]

    for i in range(3, 8):
        if args[i] != '':
            Hero(args[i].split()[0], args[i].split()[1])

    if len(heroes.sprites()) == 5:
        sorting(heroes)
    upgrading_hero = heroes.sprites()[0]  # улучшаемый герой
    attack = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for j in enemies.sprites():  # возвращение героев из измерения деда
                    if isinstance(j, Scp106):
                        heroes.add(j.hero)
                        sorting(heroes)
                        heroes.sprites()[-1].shooting = True
                save(level, money)
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 635 <= event.pos[1] <= 665 and 20 <= event.pos[0] <= 350 and (event.pos[0] - 20) % 70 <= 50:
                        upgrading_hero = heroes.sprites()[(event.pos[0] - 20) // 70]  # кнопки выбора персонажей
                    if 610 <= event.pos[1] <= 655 and not attack:
                        if 750 <= event.pos[0] <= 932 and money >= upgrading_hero.upgrade_cost:  # кнопка улучшения
                            money -= upgrading_hero.upgrade_cost
                            upgrading_hero.level += 1
                            upgrading_hero.upgrade_cost = upgrading_hero.level * 5
                        if 950 <= event.pos[0] <= 1081 and money >= heroes.sprites()[-1].buy_cost and \
                           len(heroes.sprites()) < 5:  # кнопка покупки
                            money -= heroes.sprites()[-1].buy_cost
                            Hero(1, len(heroes.sprites()))
                            sorting(heroes)
                if 491 <= event.pos[0] <= 619 and 10 <= event.pos[1] <= 55 and not attack:  # кнопка НАЧАТЬ
                    attack = True
                    generate_enemies(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for j in enemies.sprites():  # возвращение героев из измерения деда
                        if isinstance(j, Scp106):
                            heroes.add(j.hero)
                            sorting(heroes)
                            heroes.sprites()[-1].shooting = True
                    save(level, money)
                    heroes.empty()
                    enemies.empty()
                    bullets.empty()
                    pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(-1)
                    return
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

        if pygame.mouse.get_pressed()[0] == 1 and pygame.mouse.get_pos()[1] <= 600 and pygame.mouse.get_pos()[0] >= 210:
            for i in heroes.sprites():  # стрельба
                i.shoot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        if attack:
            if len(enemies.sprites()) == 0:  # проверка на победу
                attack = False
                level += 1
            scp_049 = scp_178 = 0
            for i in enemies.sprites():  # считается кол-во врагов, которые могут накладывать эффекты
                if isinstance(i, Scp049):
                    scp_049 += 1
                elif isinstance(i, Scp178One):
                    scp_178 += 1
            enemies.update(scp_049 * 0.05 + 1)  # scp 049 увеличивает скорость на 5 %. Эффект сумируется
            bullets.update(1 - scp_178 * 0.05)  # scp 178-1 уменьшает урон на 5 %. Эффект сумируется

        for i in barricade_sprites.sprites():  # проверка на проигрыш
            for k in enemies.sprites():
                if pygame.sprite.collide_mask(k, i):
                    attack = False
                    for j in enemies.sprites():  # возвращение героев из измерения деда
                        if isinstance(j, Scp106):
                            heroes.add(j.hero)
                            sorting(heroes)
                            heroes.sprites()[-1].shooting = True
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
                                    pygame.mixer.music.set_volume(volume)
                                    pygame.mixer.music.play(-1)
                                    return
                                if event.key == pygame.K_SPACE:
                                    restart = False

        fon_sprites.draw(screen)
        barricade_sprites.draw(screen)
        enemies.draw(screen)
        heroes.draw(screen)
        bullets.draw(screen)
        bullets.update()

        if not attack:
            for i in range(len(heroes.sprites())):  # кнопки выбора персонажа
                pygame.draw.rect(screen, (255, 255, 255), (20 + i * 70, 635, 50, 30), 1)
                hero_number = font.render(str(i + 1), 1, (255, 255, 255))
                screen.blit(hero_number, (35 + i * 70, 635))

            text_level = font.render("Уровень: {}".format(upgrading_hero.level), 1, (0, 0, 0))  # уровень героя
            text_level_x = 440
            text_level_y = 610
            screen.blit(text_level, (text_level_x, text_level_y))

            text_damage = font.render("Урон: {}".format(upgrading_hero.level * 5 + 20), 1, (0, 0, 0))  # уровень героя
            text_damage_x = 440
            text_damage_y = 660
            screen.blit(text_damage, (text_damage_x, text_damage_y))

        if len(heroes.sprites()) < 5 and not attack:
            text_buy = font.render("Купить", 1, (0, 0, 0))  # кнопка купить
            text_buy_x = 950
            text_buy_y = 610
            pygame.draw.rect(screen, (255, 255, 255), (text_buy_x, text_buy_y, text_buy.get_width() + 10,
                                                       text_buy.get_height() + 10))
            screen.blit(text_buy, (text_buy_x + 5, text_buy_y + 5))

            text_buy = font.render("{}$".format(heroes.sprites()[-1].buy_cost), 1, (0, 0, 0))  # цена покупки
            text_buy_x = 1015 - text_buy.get_width() // 2
            text_buy_y = 660
            screen.blit(text_buy, (text_buy_x, text_buy_y))

        if not attack:
            text_upgrade = font.render("Улучшить", 1, (0, 0, 0))  # кнопка улучшить
            text_upgrade_x = 750
            text_upgrade_y = 610
            pygame.draw.rect(screen, (255, 255, 255), (text_upgrade_x, text_upgrade_y, text_upgrade.get_width() + 10,
                                                       text_upgrade.get_height() + 10))
            screen.blit(text_upgrade, (text_upgrade_x + 5, text_upgrade_y + 5))

            text_upgrade = font.render("{}$".format(upgrading_hero.upgrade_cost), 1, (0, 0, 0))  # цена улучшения
            text_upgrade_x = 841 - text_upgrade.get_width() // 2
            text_upgrade_y = 660
            screen.blit(text_upgrade, (text_upgrade_x, text_upgrade_y))

        if not attack:
            text_start = font.render("Начать", 1, (255, 255, 255))  # кнопка НАЧАТЬ
            text_start_x = width // 2 - text_start.get_width() // 2
            text_start_y = 10
            pygame.draw.rect(screen, pygame.Color('red'), (text_start_x, text_start_y, text_start.get_width() + 10,
                                                           text_start.get_height() + 10))
            screen.blit(text_start, (text_start_x + 5, text_start_y + 5))

        text_money = font.render("money: {}$".format(money), 1, (0, 0, 0))  # деньги игрока
        text_money_x = width - 20 - text_money.get_width()
        text_money_y = 60
        screen.blit(text_money, (text_money_x, text_money_y))

        text_level = font.render("level: {}".format(level), 1, (0, 0, 0))  # уровень игрока
        text_level_x = text_money_x
        text_level_y = 20
        screen.blit(text_level, (text_level_x, text_level_y))

        clock.tick(fps)
        pygame.display.flip()


menu_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Sprite()
menu_sprite.image = pygame.transform.scale(load_image("fon/main_menu.png"), (width, height))
menu_sprite.rect = menu_sprite.image.get_rect()
menu_sprites.add(menu_sprite)

sound_x = 545
volume = (sound_x - 495) / 100

pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
pygame.mixer.music.set_volume(volume)
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
            if event.button == 1 and text_4_y <= event.pos[1] <= text_4_y + text_4.get_height() + 20 and \
               text_4_x <= event.pos[0] <= text_4_x + text_4.get_width() + 20:  # кнопка ИНФОРМАЦИЯ
                information()

    if pygame.mouse.get_pressed()[0] == 1 and sound_x <= pygame.mouse.get_pos()[0] <= sound_x + 10:
        if 500 <= pygame.mouse.get_pos()[0] <= 600:  # изменение громкости звука
            sound_x = pygame.mouse.get_pos()[0] - 5
            volume = (sound_x - 495) / 100
            pygame.mixer.music.set_volume(volume)

    menu_sprites.draw(screen)

    font = pygame.font.Font(None, 50)  # кнопка ИГРАТЬ
    text = font.render("Новая игра", 1, (0, 0, 0))
    text_x = 100
    text_y = 590
    pygame.draw.rect(screen, (255, 255, 255), (text_x, text_y, text.get_width() + 20, text.get_height() + 20))
    screen.blit(text, (text_x + 10, text_y + 10))

    text_2 = font.render("Загрузить игру", 1, (0, 0, 0))  # кнопка ЗАГРУЗИТЬ ИГРУ
    text_2_x = 450
    text_2_y = 590
    pygame.draw.rect(screen, (255, 255, 255), (text_2_x, text_2_y, text_2.get_width() + 20, text_2.get_height() + 20))
    screen.blit(text_2, (text_2_x + 10, text_2_y + 10))

    text_3 = font.render("Выход", 1, (0, 0, 0))  # кнопка ВЫХОД
    text_3_x = 850
    text_3_y = 590
    pygame.draw.rect(screen, (255, 255, 255), (text_3_x, text_3_y, text_3.get_width() + 20, text_3.get_height() + 20))
    screen.blit(text_3, (text_3_x + 10, text_3_y + 10))

    text_4 = font.render("Информация", 1, (0, 0, 0))  # кнопка информация
    text_4_x = 465
    text_4_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_4_x, text_4_y, text_4.get_width() + 20, text_4.get_height() + 20))
    screen.blit(text_4, (text_4_x + 10, text_4_y + 10))

    text_5 = font.render("Громкость", 1, (255, 255, 255))  # громкость
    text_5_x = 450
    text_5_y = 20
    screen.blit(text_5, (text_5_x + 10, text_5_y + 10))

    pygame.draw.line(screen, (255, 255, 255), (495, 90), (605, 90), 5)
    pygame.draw.rect(screen, (255, 255, 255), (sound_x, 80, 10, 20))

    pygame.display.flip()
