# -*- coding: utf-8 -*-
import pygame
import sys
end = None
# Stałe
ROWS = 6
COLS = 7
SQSIZE = 100
RADIUS = SQSIZE // 2 - 5
WIDTH = COLS * SQSIZE
HEIGHT = (ROWS + 1) * SQSIZE
SIZE = (WIDTH, HEIGHT)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Cztery w rzędzie")
font = pygame.font.SysFont("monospace", 75)

# Funkcje
def rysuj_plansze(plansza):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLACK, (c * SQSIZE, r * SQSIZE + SQSIZE, SQSIZE, SQSIZE))
            pygame.draw.circle(screen, WHITE, (c * SQSIZE + SQSIZE // 2, r * SQSIZE + SQSIZE // 2 + SQSIZE), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if plansza[r][c] == 'X':
                pygame.draw.circle(screen, RED, (c * SQSIZE + SQSIZE // 2, HEIGHT - (r * SQSIZE + SQSIZE // 2)), RADIUS)
            elif plansza[r][c] == 'O':
                pygame.draw.circle(screen, YELLOW, (c * SQSIZE + SQSIZE // 2, HEIGHT - (r * SQSIZE + SQSIZE // 2)), RADIUS)
    pygame.display.update()

def ocena_stanu(s):
    '''Ocena stanu planszy. Zwraca dodatnią liczbę jeśli wygrywa "O", ujemną jeśli "X" wygrywa.'''
    for w in range(6):
        for k in range(4):
            if s[w][k] != ' ' and all(s[w][k] == s[w][k+i] for i in range(4)):
                return 1000 if s[w][k] == 'O' else -1000
    for w in range(3):
        for k in range(7):
            if s[w][k] != ' ' and all(s[w][k] == s[w+i][k] for i in range(4)):
                return 1000 if s[w][k] == 'O' else -1000
    for w in range(3):
        for k in range(4):
            if s[w][k] != ' ' and all(s[w][k] == s[w+i][k+i] for i in range(4)):
                return 1000 if s[w][k] == 'O' else -1000
    for w in range(3):
        for k in range(3, 7):
            if s[w][k] != ' ' and all(s[w][k] == s[w+i][k-i] for i in range(4)):
                return 1000 if s[w][k] == 'O' else -1000
    return 0

def minimax(s, depth, alpha, beta, is_maximizing):
    k = czy_koniec(s)
    if k is not None:
        if k == 'X':
            return -1000
        elif k == 'O':
            return 1000
        else:
            return 0

    if depth == 0:
        return ocena_stanu(s)

    if is_maximizing:
        max_eval = -float('inf')
        for k in range(7):
            for w in range(5, -1, -1):
                if s[w][k] == ' ':
                    s[w][k] = 'O'
                    eval = minimax(s, depth-1, alpha, beta, False)
                    s[w][k] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for k in range(7):
            for w in range(5, -1, -1):
                if s[w][k] == ' ':
                    s[w][k] = 'X'
                    eval = minimax(s, depth-1, alpha, beta, True)
                    s[w][k] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def ruch_komp(s):
    '''wykonuje ruch komputera przy użyciu algorytmu Minimax z przycinaniem alfa-beta'''
    best_score = -float('inf')
    best_col = None
    for k in range(7):
        for w in range(5, -1, -1):
            if s[w][k] == ' ':
                s[w][k] = 'O'
                score = minimax(s, 4, -float('inf'), float('inf'), False)
                s[w][k] = ' '
                if score > best_score:
                    best_score = score
                    best_col = k
                break

    for w in range(5, -1, -1):
        if s[w][best_col] == ' ':
            s[w][best_col] = 'O'
            return

def czy_koniec(s):
    '''sprawdza czy natapil koniec gry. Zwraca:
      'X' lub 'O' gdy jedna ze stron wyrala
      '?' gdy zapelniono plansze i nikt nie wygral
      None gdy gre nalezy kontynuowac'''

    # czy s  4 w poziomie
    for w in range(6):
        for k in range(4):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w][k + i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s  4 w pionie
    for w in range(3):
        for k in range(7):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s  4 uko nie \
    for w in range(3):
        for k in range(4):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k + i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy s  4 uko nie /
    for w in range(3):
        for k in range(3, 7):
            if s[w][k] == ' ': continue
            for i in range(1, 4):
                if s[w + i][k - i] != s[w][k]: break
            else:
                return s[w][k]
            end
        end
    end

    # czy plansza jest pelna
    for k in range(7):
        if s[0][k] == ' ': break
    else:
        return '?'
    end

    return None

def main():
    plansza = [[' ' for _ in range(7)] for _ in range(6)]
    rysuj_plansze(plansza)
    game_over = False
    turn = 0  # 0 - gracz, 1 - komputer

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQSIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, SQSIZE // 2), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    posx = event.pos[0]
                    col = posx // SQSIZE

                    if plansza[0][col] == ' ':
                        for r in range(5, -1, -1):
                            if plansza[r][col] == ' ':
                                plansza[r][col] = 'X'
                                break

                        rysuj_plansze(plansza)

                        if czy_koniec(plansza) is not None:
                            game_over = True
                            winner = czy_koniec(plansza)
                            break

                        turn = 1

        if turn == 1 and not game_over:
            ruch_komp(plansza)
            rysuj_plansze(plansza)

            if czy_koniec(plansza) is not None:
                game_over = True
                winner = czy_koniec(plansza)

            turn = 0

        if game_over:
            if winner == 'X':
                label = font.render("Gracz wygrał!", 1, RED)
            elif winner == 'O':
                label = font.render("Komputer wygrał!", 1, YELLOW)
            else:
                label = font.render("Remis!", 1, WHITE)

            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQSIZE))
            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()

if __name__ == "__main__":
    main()
