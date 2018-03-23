from pygame.locals import *
import math
import pygame
import random
import time

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

snake_block_size = 15

screen_dimensions = 400
while screen_dimensions % snake_block_size != 0:
    screen_dimensions += 1
screenx = screen_dimensions
screeny = screen_dimensions

#__________CLASSES__________#
class Game():
    def __init__(self):
        self.lastKey = "right"
        self.food = None
        self.score = 0
    def setLastKey(self,key):
        self.lastKey = key
    def getLastKey(self):
        return self.lastKey
    def spawnFood(self):
        validx = False
        while not validx:
            x = random.randint(0,(screenx-snake_block_size)%screenx)
            if x % snake_block_size == 0:
                validx = True
        validy = False
        while not validy:
            y = random.randint(0,(screeny-snake_block_size)%screeny)
            if y % snake_block_size == 0:
                validy = True
        self.food = [x,y]
    def showFood(self):
        return pygame.draw.rect(app.getScreen(),GREEN,(self.food[0],self.food[1],snake_block_size,snake_block_size))
    def getFood(self):
        return self.food
    def increaseScore(self):
        self.score += 1
        if self.score % 5 == 0:
            app.setTickSpeed(app.getTickSpeed()+2)
    def showScore(self):
        renderText(str(self.score),25,BLACK,25,25)
    def getScore(self):
        return self.score
    
class Player():
    def __init__(self,starting_length = 5):
        self.length = starting_length
        self.x = [snake_block_size for i in range(self.length)]
        self.y = [snake_block_size for i in range(self.length)]

    def show(self):
        for i in range(self.length):
            pygame.draw.rect(app.getScreen(),RED,(self.x[i],self.y[i],snake_block_size,snake_block_size))
    def update(self,direction):
        i = self.length -1
        while i >= 1:
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
            i -= 1
        if direction == "right":
            self.x[0] = (self.x[0]+(snake_block_size)) % screenx
        elif direction == "left":
            self.x[0] = (self.x[0]-(snake_block_size)) % screenx
        elif direction == "up":
            self.y[0] = (self.y[0]-(snake_block_size)) % screeny
        elif direction == "down":
            self.y[0] = (self.y[0]+(snake_block_size)) % screeny
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getLength(self):
        return self.length
        
    def eat(self):
        game.increaseScore()
        self.length += 1
        self.x.append(screenx-1)
        self.y.append(screeny-1)

class App():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('snake')
        self.screen = pygame.display.set_mode((screenx, screeny))
        self.clock = pygame.time.Clock()
        self.tickspeed = 20
    def exitGame(self):
        pygame.quit()
        quit()
    def getTickSpeed(self):
        return self.tickspeed
    def setTickSpeed(self,new_tickspeed):
        self.tickspeed = new_tickspeed
    def getClock(self):
        return self.clock
    def getScreen(self):
        return self.screen

#__________EVENTS RENDER__________#
def events():
    direction = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app.exitGame()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and game.getLastKey() != "right":
                direction = "left"
            elif event.key == pygame.K_RIGHT and game.getLastKey() != "left":
                direction = "right"
            elif event.key == pygame.K_UP and game.getLastKey() != "down":
                direction = "up"
            elif event.key == pygame.K_DOWN and game.getLastKey() != "up":
                direction = "down"
            elif event.key == pygame.K_SPACE:
                player.eat()
            if direction != "":
                game.setLastKey(direction)
            
def render():
    app.getScreen().fill(WHITE)
    player.show()
    game.showFood()
    game.showScore()
    pygame.display.update()
    app.getClock().tick(app.getTickSpeed())

def renderText(text,fontSize,colour,x,y):
    font = pygame.font.SysFont("monospace", fontSize)
    text = app.getScreen().blit((font.render(text, 1, colour)),(x,y))
    return text

#__________GAME FUNCTIONS__________#
def eatSnake():
    headx = player.getX()[0]
    heady = player.getY()[0]
    for i in range(1,player.getLength()):
        if player.getX()[i] == headx and player.getY()[i] == heady:
            return True
    return False

def eatFood():
    if game.showFood().collidepoint(player.getX()[0],player.getY()[0]):
        game.spawnFood()
        player.eat()

#__________GAME OVER__________#
        
def gameOverRender():
    app.getScreen().fill(WHITE)
    player.show()
    game.showFood()
    renderText("GAME OVER",30,BLACK,screenx/3,screeny/10)
    renderText("Score: {}".format(str(game.getScore())),20,BLACK,screenx/3,screeny/6)
    pygame.display.update()
    app.getClock().tick(app.getTickSpeed())

def gameOverGetMove(last_choice):
    new_choice = last_choice
    while new_choice == last_choice: 
        new_choice = random.choice(["up","down","left","right"])
        if last_choice == "up" and new_choice == "down":
            new_choice = "up"
        elif last_choice == "down" and new_choice == "up":
            new_choice = "down"
        elif last_choice == "left" and new_choice == "right":
            new_choice = "left"
        elif last_choice == "right" and new_choice == "left":
            new_choice = "right"
    return new_choice

def gameOverEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app.exitGame()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                return False
    return None

def gameOverScreen():
    move = 0
    computerChoice = game.getLastKey()
    while True:
        gameOverRender()
        play_again = gameOverEvents()
        move += 1
        if move % 15 == 0:
           computerChoice = gameOverGetMove(computerChoice)
        player.update(computerChoice)
        eatFood()
        if play_again == True:
            return True
        elif play_again == False:
            app.exitGame()
    
#__________MAIN__________#
def main():
    game.spawnFood()
    gameOver = False
    while not gameOver:
        events()
        render()
        player.update(game.getLastKey())
        eatFood()
        gameOver = eatSnake()
    gameOverScreen()

if __name__ == "__main__":
    while True:
        app = App()
        player = Player() #starting_length=10
        game = Game()
        main()


