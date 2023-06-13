import pygame
from heapq import *

from map import MAP, CELL_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.player = player
        self.color = color

    def update(self):
        # Utiliza a estratégia de busca A* para perseguir o jogador
        path = self.find_path_to_player()
        #print(path)
        if path:
            next_cell = path[0]
            next_x = next_cell[0] * CELL_SIZE
            next_y = next_cell[1] * CELL_SIZE
            self.rect.x = next_x
            self.rect.y = next_y

    def render(self, g):
        pygame.draw.rect(g, self.color, [self.rect.x, self.rect.y, CELL_SIZE, CELL_SIZE])

    def find_path_to_player(self):
        start = (self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE)
        end = (self.player.rect.x // CELL_SIZE, self.player.rect.y // CELL_SIZE)
        # Implemente o algoritmo A* para encontrar o caminho até o jogador
        # Aqui está uma implementação básica para ajudar você a começar:
        open_list = []
        closed_set = set()
        heappush(open_list, (0, start, []))
        while open_list:
            current_cost, current_node, current_path = heappop(open_list)
            if current_node == end:
                return current_path
            if current_node in closed_set:
                continue
            closed_set.add(current_node)
            for neighbor in self.get_neighbors(current_node):
                neighbor_cost = current_cost + 1  # Assume um custo constante de 1 para cada movimento
                neighbor_path = current_path + [neighbor]
                heappush(open_list, (neighbor_cost + self.heuristic(neighbor, end), neighbor, neighbor_path))
        return None

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0 and MAP[y][x - 1] != 1:
            neighbors.append((x - 1, y))
        if x < len(MAP[0]) - 1 and MAP[y][x + 1] != 1:
            neighbors.append((x + 1, y))
        if y > 0 and MAP[y - 1][x] != 1:
            neighbors.append((x, y - 1))
        if y < len(MAP) - 1 and MAP[y + 1][x] != 1:
            neighbors.append((x, y + 1))
        return neighbors

    def heuristic(self, node, goal):
        x1, y1 = node
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)