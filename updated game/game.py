import pygame, math
import pygame.freetype
import random
from random import choice


def startgame(board_size, num_colors):
    N = board_size  # Liczba rzędów trójkątów
    BOK = 100
    MARGIN = 50  # Margines na górze i na dole

    czerwony = (255, 0, 0)
    zielony = (0, 255, 0)
    niebieski = (0, 0, 255)
    zolty = (255, 255, 0)
    fioletowy = (128, 0, 128)
    pomaranczowy = (255, 160, 0)
    czarny = (0, 0, 0)

    kolory = [czerwony, zielony, niebieski, fioletowy, pomaranczowy, zolty]
    kolory = kolory[:num_colors]

    licznik_ruchow = 0

    # Inicjalizacja tablicy trójkątów z losowymi kolorami
    t = [[kolory[0] for _ in range(2 * i + 1)] for i in range(N)]

    # Lista sąsiadów
    sasiady = [[[] for _ in range(2 * i + 1)] for i in range(N)]

    # Funkcja budująca listę sąsiadów
    def zbuduj_liste_sasiadow():
        for k in range(N):
            for i in range(2 * k + 1):
                if i % 2 == 0:  # trójkąt do góry
                    if k == 0 and i == 0:
                        sasiady[k][i].append((k + 1, i + 1))

                    if k == (N - 1) and i == 0:
                        sasiady[k][i].append((k, i + 1))

                    if i == 0 and k != 0 and k != (N - 1):
                        sasiady[k][i].append((k, i + 1))
                        sasiady[k][i].append((k + 1, i + 1))

                    if i == (2 * k) and k != 0 and k == (N - 1):
                        sasiady[k][i].append((k, i - 1))

                    if i == (2 * k) and k != 0 and k != (N - 1):
                        sasiady[k][i].append((k, i - 1))
                        sasiady[k][i].append((k + 1, i + 1))

                    if i != 0 and i != (2 * k) and k != 0 and k != (N - 1):
                        sasiady[k][i].append((k, i - 1))
                        sasiady[k][i].append((k, i + 1))
                        sasiady[k][i].append((k + 1, i + 1))

                    if i != 0 and i != (2 * k) and k != 0 and k == (N - 1):
                        sasiady[k][i].append((k, i - 1))
                        sasiady[k][i].append((k, i + 1))

                else:  # trójkąt w dół
                    sasiady[k][i].append((k, i - 1))
                    sasiady[k][i].append((k, i + 1))
                    sasiady[k][i].append((k - 1, i - 1))

    # Funkcja rysująca trójkąt równoboczny z obramówką
    def trojkat(x, y, rozmiar, kolor):
        wysokosc = rozmiar * math.sqrt(3) / 2
        punkty = [
            (x, y),
            (x + rozmiar / 2, y + wysokosc),
            (x - rozmiar / 2, y + wysokosc)
        ]
        pygame.draw.polygon(win, kolor, punkty)
        pygame.draw.polygon(win, czarny, punkty, 3)  # Czarna obramówka

    # Funkcja rysująca odwrócony trójkąt równoboczny z obramówką
    def odwrocony_trojkat(x, y, rozmiar, kolor):
        wysokosc = rozmiar * math.sqrt(3) / 2
        punkty = [
            (x, y + wysokosc),
            (x + rozmiar / 2, y),
            (x - rozmiar / 2, y)
        ]
        pygame.draw.polygon(win, kolor, punkty)
        pygame.draw.polygon(win, czarny, punkty, 3)  # Czarna obramówka

    # Obliczenie szerokości i wysokości okna
    szerokosc_okna = N * BOK + 2 * MARGIN
    wysokosc_okna = int(N * BOK * math.sqrt(3) / 2) + 2 * MARGIN

    pygame.init()
    win = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
    pygame.display.set_caption("Moja gra")
    win.fill((255, 255, 255))

    # Funkcja rysująca całą planszę
    def rysuj_plansze():
        win.fill((0, 0, 0))
        start_x = szerokosc_okna // 2  # Początek na środku ekranu
        start_y = MARGIN

        for k in range(N):
            x = start_x - k * BOK / 2
            y = start_y + k * BOK * math.sqrt(3) / 2
            for i in range(2 * k + 1):
                if i % 2 == 0:
                    trojkat(x + (i // 2) * BOK, y, BOK, t[k][i])
                else:
                    odwrocony_trojkat(x + (i // 2) * BOK + BOK / 2, y, BOK, t[k][i])

        font.render_to(win, (szerokosc_okna // 2.6, 15), f"Ruchy: {licznik_ruchow}", (252, 203, 6))
        pygame.display.update()

    # Funkcja zmieniająca kolor trójkąta na następny z listy kolorów
    def zmien_kolor(k, i):
        obecny_kolor = t[k][i]
        nowy_kolor = kolory[(kolory.index(obecny_kolor) + 1) % len(kolory)]
        t[k][i] = nowy_kolor

    # Funkcja obsługująca kliknięcie
    def obsluga_klikniecia(k, i):
        nonlocal licznik_ruchow
        zmien_kolor(k, i)
        for sasiad in sasiady[k][i]:
            zmien_kolor(*sasiad)
        licznik_ruchow += 1
        rysuj_plansze()

    def create_triangle_mask(points, size):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.polygon(surface, (255, 255, 255, 255), points)
        return pygame.mask.from_surface(surface)

    # Funkcja do identyfikacji trójkąta na podstawie pozycji kliknięcia
    def znajdz_trojkat(pos):
        x, y = pos
        start_x = szerokosc_okna // 2
        start_y = MARGIN

        for k in range(N):
            row_y = start_y + k * BOK * math.sqrt(3) / 2
            row_x_start = start_x - k * BOK / 2
            for i in range(2 * k + 1):
                if i % 2 == 0:
                    # Wierzchołki trójkąta zwróconego w górę
                    ax, ay = row_x_start + (i // 2) * BOK, row_y
                    bx, by = ax + BOK / 2, ay + BOK * math.sqrt(3) / 2
                    cx, cy = ax - BOK / 2, ay + BOK * math.sqrt(3) / 2
                else:
                    # Wierzchołki trójkąta zwróconego w dół
                    ax, ay = row_x_start + (i // 2) * BOK + BOK / 2, row_y + BOK * math.sqrt(3) / 2
                    bx, by = ax - BOK / 2, ay - BOK * math.sqrt(3) / 2
                    cx, cy = ax + BOK / 2, ay - BOK * math.sqrt(3) / 2

                mask = create_triangle_mask([(ax, ay), (bx, by), (cx, cy)], (szerokosc_okna, wysokosc_okna))
                if mask.get_at((x, y)):
                    return k, i

        return None, None

    # Budujemy listę sąsiadów
    zbuduj_liste_sasiadow()

    for _ in range(50):
        k = random.randint(0, N - 1)
        i = random.randint(0, 2 * k)
        zmien_kolor(k, i)
        for sasiad in sasiady[k][i]:
            zmien_kolor(*sasiad)
    # Rysujemy planszę
    rysuj_plansze()

    # Główna pętla gry
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Sprawdza lewy przycisk myszy
                pos = pygame.mouse.get_pos()
                k, i = znajdz_trojkat(pos)
                if k is not None and i is not None:
                    obsluga_klikniecia(k, i)


# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Ekran startowy gry")

# Fonty
font = pygame.freetype.Font(None, 24)
font_title = pygame.freetype.Font(None, 32)
font_small = pygame.freetype.Font(None, 20)

# Zmienne dla pól tekstowych i przycisku
input_boxes = [
    pygame.Rect(200, 100, 200, 40),
    pygame.Rect(200, 200, 200, 40)
]
button = pygame.Rect(200, 300, 200, 50)
text = ["", ""]

# Opisy pól
labels = ["Rozmiar planszy:             (3-10)", "Ilość kolorów:                  (2-6)"]
game_description = "Kliknij w trójkąt aby zmienić kolor jego oraz sąsiadów."
game_description2 = "Celem gry jest pokolorwanie planszy jednym kolorem."


# Funkcja do rysowania pól tekstowych z etykietami
def draw_textbox(screen, rect, text, label):
    pygame.draw.rect(screen, (169, 169, 169), rect)
    pygame.draw.rect(screen, (255, 140, 0), rect, 2)
    font.render_to(screen, (rect.x + 5, rect.y + 10), text, (0, 0, 0))
    font.render_to(screen, (rect.x, rect.y - 30), label, (0, 255, 0))


# Funkcja do rysowania przycisku
def draw_button(screen, rect, text):
    pygame.draw.rect(screen, (0, 0, 128), rect)
    font.render_to(screen, (rect.x + (rect.width - 73) / 2, rect.y + 15), text, (255, 255, 255))


def validate_data(board_size, num_colors):
    global error_message
    if not (3 <= board_size <= 10):
        error_message = "Rozmiar planszy musi być między 3 a 10."
        print(error_message)
        return False
    if not (2 <= num_colors <= 6):
        error_message = "Ilość kolorów musi być między 2 a 6."
        print(error_message)
        return False
    error_message = ""
    return True


error_message = ""

# Główna pętla programu
running = True
active_index = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            active_index = None
            for index, rect in enumerate(input_boxes):
                if rect.collidepoint(event.pos):
                    active_index = index
            if button.collidepoint(event.pos):
                try:
                    board_size = int(text[0])
                    num_colors = int(text[1])
                    if validate_data(board_size, num_colors):
                        startgame(board_size, num_colors)  # Wywołaj funkcję startującą grę
                        print("Rozpoczynam grę!")
                        print(f"Rozmiar planszy: {board_size}, Ilość kolorów: {num_colors}")
                except ValueError:
                    error_message = "Wprowadzono nieprawidłowe dane."
                    print("Wprowadzono nieprawidłowe dane.")
        elif event.type == pygame.KEYDOWN and active_index is not None:
            if event.key == pygame.K_BACKSPACE:
                text[active_index] = text[active_index][:-1]
            elif event.key <= 127:
                text[active_index] += event.unicode

    screen.fill((0, 0, 0))
    for i, rect in enumerate(input_boxes):
        draw_textbox(screen, rect, text[i], labels[i])
    draw_button(screen, button, "START")
    font_small.render_to(screen, (40, 375), game_description, (252, 203, 6))
    font_small.render_to(screen, (40, 410), game_description2, (252, 203, 6))

    if error_message:
        font.render_to(screen, (100, 450), error_message, (173, 52, 62))
    pygame.display.flip()

pygame.quit()