import pygame
import game_configs as configs

# 1. Initialize Pygame
pygame.init()

# 2. Setup constants and window
WIDTH, HEIGHT = configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = SCREEN.get_rect()
pygame.display.set_caption(configs.TITLE_CAPTION)

# 3. Setup clock for frame rate control
clock = pygame.time.Clock()
FPS = 60

winning_lists = [
    [0,1,2],
    [0,3,6],
    [0,4,8],
    [1,4,7],
    [3,4,6],
    [6,7,8],
    [2,5,8],
    [2,4,6],
    [3,4,5],
]

font = pygame.font.SysFont(None, configs.CHAR_SIZE)
info_font = pygame.font.SysFont(None, configs.INFO_TEXT_SIZE)

rects: list[pygame.rect.Rect] = []

info_surface = pygame.surface.Surface((WIDTH, HEIGHT * .2), 0, SCREEN)
info_surface_rect = info_surface.get_rect(topleft=(0,0))

game_surface = pygame.surface.Surface((WIDTH, HEIGHT * .8), 0, SCREEN)
game_surface_rect = game_surface.get_rect(topleft=(0, info_surface.get_height()))

platform = game_surface
pl_width = platform.get_width()
pl_height = platform.get_height()

BOX_WIDTH = (pl_width) // 3
BOX_HEIGHT = (pl_height) // 3

def check_game_won(board: list):
    global winning_lists

    for wl in winning_lists:
        char = board[wl[0]]
        if char == "0":
            continue
        won = True
        for ind in wl[1:]:
            won = won and char == board[ind]
            char = board[ind]
        if won:
            return True, char, wl
    return False, "", []


def main():
    # board = "XXXOXOXOO"
    board = "0"*9
    # board = "123456789"
    board = list(board)

    assert len(board) == 9, "Invalid board"
    
    turn = "X"
    running = True
    won = False
    char = "0"
    won_indexs = []
    while running:
        # 4. Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for ind, rect in enumerate(rects):
                    rect.y += game_surface_rect.y
                    if rect.collidepoint(mouse_pos) and board[ind] == "0" and not won:
                        board[ind] = turn
                        turn = "X" if turn == "O" else "O"
                        won, char, won_indexs = check_game_won(board)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and won:
                board = list("0"*9)
                won = False

        # 6. Drawing / Rendering
        SCREEN.fill(configs.BLACK)  # Clear screen with black
        SCREEN.blit(info_surface, (0, 0))
        SCREEN.blit(game_surface, game_surface_rect)
        info_surface.fill(configs.OFFWHITE)

        turn_text = info_font.render(f"Turn: {turn}", 1, configs.BLACK)
        turn_text_rect = turn_text.get_rect(center=info_surface_rect.center)

        info_surface.blit(turn_text, turn_text_rect)
        game_surface.fill(configs.GRAY)

        if won:
            st_ind = won_indexs[0]
            end_ind = won_indexs[2]
            st_rect, end_rect = rects[st_ind], rects[end_ind]
            pygame.draw.line(game_surface, configs.GREEN, st_rect.center, end_rect.center, 5)


        rects.clear()
        char_ind = 0
        for i in range(3):
            x = (i * BOX_WIDTH)
            for j in range(3):
                y = (j * BOX_HEIGHT)
                rect_value = (x, y, BOX_WIDTH, BOX_HEIGHT)
                rect = pygame.draw.rect(platform, configs.OFFWHITE, rect_value, 1)
                rects.append(rect)
                char = board[char_ind]
                if char == "0":
                    char_ind += 1
                    continue

                text_surf = font.render(char, True, configs.BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                game_surface.blit(text_surf, text_rect)
                char_ind += 1

        pygame.display.flip()  # Update the full display Surface to the screen

        # 7. Control the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
