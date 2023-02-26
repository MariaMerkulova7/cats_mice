import pygame
from random import randint
import sys
from pygame.locals import *
from const import *


# Функция, отключающая программу
def terminate():
    pygame.quit()
    sys.exit()


# Функция ожидания нажатия кнопки
def waiting_for_pressed_button():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# Функция проверки столкновения игрока с кошкой
def mouse_met_cats(mouse_rect, cats):
    center_of_mouse = mouse_rect.center
    for i in cats:
        if i['rect'].collidepoint(center_of_mouse):
            return True
    return False


# Функция написания текста. Имеет 3 "мода"
# 1ый - основной текст программы, 2ой - текст поздравительного сообщения, 3ий - текст почты создателя
def writing_text(text, font, surface, x, y, mode=1):
    if mode == 1:
        textrect = font.render(text, 1, TEXTCOLOR).get_rect()
        textrect.topleft = (x, y)
        surface.blit(font.render(text, 1, TEXTCOLOR), textrect)
    elif mode == 2:
        textrect = font.render(text, 1, TEXTCOLOR2).get_rect()
        textrect.topleft = (x, y)
        surface.blit(font.render(text, 1, TEXTCOLOR2), textrect)
    elif mode == 3:
        textrect = font.render(text, 1, (23, 69, 63)).get_rect()
        textrect.topleft = (x, y)
        surface.blit(font.render(text, 1, (23, 69, 63)), textrect)


# Настройка окна
pygame.init()
mainClock = pygame.time.Clock()
surf = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Кошки-мышки')
pygame.mouse.set_visible(False)

# Настройка музыки
gameOverSound = pygame.mixer.Sound('data/game_over.mp3')
pygame.mixer.music.load('data/bg.mp3')

# Настройка шрифтов
font = pygame.font.SysFont(None, 50)

# Настройка картинки мышки
mouse_img = pygame.transform.scale(pygame.image.load('data/scared_mouse.png'), (75, 75))
mouse_rect = mouse_img.get_rect()

# Настройка картинки кошки
cats_img = pygame.image.load('data/skinny_cat.png')

# Настройка изображения мышки на приветственном окне
logo = pygame.transform.scale(pygame.image.load('data/scared_mouse.png'), (100, 100))
logo_rect = logo.get_rect(center=(WIDTH / 2 + 100, HEIGHT / 2 + 100))

# Настройка изображения кошки на приветственном окне
logo2 = pygame.transform.scale(cats_img, (150, 150))
logo2_rect = logo2.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

# Отображение приветственного окна
surf.fill(BACKGROUND_COLOR_START)

# Отбражение всех элементов приветственного окна
surf.blit(logo, logo_rect)
surf.blit(logo2, logo2_rect)
writing_text('Игра "Кошки-мышки"', font, surf, (WIDTH / 2) - 185, (HEIGHT / 3))
writing_text('Нажмите любую кнопку, чтобы начать', font, surf, (WIDTH / 2) - 325, (HEIGHT / 3) + 50)
writing_text('marym271007@yandex.ru', pygame.font.SysFont(None, 20), surf, 20, HEIGHT - 20, 3)

pygame.display.update()

waiting_for_pressed_button()

# Открытие файла с информацией о лучшей попытке в режиме дописывания, что даёт нам его создание при его отсутствии
with open("data/record.txt", mode='a', encoding="utf-8"):
    pass

# Открытие файла с информацией о лучшей попытке
with open("data/record.txt", encoding="utf-8") as f:
    text = f.readline()
if text:
    info = int(text)
else:
    info = 0

