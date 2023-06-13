import pygame

from map import CELL_SIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        self.color = color
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE

    def render(self, g):
        pygame.draw.rect(g, self.color, [self.x, self.y, CELL_SIZE, CELL_SIZE])
