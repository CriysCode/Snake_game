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
        pass
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

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
        return True
    
    def game_over_screen(self):
        pass

    

    def show_score(self):
        pygame.font.init()
        score_font = pygame.font.SysFont(None, 43)
        text = score_font.render(str(self.score), True, (255,255,255), None)
        self._display_surf.blit(text, (self.width / 2, self.height * 0.10))
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
        clockobject = pygame.time.Clock()
        clockobject.tick(self.fps)
        self.snake.snake_move()
        self.snake.draw_snake(self._display_surf)
        if self.snake.eats_apple():
            #balance this later
            self.score += 10
            if self.score >= 100:
                self.fps += self.fps * 0.010
            if self.score >= 200:
                self.fps += self.fps * 0.010
            if self.score >= 300:
                self.fps += self.fps * 0.010
            if self.score >= 400:
                self.fps += self.fps * 0.010
            self.snake.grow_snake()
            self.apple.respawn_apple()

    def on_render(self):
        self._display_surf.fill(self.black)
        self.apple.draw_apple(self._display_surf)
        self.snake.draw_snake(self._display_surf)
        self.show_score()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

if __name__ == '__main__':
    AppRunning = App()
    AppRunning.on_execute()