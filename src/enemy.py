import pygame
from heapq import *
from map import MAP, CELL_SIZE
from spritesheet import SpriteSheet

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
        self.spritesheet = SpriteSheet(pygame.image.load("imagens/sprites_fantasma.png"), 16, 16, CELL_SIZE / 16)
        self.count = 0
        self.count_max = 1
        self.frame = 0
        self.scale = (CELL_SIZE / 16)
        self.eye_size = (CELL_SIZE / 16) * 2
        self.eye_center_pos_x = [self.scale * 4, self.scale * 10]
        self.eye_center_pos_y = self.scale * 7
        self.eye_pos_x = [0, 0]
        self.eye_pos_y = 0
        self.eye_range = 3

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

        # atualiza sprite
        self.count += 1
        if self.count >= self.count_max:
            self.count = 0
            if self.frame % 2 == 0:
                self.frame += 1
            else:
                self.frame -= 1
            self.change_eye_position()

    def render(self, g):
        #pygame.draw.rect(g, self.color, [self.rect.x, self.rect.y, CELL_SIZE, CELL_SIZE])
        _imagem = self.spritesheet.get_image(self.frame)
        g.blit(_imagem, (self.rect.x, self.rect.y))
        # desenha a posição do olho
        eye_x_0 = self.rect.x + self.eye_pos_x[0] + self.eye_center_pos_x[0]
        eye_x_1 = self.rect.x + self.eye_pos_x[1] + self.eye_center_pos_x[1]
        eye_y = self.rect.y + self.eye_pos_y + self.eye_center_pos_y
        pygame.draw.rect(g, (0,0,255), [eye_x_0, eye_y, self.eye_size, self.eye_size])
        pygame.draw.rect(g, (0,0,255), [eye_x_1, eye_y, self.eye_size, self.eye_size])

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
    
    def change_eye_position(self):
        _x =  self.player.rect.x - self.rect.x
        _y =  self.player.rect.y - self.rect.y
        # posição x dos olhos 
        if _x < 0:
            self.eye_pos_x[0] = -self.eye_range
            self.eye_pos_x[1] = -self.eye_range
        elif _x > 0:
            self.eye_pos_x[0] = self.eye_range
            self.eye_pos_x[1] = self.eye_range
        else:
            self.eye_pos_x[0] = 0
            self.eye_pos_x[1] = 0
        
        # posição y dos olhos
        if _y < 0:
            self.eye_pos_y = -self.eye_range
        elif _y > 0:
            self.eye_pos_y = self.eye_range
        else:
            self.eye_pos_y = 0
