
import collections
from pygame.locals import *
import pygame.font
import pygame
import random as rand

class Apple:
    def __init__(self):
        self.applesize = 20
        self.start_spawn_x_y = [(rand.randrange(0, 640)), (rand.randrange(0, 640))]

    def draw_apple(self, surface):
        red = (255,0,0)
        apple_spawn_x, apple_spawn_y = self.start_spawn_x_y[0], self.start_spawn_x_y[1]
        pygame.draw.rect(surface, red, pygame.Rect(apple_spawn_x, apple_spawn_y, self.applesize, self.applesize))
        pygame.display.flip()

    def respawn_apple(self):
        self.start_spawn_x_y = [(rand.randrange(0, 640 - self.applesize)), (rand.randrange(0, 640 - self.applesize))]

class Snake:
    def __init__(self, apple):
        self.snake_body = collections.deque([(300, 240), (320,240), (340, 240)])
        self.direction = 'RIGHT'
        self.segment_size = 20
        self.white = (255,255,255)
        self.apple = apple

    def snake_move(self):
        self.velocity = 10
        x_head, y_head = self.snake_body[0]
        if self.direction == 'UP':
            y_head -= self.velocity
        elif self.direction == 'DOWN':
            y_head += self.velocity
        elif self.direction == 'LEFT':
            x_head -= self.velocity
        elif self.direction == 'RIGHT':
            x_head += self.velocity
        self.snake_body.appendleft((x_head ,y_head))
        self.snake_body.pop()

    def draw_snake(self, surface):
        for segment in self.snake_body:
            pygame.draw.rect(surface, self.white, pygame.Rect(segment[0], segment[1], self.segment_size, self.segment_size))

    def grow_snake(self):
        self.snake_body.appendleft(self.snake_body[0])

    def eats_apple(self):
        if pygame.Rect(self.snake_body[0], (self.segment_size, self.segment_size)).colliderect(pygame.Rect(self.apple.start_spawn_x_y, (self.apple.applesize, self.apple.applesize))):
            return True
    def snake_hit_self(self):
        x_head, y_head = self.snake_body[0]
        snake_head = x_head, y_head
        for segments in range(2,len(self.snake_body)):
            if snake_head == self.snake_body[segments]:
                return True
    

    def border_return(self):
        x_head, y_head = self.snake_body[0]
        #from left screen to right screen
        if x_head == -10:
            self.snake_body.appendleft((600, y_head))
            self.snake_body.pop()
        if x_head == 610:
            self.snake_body.appendleft((0, y_head))
            self.snake_body.pop()
        if y_head == -10:
            self.snake_body.appendleft((x_head, 800))
            self.snake_body.pop()
        if y_head == 810:
            self.snake_body.appendleft((x_head, 0))
            self.snake_body.pop()
        
class App:
    def __init__(self):
        self._running = True
        self._display_surf = True
        self.size = self.width, self.height = (640, 800)
        self.apple = Apple()
        self.snake = Snake(self.apple)
        self.black = (0,0,0)
        self.font = 'times new roman'
        self.score = 0
        self.fps = 20
        self.game_over = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
        return True
    
    def restart_game(self):
        self.apple = Apple()
        self.snake = Snake(self.apple)
        self.score = 0
        self.fps = 20
        self.game_over = False
        pygame.display.flip()

    def game_over_screen(self):
        self._display_surf.fill(self.black)
        surface = pygame.Surface(self.size)
        surface.fill(self.black)
        pygame.font.init()
        game_over_str = 'Game Over!'
        game_over_font = pygame.font.SysFont(None, 100)
        game_over_text = game_over_font.render(game_over_str, True, (255,255,255), None)
        press_space = 'Press Space To Play Again!'
        press_space_font = pygame.font.SysFont(None, 60)
        press_space_text = press_space_font.render(press_space, True, (255,255,255), None) 

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_cleanup()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                        return 
            surface.blit(game_over_text, (self.width / 2 - game_over_text.get_width() / 2, self.height * 0.10))
            self._display_surf.blit(game_over_text, (self.width / 2 - game_over_text.get_width() / 2, self.height * 0.10))
            surface.blit(press_space_text, (self.width / 2 - press_space_text.get_width() / 2, self.height * 0.20))
            self._display_surf.blit(press_space_text, (self.width / 2 - press_space_text.get_width() / 2, self.height * 0.20))
            pygame.display.update()


    

    def show_score(self):
        pygame.font.init()
        score_font = pygame.font.SysFont(None, 43)
        text = score_font.render(str(self.score), True, (255,255,255), None)
        self._display_surf.blit(text, (self.width // 2, self.height * 0.10))
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

    def on_loop(self):
        #while self._running:     
            clockobject = pygame.time.Clock()
            clockobject.tick(self.fps)
            self.snake.snake_move()
            self.snake.draw_snake(self._display_surf)
            self.snake.border_return()
            if self.snake.eats_apple():
                #balance this later
                self.score += 10
                if self.score >= 100:
                    self.fps += self.fps * 0.010
                if self.score >= 500:
                    self.fps += self.fps * 0.010
                if self.score >= 750:
                    self.fps += self.fps * 0.010
                if self.score >= 1000:
                    self.fps += self.fps * 0.010
                self.snake.grow_snake()
                self.apple.respawn_apple()
            if self.snake.snake_hit_self():
                    self.game_over = True    
                

    def on_render(self):
        self._display_surf.fill(self.black)
        self.apple.draw_apple(self._display_surf)
        self.snake.draw_snake(self._display_surf)
        self.show_score()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def game_loop(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            if not self.game_over:
                self.on_loop()
                self.on_render()
            else:
                self.game_over_screen()
                        

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while True:  # Game loop
            self.game_loop()

if __name__ == '__main__':
    AppRunning = App()
    AppRunning.on_execute()
   