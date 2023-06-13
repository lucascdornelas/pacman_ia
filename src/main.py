import pygame

# Cores
from colors import *

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

from food import Food

from wall import Wall


# Classe principal do jogo
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.player = None
        self.enemies = []
        self.foods = []
        self.walls = []

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

    def collision(self):
        # colisão com comidas
        for comida in self.foods:
            rect_player = pygame.Rect(self.player.rect.x, self.player.rect.y, CELL_SIZE, CELL_SIZE)
            rect_comida = pygame.Rect(comida.x, comida.y, comida.size, comida.size)
            if rect_player.colliderect(rect_comida):
                self.player.points += 1
                self.foods.remove(comida)


        # colisão com os inimigos
        for inimigos in self.enemies:
            rect_player = pygame.Rect(self.player.rect.x, self.player.rect.y, CELL_SIZE, CELL_SIZE)
            rect_inimigos = pygame.Rect(inimigos.rect.x, inimigos.rect.y, CELL_SIZE, CELL_SIZE)
            if rect_player.colliderect(rect_inimigos):
                self.running = False


    def update(self, counter):
        counter = counter % 30

        if counter == 0:
            for enemy in self.enemies:
                enemy.update()
        
        self.player.update()
        self.collision()


    def draw(self):
        self.screen.fill(BLACK)
        # Desenhe o mapa
        # renderiza todas as entidades do jogo
        for parede in self.walls:
            parede.render(self.screen)
        # renderiza todas os inimigos do jogo
        for comida in self.foods:
            comida.render(self.screen)
        # renderiza todas os inimigos do jogo
        for inimigos in self.enemies:
            inimigos.render(self.screen)
        # renderiza o player
        self.player.render(self.screen)
        # renderiza UI
        self.screen.blit(self.font.render("Pontos: " + str(self.player.points), True, GREEN), (10,10))
        pygame.display.flip()

    def start(self):
        for row in range(len(MAP)):
            for col in range(len(MAP[row])):
                cell_type = MAP[row][col]
                if cell_type == 2:
                    self.player = Character(col, row, YELLOW)
                elif cell_type == 3:
                    enemy = Enemy(col, row, RED, self.player)
                    self.enemies.append(enemy)
                elif cell_type == 1:
                    wall = Wall(col, row, BLUE)
                    self.walls.append(wall)
                elif cell_type == 4:
                    _food = Food(col, row, int(CELL_SIZE/8), WHITE)
                    self.foods.append(_food)
        # o inimigo é lido antes do player
        for _enemy in self.enemies:
            _enemy.player = self.player
        self.run()


# Função principal para iniciar o jogo
if __name__ == "__main__":
    game = Game()
    game.start()
    pygame.quit()
