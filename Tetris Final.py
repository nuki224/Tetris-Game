import pygame
import random

# determines how many times the game updates
FPS = 25
#defines the size of each grid cell
GRID_SIZE = 21
#defining width and height of the window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
FONT_SIZE = 25
# starting position of the grid
START_X = 150
START_Y = 50

class Tetris:
    # predefined colors used throughout the code
    COLORS = {
        "RED": (255, 51, 51),
        "YELLOW": (255, 255, 102),
        "BLUE": (51, 102, 255),
        "GREEN": (51, 204, 51),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "GRAY": (102, 102, 102),
    }

    RCOLORS = [COLORS["BLACK"], COLORS["RED"], COLORS["YELLOW"], COLORS["BLUE"], COLORS["GREEN"], COLORS["WHITE"], COLORS["GRAY"]]

    def __init__(self, height, width):
        self.score = 0
        #Sets the initial state of the game to "start" - the state of the game
        self.state = "start"
        #representing the game field
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width
        self.x = START_X
        self.y = START_Y
        self.zoom = GRID_SIZE
        self.figure = None
        self.start_time = pygame.time.get_ticks()

    def new_figure(self):
        self.figure = Figure(3, 0)
    #checks whether the current falling Tetris piece collides with the walls or existing blocks on the game grid
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def get_elapsed_time(self):
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        elapsed_time_sec = elapsed_time_ms // 1000
        hours = elapsed_time_sec // 3600
        minutes = (elapsed_time_sec % 3600) // 60
        seconds = elapsed_time_sec % 60
        return hours, minutes, seconds

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figures = [
            [[1, 5, 9, 13], [4, 5, 6, 7]],
            [[4, 5, 9, 10], [2, 6, 5, 9]],
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            [[1, 2, 5, 6]],
        ]
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(Tetris.RCOLORS) - 1)
        self.rotation = 0

    def image(self):
        current_figure = self.figures[self.type]
        return current_figure[self.rotation]

    def rotate(self):
        num_rotations = len(self.figures[self.type])
        self.rotation = (self.rotation + 1) % num_rotations

def draw_grid_and_blocks(screen, game):
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, Tetris.COLORS["GRAY"], [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, Tetris.RCOLORS[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 2])

def draw_current_figure(screen, game):
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, Tetris.RCOLORS[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

def draw_game_over_text(screen, game):
    if game.state == "gameover":
        text_game_over = pygame.font.Font(None, FONT_SIZE + 5).render("Game Over", True, Tetris.COLORS["RED"])
        text_game_over1 = pygame.font.Font(None, FONT_SIZE - 5).render("Press ESC", True, Tetris.COLORS["YELLOW"])
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

def draw_score_and_time(screen, game):
    text_score = pygame.font.Font(None, FONT_SIZE).render("Score: " + str(game.score), True, Tetris.COLORS["WHITE"])
    screen.blit(text_score, [10, 190])

    elapsed_hours, elapsed_minutes, elapsed_seconds = game.get_elapsed_time()
    time_str = "Time: {:02}:{:02}:{:02}".format(elapsed_hours, elapsed_minutes, elapsed_seconds)
    time_text = pygame.font.Font(None, FONT_SIZE).render(time_str, True, Tetris.COLORS["WHITE"])
    screen.blit(time_text, [10, 210])

def handle_key_event(key, game):
    key_actions = {
        pygame.K_UP: game.rotate,
        pygame.K_DOWN: game.go_down,
        pygame.K_LEFT: lambda: game.go_side(-1),
        pygame.K_RIGHT: lambda: game.go_side(1),
        pygame.K_SPACE: game.go_space,
        pygame.K_ESCAPE: lambda: game.__init__(20, 10),
    }
    if key in key_actions:
        key_actions[key]()

def initialize_game():
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris(20, 10)
    return screen, clock, game

def main():
    screen, clock, game = initialize_game()
    done = False
    counter = 0
    pressing_down = False

    while not done:
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (FPS // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                else:
                    handle_key_event(event.key, game)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill("black")

        draw_grid_and_blocks(screen, game)
        draw_current_figure(screen, game)
        draw_score_and_time(screen, game)
        draw_game_over_text(screen, game)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()