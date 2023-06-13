import pygame

from map import CELL_SIZE

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE
        self.color = color
        self.points = 0

    def update(self):
        pass

    def render(self, g):
        pygame.draw.rect(g, self.color, [self.rect.x, self.rect.y, CELL_SIZE, CELL_SIZE])

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy