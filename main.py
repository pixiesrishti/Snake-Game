import pygame, random
from pygame import Vector2

pygame.init()
difficulty=200
OFFSET = 50
score_font = pygame.font.SysFont("bahnschrift", 40)
#GRID
cell_size=27
number_of_cells=22
screen = pygame.display.set_mode((2 * OFFSET + cell_size*number_of_cells, 2 * OFFSET + cell_size*number_of_cells))


class Food:

    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
    
    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_icon, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x,y)

    def generate_random_pos(self, snake_body):

        position = self.generate_random_cell()

        while position in snake_body:
            position = self.generate_random_cell()

        return position

class Snake:
    def __init__(self):
        self.body=[Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False
        self.bg_sound = pygame.mixer.Sound("Snake Game/SFX/bg_music_1.mp3")
        self.eat_sound = pygame.mixer.Sound("Snake Game/SFX/ding.mp3")
        self.hit_sound = pygame.mixer.Sound("Snake Game/SFX/crash.mp3")

        self.bg_sound.play(-1)


    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, "green", segment_rect, 0, 7)
        
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)


class Game:
    def __init__(self):
        self.snake=Snake()
        self.food=Food(self.snake.body)
        self.state="RUNNING"
        self.score = 0


    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.snake.hit_sound.play()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()



pygame.display.set_caption("Snake Game")

icon_image=pygame.image.load("Snake Game/Media/Icon.png").convert()
pygame.display.set_icon(icon_image)

background_image = pygame.image.load("Snake Game/Media/background.jpg") 
background_image = pygame.transform.scale(background_image, (2 * OFFSET + cell_size*number_of_cells, 2 * OFFSET + cell_size*number_of_cells))

clock = pygame.time.Clock()
running = True

game=Game()

food_icon = pygame.image.load("Snake Game/Media/Apple.png").convert_alpha()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, difficulty)

while running:

    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
               game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0) 


    screen.blit(background_image, (0, 0))
    game.draw()
    pygame.draw.rect(screen, "black", (OFFSET, OFFSET, cell_size*number_of_cells, cell_size*number_of_cells), 3)
    
    score_surface = score_font.render("SCORE: " + str(game.score), True, "#006400")
    score_rect = score_surface.get_rect(center=(screen.get_width() // 2, 30))
    screen.blit(score_surface, score_rect)


    pygame.display.flip()   #To update window

    clock.tick(60)  #Cap FPS

pygame.quit()