# Игровой процесс
while True:
    # Настройка начала игры
    cats = []
    record_now = 0
    mouse_rect.topleft = (WIDTH / 2 - 37, HEIGHT - 75)
    left = False
    right = False
    up = False
    down = False
    cheating_reverse_cats = False
    cheating_slow_cats = False
    add_cat = 0
    fps = FPS
    pygame.mixer.music.play(-1, 0.0)

    # Цикл выполняется пока игра идет
    while True:
        record_now += 1

        # Увеличение fps на 1 каждые 100 очков
        if record_now % 100 == 0:
            fps += 1

        for event in pygame.event.get():
            # Если пользователь нажал на крестик, программа закрывается
            if event.type == QUIT:
                terminate()

            # Обработка события, когда клавиша зажата
            if event.type == KEYDOWN:
                # Случай жульничества
                if event.key == K_z:
                    cheating_reverse_cats = True
                if event.key == K_x:
                    cheating_slow_cats = True

                # Случай зажатия клавиш движения
                if event.key == K_UP or event.key == K_w:
                    down = False
                    up = True
                if event.key == K_DOWN or event.key == K_s:
                    up = False
                    down = True

                if event.key == K_LEFT or event.key == K_a:
                    right = False
                    left = True
                if event.key == K_RIGHT or event.key == K_d:
                    left = False
                    right = True

            # Обработка события, когда клавишу отпустили
            if event.type == KEYUP:
                # Случай жульничества
                if event.key == K_z:
                    cheating_reverse_cats = False
                if event.key == K_x:
                    cheating_slow_cats = False
                if event.key == K_ESCAPE:
                    terminate()

                # Случай отпускания клавиш движения
                if event.key == K_UP or event.key == K_w:
                    up = False
                if event.key == K_DOWN or event.key == K_s:
                    down = False

                if event.key == K_LEFT or event.key == K_a:
                    left = False
                if event.key == K_RIGHT or event.key == K_d:
                    right = False

            # Обработка события движения компьютерной мыши: перемещение игрока к курсору мыши
            if event.type == MOUSEMOTION:
                if HEIGHT - 25 > event.pos[1] > 75:
                    mouse_rect.centery = event.pos[1]
                if WIDTH - 25 > event.pos[0] > 25:
                    mouse_rect.centerx = event.pos[0]

        # Добавление кошек, если это необходимо
        if not cheating_reverse_cats and not cheating_slow_cats:
            add_cat += 1
        if add_cat == TIME_OF_NEW_CATS:
            add_cat = 0
            size_of_cats = randint(MIN_SIZE_OF_CAT, MAX_SIZE_OF_CAT)
            new_cat = {'rect': pygame.Rect(randint(0, WIDTH - size_of_cats), 0 - size_of_cats, size_of_cats,
                                           size_of_cats),
                       'speed': randint(MIN_SPEED_OF_CAT, MAX_SPEED_OF_CAT),
                       'surface': pygame.transform.scale(cats_img, (size_of_cats, size_of_cats)),
                       }

            cats.append(new_cat)

        # Перемещение игрока-мышки
        if up and mouse_rect.top > 50:
            mouse_rect.move_ip(0, -1 * MOUSE_STEP)

        if down and mouse_rect.bottom < HEIGHT:
            mouse_rect.move_ip(0, MOUSE_STEP)

        if left and mouse_rect.left > 0:
            mouse_rect.move_ip(-1 * MOUSE_STEP, 0)

        if right and mouse_rect.right < WIDTH:
            mouse_rect.move_ip(MOUSE_STEP, 0)

        # Падение кошек
        for c in cats:
            if not cheating_reverse_cats and not cheating_slow_cats:
                c['rect'].move_ip(0, c['speed'])

            elif cheating_reverse_cats:
                c['rect'].move_ip(0, -5)

            elif cheating_slow_cats:
                c['rect'].move_ip(0, 1)

        # Убираем кошек, ушедших за границы экрана
        for c in cats:
            if c['rect'].top > HEIGHT:
                cats.remove(c)

        # Отображение окна
        surf.fill(BACKGROUND_COLOR_GAME)

        surf.blit(mouse_img, mouse_rect)

        for c in cats:
            surf.blit(c['surface'], c['rect'])

        pygame.draw.rect(surf, (121, 104, 186), (0, 0, WIDTH, 50), 5)
        pygame.draw.rect(surf, (179, 227, 221), (5, 5, WIDTH - 10, 40), 0)

        # Вывод информации о текущем количестве очков
        writing_text(f'Счёт: {record_now}', font, surf, 10, 5)

        # Считывание информации из файла о лучшей попытке и вывод ее на экран
        with open("data/record.txt", encoding="utf-8") as f:
            text = f.readline()
        if text:
            info = int(text)
        else:
            info = 0

        writing_text(f'Лучшая попытка: {info}', font, surf, WIDTH - 400, 5)

        pygame.display.update()

        # Обработка окончания игры
        if mouse_met_cats(mouse_rect, cats):
            fps = FPS

            # открываем файл с  информацией о лучшей попытке
            with open("data/record.txt", encoding="utf-8") as f:
                text = f.readline()

            # сверяем набранное количество очков с лучшей попыткой
            # если набранное количество очков больше рекорда, то выводится поздравительное слово и кубок
            if text and record_now > int(text) or not text:
                with open("data/record.txt", encoding="utf-8", mode="w") as f:
                    f.write(str(record_now))

                pygame.draw.rect(surf, (121, 104, 186), ((WIDTH / 2) - 425, (HEIGHT / 3) - 20, (WIDTH / 2) + 360, 170),
                                 5)

                pygame.draw.rect(surf, (242, 188, 247), ((WIDTH / 2) - 420, (HEIGHT / 3) - 15, (WIDTH / 2) + 350, 160),
                                 0)

                writing_text('Ура, новый рекорд!!!', font, surf, (WIDTH / 2) - 180, (HEIGHT / 2), 2)

                prize_img = pygame.transform.scale(pygame.image.load('data/kubok.png'), (200, 200))
                prize_rect = prize_img.get_rect(center=((WIDTH / 2) - 25, (HEIGHT / 4) * 3))

                surf.blit(prize_img, prize_rect)
            else:
                pygame.draw.rect(surf, (121, 104, 186), ((WIDTH / 2) - 425, (HEIGHT / 3) - 20, (WIDTH / 2) + 360, 120),
                                 5)

                pygame.draw.rect(surf, (242, 188, 247), ((WIDTH / 2) - 420, (HEIGHT / 3) - 15, (WIDTH / 2) + 350, 110),
                                 0)
            break

        mainClock.tick(fps)

    # Завершение игры
    pygame.mixer.music.stop()
    gameOverSound.play()

    # Вывод информации об окончании игры
    writing_text('Игра закончилась!', font, surf, (WIDTH / 2) - 160, (HEIGHT / 3))
    writing_text('Нажмите любую кнопку, чтобы запустить снова', font, surf, (WIDTH / 2) - 405, (HEIGHT / 3) + 50)

    pygame.display.update()
    waiting_for_pressed_button()

    gameOverSound.stop()
