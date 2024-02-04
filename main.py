import collections
from pygame.locals import *
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
        self.start_spawn_x_y = [(rand.randrange(0, 640)), (rand.randrange(0, 640))]

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
        self.snake_body.append(self.snake_body[-1])

    def eats_apple(self):
        x_head, y_head = self.snake_body[0]
        apple_pos_x, apple_pos_y = self.apple.start_spawn_x_y
        return x_head == apple_pos_x and y_head == apple_pos_y

class App:
    def __init__(self):
        self._running = True
        self._display_surf = True
        self.size = self.width, self.height = (640, 800)
        self.apple = Apple()
        self.snake = Snake(self.apple)
        self.black = (0,0,0)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
        return True

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
        clockobject.tick(20)
        self.snake.snake_move()
        self.snake.draw_snake(self._display_surf)
        if self.snake.eats_apple():
            self.snake.grow_snake()
            self.apple.respawn_apple()

    def on_render(self):
        self._display_surf.fill(self.black)
        self.apple.draw_apple(self._display_surf)
        self.snake.draw_snake(self._display_surf)
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