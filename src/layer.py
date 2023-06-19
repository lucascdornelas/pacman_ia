import pygame

class Menu():
    def __init__(self) -> None:
        self.option = ["JOGAR", "SAIR"]
        self.index = 0
        self.font_title = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.font_option = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.title = "PAC-MAN"
        self.choice = -1
        self.space = 40
        self.comand = False

    def update(self):
        # tem de soltar a tecla para dar o proximo comando
        comand = pygame.key.get_pressed()
        if self.comand != comand:
            if comand[pygame.K_UP]:
                if self.index > 0:
                    self.index -= 1
            elif comand[pygame.K_DOWN]:
                if self.index < len(self.option) - 1:
                    self.index += 1
            elif comand[pygame.K_RETURN]:
                self.choice = self.index
        self.comand = comand
        return self.choice

            

    def render(self, g, position):
        g.fill((0,0,0))
        g.blit(self.font_title.render(self.title, True, (255,255, 0)), position)
        for i, option in enumerate(self.option):
            _color = (255,255, 255)
            if i == self.index:
                _color = (255,255, 0)
            g.blit(self.font_option.render(self.option[i], True, _color), (position[0], position[1] + 100 + (i * self.space)))

class Pause():
    def __init__(self) -> None:
        self.option = ["CONTINUAR", "REINICIAR", "MENU"]
        self.index = 0
        self.font_title = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.font_option = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.title = "PAUSE"
        self.choice = -1
        self.space = 40
        self.comand = False

    def update(self):
        # tem de soltar a tecla para dar o proximo comando
        comand = pygame.key.get_pressed()
        if self.comand != comand:
            if comand[pygame.K_UP]:
                if self.index > 0:
                    self.index -= 1
            elif comand[pygame.K_DOWN]:
                if self.index < len(self.option) - 1:
                    self.index += 1
            elif comand[pygame.K_RETURN]:
                self.choice = self.index
        self.comand = comand
        return self.choice

    def render(self, g, position):
        g.blit(self.font_title.render(self.title, True, (255,255, 0)), position)
        for i, option in enumerate(self.option):
            _color = (255,255, 255)
            if i == self.index:
                _color = (255,255, 0)
            g.blit(self.font_option.render(self.option[i], True, _color), (position[0], position[1] + 100 + (i * self.space)))

class GameOver():
    def __init__(self) -> None:
        self.font_title = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.font_option = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.title = "GAME OVER"

    def update(self):
        comand = pygame.key.get_pressed()
        if comand[pygame.K_RETURN]:
            return 1
        elif comand[pygame.K_r]:
            return 2
        return 0

    def render(self, g, position, points):
        g.blit(self.font_title.render(self.title, True, (255,0, 0)), position)
        g.blit(self.font_option.render("Pontos: "+  str(points), True, (255,255, 0)), (position[0]+ 50, position[1] + 100))
        g.blit(self.font_option.render("[ENTER] ->   MENU", True, (255,255, 255)), (position[0], position[1] + 150 ))
        g.blit(self.font_option.render("   [R]   ->  RESTART", True, (255,255, 255)), (position[0], position[1] + 180))

class Victory():
    def __init__(self) -> None:
        self.font_title = pygame.font.Font(pygame.font.get_default_font(), 42)
        self.font_option = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.title = "VITÓRIA"

    def update(self):
        comand = pygame.key.get_pressed()
        if comand[pygame.K_RETURN]:
            return 1
        return 0

    def render(self, g, position, points):
        g.blit(self.font_title.render(self.title, True, (0,255, 0)), position)
        g.blit(self.font_option.render("Pontos: "+  str(points), True, (255,255, 0)), (position[0] + 50, position[1] + 100))
        g.blit(self.font_option.render("[ENTER] -> MENU", True, (255,255, 255)), (position[0], position[1] + 150))