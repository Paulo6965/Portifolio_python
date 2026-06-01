import pygame

pygame.init()

# Configurações da janela
WIDTH = 400
HEIGHT = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste de Merge 2048")

font = pygame.font.Font(None, 50)

# Linha de teste
row = [2, 2, 4, 0]


def merge(row):
    # Remove zeros
    row = [num for num in row if num != 0]

    result = []
    skip = False

    for i in range(len(row)):
        if skip:
            skip = False
            continue

        if i + 1 < len(row) and row[i] == row[i + 1]:
            result.append(row[i] * 2)
            skip = True
        else:
            result.append(row[i])

    while len(result) < 4:
        result.append(0)

    return result


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                row = merge(row)
                print(row)

    screen.fill((240, 240, 240))

    # Desenha os blocos
    for i, value in enumerate(row):

        rect = pygame.Rect(i * 90 + 20, 30, 80, 80)

        pygame.draw.rect(screen, (180, 180, 180), rect)

        if value != 0:
            text = font.render(str(value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()