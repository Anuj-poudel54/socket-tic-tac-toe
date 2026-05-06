import pygame
import game_configs as configs
from client_socket import ClientSocket


class TicTacToe:

    def __init__(self, my_char:str | None = None, socket: ClientSocket | None = None) -> None:
        pygame.init()

        self.my_char = my_char
        self.other_char = "O" if my_char == "X" else "X"
        if not my_char:
            self.other_char = None
        self.socket = socket

        self.init_board()
        self._running = True
        self.turn = "X"
        self.won = False
        self.won_char = ""
        self.won_indexs = []

        # 2. Setup constants and window
        self.WIDTH, self.HEIGHT = configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen_rect = self.SCREEN.get_rect()
        pygame.display.set_caption(configs.TITLE_CAPTION)

        # 3. Setup clock for frame rate control
        self.clock = pygame.time.Clock()
        self.FPS = configs.FPS

        self.winning_lists = [
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

        self.font = pygame.font.SysFont(None, configs.CHAR_SIZE)
        self.info_font = pygame.font.SysFont(None, configs.INFO_TEXT_SIZE)

        self.rects: list[pygame.rect.Rect] = []

        self.info_surface = pygame.surface.Surface((self.WIDTH, self.HEIGHT * .2), 0, self.SCREEN)
        self.info_surface_rect = self.info_surface.get_rect(topleft=(0,0))

        self.game_surface = pygame.surface.Surface((self.WIDTH, self.HEIGHT * .8), 0, self.SCREEN)
        self.game_surface_rect = self.game_surface.get_rect(topleft=(0, self.info_surface.get_height()))

        self.platform = self.game_surface
        self.pl_width = self.platform.get_width()
        self.pl_height = self.platform.get_height()

        self.BOX_WIDTH = (self.pl_width) // 3
        self.BOX_HEIGHT = (self.pl_height) // 3

    def start_game_loop(self):
        while self._running:
            self.update()

        pygame.quit()

    def set_char(self, ind, char):
        self.board[ind] = char

    def _toggle_turn(self):
        if self.my_char:
            self.turn = self.my_char if self.turn == self.other_char else self.other_char
        else:
            self.turn = "X" if self.turn == "O" else "O"

    def _render_board(self):
        char_ind = 0
        for i in range(3):
            x = (i * self.BOX_WIDTH)
            for j in range(3):
                y = (j * self.BOX_HEIGHT)
                rect_value = (x, y, self.BOX_WIDTH, self.BOX_HEIGHT)
                rect = pygame.draw.rect(self.platform, configs.OFFWHITE, rect_value, 1)
                self.rects.append(rect)
                char = self.board[char_ind]
                if char == "0":
                    char_ind += 1
                    continue

                text_surf, text_rect = self.create_text(char, configs.BLACK, None, center=rect.center)
                self.game_surface.blit(text_surf, text_rect)
                char_ind += 1

    def _get_socket_msg(self):
        if self.socket is None:
            return None

        return self.socket.msg

    def update(self):
        self.handle_events()
        msg = self._get_socket_msg()
        if msg is not None:
            ind = int(msg)
            if self.board[ind] == "0":
                self.board[ind] = self.other_char
                self._toggle_turn()

            self.check_game_won()

        # 6. Drawing / Rendering
        self.SCREEN.fill(configs.BLACK)  # Clear screen with black
        self.SCREEN.blit(self.info_surface, (0, 0))
        self.SCREEN.blit(self.game_surface, self.game_surface_rect)
        self.info_surface.fill(configs.OFFWHITE)

        turn_text, turn_text_rect = self.create_text(f"Turn: {self.turn}", configs.BLACK, None, center=self.info_surface_rect.center)
        self.info_surface.blit(turn_text, turn_text_rect)
        self.game_surface.fill(configs.GRAY)

        if self.won:
            st_ind = self.won_indexs[0]
            end_ind = self.won_indexs[2]
            st_rect, end_rect = self.rects[st_ind], self.rects[end_ind]
            pygame.draw.line(self.game_surface, configs.GREEN, st_rect.center, end_rect.center, 5)

        self.rects.clear()
        self._render_board()

        pygame.display.flip()  # Update the full display Surface to the screen

        # 7. Control the frame rate
        self.clock.tick(self.FPS)

    def _my_turn(self):
        return not self.my_char or self.my_char == self.turn

    def _can_draw_char_in(self, ind: int):
        return self.board[ind] == "0" and not self.won and self._my_turn()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for ind, rect in enumerate(self.rects):
                    rect.y += self.game_surface_rect.y
                    if rect.collidepoint(mouse_pos) and self._can_draw_char_in(ind):
                        self.board[ind] = self.turn
                        self._toggle_turn()

                        if self.socket:
                            self.socket.update_board_at(ind)
                        self.check_game_won()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.won:
                self.init_board()
                self.won = False


    def init_board(self):
        self.board = list("0"*9)

    def check_game_won(self):
        for wl in self.winning_lists:
            char = self.board[wl[0]]
            if char == "0":
                continue
            won = True
            for ind in wl[1:]:
                won = won and char == self.board[ind]
                char = self.board[ind]
            if won:
                self.won = True
                self.won_char = char
                self.won_indexs = wl
                return

        self.won = False
        self.won_char = ""
        self.won_indexs = []

    def create_text(self, text: str, color, font: pygame.font.Font| None = None, **rect_kwargs):
        if font is None:
            font = pygame.font.SysFont(None, configs.CHAR_SIZE)

        turn_text = self.info_font.render(text, 1, color)
        turn_text_rect = turn_text.get_rect(**rect_kwargs)

        return turn_text, turn_text_rect

if __name__ == "__main__":
    try:
        print("Connecting to server...")
        cs = ClientSocket()
        my_char = cs._socket_msg
        print("Connected to server, waiting for other player...")
        ttt = TicTacToe(my_char=my_char, socket=cs)
        ttt.start_game_loop()
        cs.close()
    except Exception as e:
        ttt = TicTacToe()
        print("Could not connect to server. Play offline :( !")
        ttt.start_game_loop()

