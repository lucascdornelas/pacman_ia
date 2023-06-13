import pygame

from map import CELL_SIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        self.color = color
        self.x = (x * CELL_SIZE) + (CELL_SIZE/2) - (size/2)
        self.y = (y * CELL_SIZE) + (CELL_SIZE/2) - (size/2)
        self.size = size

    def render(self, g):
        pygame.draw.rect(g, self.color, [self.x, self.y, self.size, self.size])
