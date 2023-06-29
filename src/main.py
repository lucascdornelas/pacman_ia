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
#estados
ESTADO_MENU = "menu"
ESTADO_PAUSE = "pause"
ESTADO_GAME = "game"
ESTADO_GAMEOVER = "gameover"
ESTADO_VICTORY = "victory"


# Classe para representar o personagens
from character import Character

from enemy import Enemy

from food import Food

from wall import Wall

from layer import *


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
        self.estado = ESTADO_MENU
        self.menu = Menu()
        self.pause = Pause()
        self.victory = Victory()
        self.gameover = GameOver()

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
            self.player.direcao = 1
            new_x = self.player.rect.x - CELL_SIZE
            if (
                self.player.rect.x > 0
                and MAP[self.player.rect.y // CELL_SIZE][new_x // CELL_SIZE] != 1
            ):
                self.player.rect.x = new_x
            elif self.player.rect.x == 0:
                self.player.rect.x = WIDTH - CELL_SIZE
        elif event.key == pygame.K_RIGHT:
            self.player.direcao = 0
            new_x = self.player.rect.x + CELL_SIZE
            if (
                self.player.rect.x < WIDTH - CELL_SIZE
                and MAP[self.player.rect.y // CELL_SIZE][new_x // CELL_SIZE] != 1
            ):
                self.player.rect.x = new_x
            elif self.player.rect.x == WIDTH - CELL_SIZE:
                self.player.rect.x = 0
        elif event.key == pygame.K_UP:
            self.player.direcao = 2
            new_y = self.player.rect.y - CELL_SIZE
            if (
                self.player.rect.y > 0
                and MAP[new_y // CELL_SIZE][self.player.rect.x // CELL_SIZE] != 1
            ):
                self.player.rect.y = new_y
        elif event.key == pygame.K_DOWN:
            self.player.direcao = 3
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
                if self.estado == ESTADO_GAME:
                    self.controllerPlayer(event)
                    if event.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_PAUSE
                elif self.estado == ESTADO_PAUSE:
                    if event.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_GAME

    def collision(self):
        # checa se as comidas acabaram
        if len(self.foods) == 0:
            self.estado = ESTADO_VICTORY

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
                self.estado = ESTADO_GAMEOVER


    def update(self, counter):
        if self.estado == ESTADO_GAME:
            counter = counter % 30

            if counter == 0:
                for enemy in self.enemies:
                    enemy.update()
            
            self.player.update()
            self.collision()
        elif self.estado == ESTADO_MENU:
            _option = self.menu.update()
            if _option == 0:
                game.restart()
            elif _option == 1:
                self.running = False
        elif self.estado == ESTADO_PAUSE:
            _option = self.pause.update()
            if _option == 0:
                self.pause.choice = -1
                self.estado = ESTADO_GAME
            elif _option == 1:
                game.restart()
            elif _option == 2:
                self.estado = ESTADO_MENU
        elif self.estado == ESTADO_VICTORY:
            _option = self.victory.update()
            if _option == 1:
                self.estado = ESTADO_MENU
        elif self.estado == ESTADO_GAMEOVER:
            _option = self.gameover.update()
            if _option == 1:
                self.estado = ESTADO_MENU
            elif _option == 2:
                game.restart()


    def draw(self):
        if self.estado == ESTADO_GAME:
            self.screen.fill(BLACK)

            for parede in self.walls:
                parede.render(self.screen)
            for comida in self.foods:
                comida.render(self.screen)

            for inimigos in self.enemies:
                inimigos.render(self.screen)

            self.player.render(self.screen)

            self.screen.blit(self.font.render("Pontos: " + str(self.player.points), True, GREEN), (10,10))

        elif self.estado == ESTADO_MENU:
            self.menu.render(self.screen, ((WIDTH/2)-100, (HEIGHT/2) - 100))
        elif self.estado == ESTADO_PAUSE:
            self.pause.render(self.screen, ((WIDTH/2)-75, (HEIGHT/2) - 100))
        elif self.estado == ESTADO_VICTORY:
            self.victory.render(self.screen, ((WIDTH/2)-100, (HEIGHT/2) - 100), self.player.points)
        elif self.estado == ESTADO_GAMEOVER:
            self.gameover.render(self.screen, ((WIDTH/2)-100, (HEIGHT/2) - 100), self.player.points)

        pygame.display.flip()

    def restart(self):
        self.menu.choice = -1
        self.pause.choice = -1
        self.enemies = []
        self.foods = []
        self.walls = []
        self.player = None
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
        self.estado = ESTADO_GAME

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
