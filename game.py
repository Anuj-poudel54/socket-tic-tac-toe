import pygame
import game_configs as configs

# 1. Initialize Pygame
pygame.init()

# 2. Setup constants and window
WIDTH, HEIGHT = configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(configs.TITLE_CAPTION)

# 3. Setup clock for frame rate control
clock = pygame.time.Clock()
FPS = 60


# board = "XXXOXOXOO"
board = "123456789"

assert len(board) == 9, "Invalid board"


font = pygame.font.SysFont(None, configs.CHAR_SIZE)

rects: list[pygame.rect.Rect] = []
game_surface = pygame.surface.Surface((WIDTH, HEIGHT), 0, SCREEN)

platform = game_surface
pl_width = platform.get_width()
pl_height = platform.get_height()

BOX_WIDTH = (pl_width) // 3
BOX_HEIGHT = (pl_height) // 3

def main():
    running = True
    while running:
        # 4. Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 6. Drawing / Rendering
        SCREEN.fill(configs.WHITE)  # Clear screen with black
        SCREEN.blit(game_surface, (0 , 0))
        game_surface.fill(configs.GRAY)

        for i in range(3):
            x = (i * BOX_WIDTH)
            for j in range(3):
                y = (j * BOX_HEIGHT)
                rect_value = (x, y, BOX_WIDTH, BOX_HEIGHT)
                rect = pygame.draw.rect(platform, configs.OFFWHITE, rect_value, 1)
                rects.append(rect)
                char = board[j + i] # TODO: not correct way of getting value
                if char == "0":
                    continue

                text_surf = font.render(char, True, configs.BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                game_surface.blit(text_surf, text_rect)

        pygame.display.flip()  # Update the full display Surface to the screen

        # 7. Control the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
