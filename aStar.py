import pygame
import math

WIDTH = 900
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A * Path Finding Alg")

RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
unknown = (0, 200, 126)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.neighbors = []
        self.f = 100
        self.g = 100
        self.h = 0
        self.previous = None
        self.total_rows = total_rows

    def ChangeColors(self, color):
        self.color = color

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def find_neighbor(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        #if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():
            #self.neighbors.append(grid[self.row + 1][self.col + 1])
       # if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
            #self.neighbors.append(grid[self.row - 1][self.col + 1])
        #if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier():
            #self.neighbors.append(grid[self.row + 1][self.col - 1])
        #if self.row > 0 and self.col > 0 and  not grid[self.row -1][self.col - 1].is_barrier():
           # self.neighbors.append(grid[self.row - 1][self.col - 1])

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


def heuristic(node, end):
    dist = abs(node.row - end.row) + abs(node.col - end.col)
    return dist


def reconstruct(node, draw):
    node.color = BLUE
    node = node.previous
    while node.previous:
        node.color = unknown
        node = node.previous
        draw()


def algorithm(draw, grid, start, end):
    openSet = [start]
    start.g = 0
    start.f = heuristic(start, end)

    while len(openSet) > 0:
    
    	
        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i

        current = openSet[winner]
        if current == end:
            reconstruct(current, draw)
            return True

        del openSet[winner]

        for neighbour in current.neighbors:
            tempg = current.g + 1
            if tempg < neighbour.g:
                neighbour.g = tempg
                neighbour.previous = current
                neighbour.f = neighbour.g + heuristic(neighbour, end)

                if neighbour not in openSet:
                    openSet.append(neighbour)
                    neighbour.color = GREEN

        draw()
        if current != start:
            current.color = RED


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.ChangeColors(BLUE)
                elif not end and spot != start:
                    end = spot
                    end.ChangeColors(RED)
                elif spot != start and spot != end:
                    spot.ChangeColors(BLACK)


            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.color = WHITE
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.find_neighbor(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

    pygame.quit()


main(win, WIDTH)
