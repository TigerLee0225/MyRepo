import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 크기 설정
s_width = 800
s_height = 700
play_width = 300  # 300 // 10 = 30, 블록 하나의 크기
play_height = 600  # 600 // 20 = 30
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# 색상 정의
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# 블록 형태 정의
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (255, 165, 0),  # J
    (0, 0, 255),    # L
    (128, 0, 128)   # T
]

# 클래스 정의
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[black for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j - 2, shape.y + i - 4))
    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(
        10) if grid[i][j] == black] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('malgungothic', size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, gray, (sx, sy + i*block_size),
                         (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, gray, (sx + j*block_size, sy),
                             (sx + j*block_size, sy + play_height))

def clear_rows(grid, locked):
    inc = 0
    ind = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if black not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('malgungothic', 30)
    label = font.render('다음 블록', True, white)

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    surface.blit(label, (sx + 10, sy - 30))

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size,
                                 sy + i*block_size, block_size, block_size), 0)

def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    try:
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()
    except:
        score = 0
    return score

def draw_window(surface, grid, score=0, level=1):
    surface.fill(black)

    # 제목
    font = pygame.font.SysFont('malgungothic', 60)
    label = font.render('테트리스', True, white)

    surface.blit(label, (top_left_x + play_width / 2 -
                         (label.get_width() / 2), 30))

    # 현재 점수
    font = pygame.font.SysFont('malgungothic', 30)
    label = font.render(f'점수: {score}', True, white)

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 10, sy + 150))

    # 최고 점수
    label = font.render(f'최고 점수: {max_score()}', True, white)
    surface.blit(label, (sx - 20, sy + 200))

    # 레벨 표시
    label = font.render(f'레벨: {level}', True, white)
    surface.blit(label, (sx + 10, sy + 250))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                             top_left_y + i*block_size, block_size, block_size), 0)

    # 격자 그리기
    draw_grid(surface, grid)

    # 경계선 그리기
    pygame.draw.rect(surface, red, (top_left_x, top_left_y,
                     play_width, play_height), 5)

def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    level = 1
    fall_speed = 0.5
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # 레벨 업 조건 (15초마다 레벨 증가)
        if level_time / 1000 > 15:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.02
            level += 1
            if level > 30:
                level = 30  # 최대 레벨 30 유지

        # 블록 떨어지는 속도 조절
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        # 블록 위치 업데이트
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # 블록 교체 및 점수 업데이트
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            cleared_rows = clear_rows(grid, locked_positions)
            if cleared_rows > 0:
                score += cleared_rows * 10

        draw_window(win, grid, score, level)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # 게임 오버 검사
        if check_lost(locked_positions):
            draw_text_middle("게임 오버", 80, white, win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu():
    run = True
    while run:
        win.fill(black)
        draw_text_middle('테트리스 게임 시작하려면 아무 키나 누르세요', 30, white, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

# 게임 실행
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('테트리스')

red = (255, 0, 0)
main_menu()  # 시작 화면 호출
