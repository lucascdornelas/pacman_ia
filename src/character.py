import pygame

from map import CELL_SIZE
from spritesheet import SpriteSheet

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
        self.spritesheet = SpriteSheet(pygame.image.load("imagens/sprite_pacman.png"), 13, 13, CELL_SIZE / 13)
        self.count = 0
        self.count_max = 10
        self.frame = 0
        self.direcao = 0

    def update(self):
        self.count += 1
        if self.count >= self.count_max:
            self.count = 0
            if self.frame % 2 == 0:
                self.frame += 1
            else:
                self.frame -= 1

    def render(self, g):
        #pygame.draw.rect(g, self.color, [self.rect.x, self.rect.y, CELL_SIZE, CELL_SIZE])
        _imagem = self.spritesheet.get_image(self.frame+(self.direcao*2))
        g.blit(_imagem, (self.rect.x, self.rect.y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
