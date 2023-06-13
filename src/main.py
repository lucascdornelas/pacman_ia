import pygame

# Cores
from colors import BLACK, WHITE, RED, BLUE

# Mapa
from map import MAP, CELL_SIZE, MAP_WIDTH, MAP_HEIGHT

# Defina as constantes do jogo
WIDTH = MAP_WIDTH * CELL_SIZE
HEIGHT = MAP_HEIGHT * CELL_SIZE
FPS = 60
ENEMY_SPEED = 5

# Classe para representar o personagens
from character import Character

from enemy import Enemy


# Classe principal do jogo
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.enemies = []

    def run(self):
        counter = 0
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update(counter)
            self.draw()

            counter += 1

    def controllerPlayer(self, event):
        if event.key == pygame.K_LEFT:
            new_x = self.player.rect.x - CELL_SIZE
            if (
                self.player.rect.x > 0
                and MAP[self.player.rect.y // CELL_SIZE][new_x // CELL_SIZE] != 1
            ):
                self.player.rect.x = new_x
            elif self.player.rect.x == 0:
                self.player.rect.x = WIDTH - CELL_SIZE
        elif event.key == pygame.K_RIGHT:
            new_x = self.player.rect.x + CELL_SIZE
            if (
                self.player.rect.x < WIDTH - CELL_SIZE
                and MAP[self.player.rect.y // CELL_SIZE][new_x // CELL_SIZE] != 1
            ):
                self.player.rect.x = new_x
            elif self.player.rect.x == WIDTH - CELL_SIZE:
                self.player.rect.x = 0
        elif event.key == pygame.K_UP:
            new_y = self.player.rect.y - CELL_SIZE
            if (
                self.player.rect.y > 0
                and MAP[new_y // CELL_SIZE][self.player.rect.x // CELL_SIZE] != 1
            ):
                self.player.rect.y = new_y
        elif event.key == pygame.K_DOWN:
            new_y = self.player.rect.y + CELL_SIZE
            if (
                self.player.rect.y < HEIGHT - CELL_SIZE
                and MAP[new_y // CELL_SIZE][self.player.rect.x // CELL_SIZE] != 1
            ):
                self.player.rect.y = new_y

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.controllerPlayer(event)

    def update(self, counter):
        counter = counter % 30

        if counter == 0:
            for enemy in self.enemies:
                enemy.update()
        
        self.player.update()


    def draw(self):
        self.screen.fill(BLACK)
        # Desenhe o mapa
        for row in range(len(MAP)):
            for col in range(len(MAP[row])):
                cell_type = MAP[row][col]
                color = BLUE if cell_type == 1 else BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def start(self):
        for row in range(len(MAP)):
            for col in range(len(MAP[row])):
                cell_type = MAP[row][col]
                if cell_type == 2:
                    self.player = Character(col, row, RED)
                    self.all_sprites.add(self.player)
                elif cell_type == 3:
                    enemy = Enemy(col, row, WHITE, self.player)
                    self.enemies.append(enemy)
                    self.all_sprites.add(enemy)
        # o inimigo é lido antes do player
        for _enemy in self.enemies:
            enemy.player = self.player
        self.run()


# Função principal para iniciar o jogo
if __name__ == "__main__":
    game = Game()
    game.start()
    pygame.quit()
