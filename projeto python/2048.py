import pygame
import random


pygame.init()


WIDTH = 400
HEIGHT = 500  
GRID_SIZE = 4
CELL_SIZE = 80
GAP = 10
BOARD_SIZE = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GAP
OFFSET_Y = 100 

COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
}
DEFAULT_TEXT_COLOR = (249, 246, 242)
BG_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (204, 192, 179)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) 
                       for r in range(GRID_SIZE) 
                       for c in range(GRID_SIZE) 
                       if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def merge(self, row):
        non_zero = [num for num in row if num != 0]
        result = []
        skip = False
        row_score = 0

        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue

            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_val = non_zero[i] * 2
                result.append(merged_val)
                row_score += merged_val
                skip = True
            else:
                result.append(non_zero[i])

        while len(result) < GRID_SIZE:
            result.append(0)
        
        return result, row_score

    def move(self, direction):
        if self.game_over:
            return False

        old_grid = [row[:] for row in self.grid]
        moved = False
        turn_score = 0

        if direction == "LEFT":
            for i in range(GRID_SIZE):
                new_row, s = self.merge(self.grid[i])
                self.grid[i] = new_row
                turn_score += s
        
        elif direction == "RIGHT":
            for i in range(GRID_SIZE):
                reversed_row = self.grid[i][::-1]
                new_row, s = self.merge(reversed_row)
                self.grid[i] = new_row[::-1]
                turn_score += s

        elif direction == "UP":
            for c in range(GRID_SIZE):
                col = [self.grid[r][c] for r in range(GRID_SIZE)]
                new_col, s = self.merge(col)
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_col[r]
                turn_score += s

        elif direction == "DOWN":
            for c in range(GRID_SIZE):
                col = [self.grid[r][c] for r in range(GRID_SIZE)][::-1]
                new_col, s = self.merge(col)
                new_col = new_col[::-1]
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_col[r]
                turn_score += s

        if self.grid != old_grid:
            self.score += turn_score
            self.add_new_tile()
            self.check_game_over()
            return True
        return False

    def check_game_over(self):
        # Verifica se há o bloco 2048
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 2048:
                    self.won = True

        # Verifica se ainda há espaços vazios
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return

        # Verifica se há movimentos possíveis (adjacentes iguais)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                if (r + 1 < GRID_SIZE and self.grid[r+1][c] == val) or \
                   (c + 1 < GRID_SIZE and self.grid[r][c+1] == val):
                    return
        
        self.game_over = True

def draw_game(game):
    screen.fill((250, 248, 239))
    
    # Desenhar Placar
    score_text = font_medium.render(f"Score: {game.score}", True, (119, 110, 101))
    screen.blit(score_text, (20, 30))
    
    title_text = font_large.render("2048", True, (119, 110, 101))
    screen.blit(title_text, (WIDTH - 120, 20))

    # Desenhar Fundo do Tabuleiro
    board_rect = pygame.Rect(
        (WIDTH - BOARD_SIZE) // 2, 
        OFFSET_Y, 
        BOARD_SIZE, 
        BOARD_SIZE
    )
    pygame.draw.rect(screen, BG_COLOR, board_rect, border_radius=5)

    # Desenhar Blocos
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = game.grid[r][c]
            color = COLORS.get(value, (60, 58, 50))
            
            x = board_rect.x + GAP + c * (CELL_SIZE + GAP)
            y = board_rect.y + GAP + r * (CELL_SIZE + GAP)
            
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect, border_radius=3)

            if value != 0:
                text_color = TEXT_COLORS.get(value, DEFAULT_TEXT_COLOR)
                # Ajustar tamanho da fonte para números grandes
                current_font = font_medium if value < 100 else font_small
                text = current_font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))
        screen.blit(overlay, (0, 0))
        msg = "GAME OVER!"
        text = font_large.render(msg, True, (119, 110, 101))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        
        retry_text = font_small.render("Pressione R para reiniciar", True, (119, 110, 101))
        retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(retry_text, retry_rect)

    pygame.display.flip()

def main():
    game = Game2048()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.game_over and event.key == pygame.K_r:
                    game = Game2048()
                elif not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        game.move("RIGHT")
                    elif event.key == pygame.K_UP:
                        game.move("UP")
                    elif event.key == pygame.K_DOWN:
                        game.move("DOWN")

        draw_game(game)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
