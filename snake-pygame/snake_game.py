import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25) 

# rgb colors 
WHITE = (255,255,255)
RED = (255,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SMALL_SQUARE = 12
SMALL_SQUARE_POS = 4
SPEED = 10
class Direction(Enum):
  RIGHT = 1
  LEFT = 2
  UP = 3
  DOWN = 4

Point = namedtuple('Point', ['x', 'y'])

class SnakeGame:

  def __init__(self, w=640, h=480):
    self.w = w
    self.h = h

    # init display
    self.display = pygame.display.set_mode((self.w, self.h))
    pygame.display.set_caption("Snake")
    self.clock = pygame.time.Clock()

    # init game state
    self.direction = Direction.RIGHT

    self.head = Point(self.w/2, self.h/2)
    self.snake = [
      self.head,
      Point(self.head.x - (BLOCK_SIZE), self.head.y),
      Point(self.head.x - (BLOCK_SIZE*2), self.head.y),
    ]

    self.score = 0
    self.food = None
    self._place_food()

  def _place_food(self):
    x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    food = Point(x, y)
    if food in self.snake:
      self._place_food()
    else:
      self.food = food

  def _update_ui(self):
    self.display.fill(BLACK)

    for pt in self.snake:
      pygame.draw.rect(self.display, BLUE1, pygame.Rect( pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE ))
      pygame.draw.rect(self.display, BLUE2, pygame.Rect( (pt.x+SMALL_SQUARE_POS), (pt.y+SMALL_SQUARE_POS), SMALL_SQUARE, SMALL_SQUARE ))

    pygame.draw.rect(self.display, RED, pygame.Rect( self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE ))

    score_text = font.render(f"Score: {str(self.score)}", True, WHITE)
    self.display.blit(score_text, [0, 0])
    pygame.display.flip()

  def _move(self, direction):
    x = self.head.x
    y = self.head.y
    if direction == Direction.RIGHT:
      x += BLOCK_SIZE
    elif direction == Direction.LEFT:
      x -= BLOCK_SIZE
    elif direction == Direction.UP:
      y -= BLOCK_SIZE
    elif direction == Direction.DOWN:
      y += BLOCK_SIZE

    self.head = Point(x, y)
    
  def _is_collided(self):
    # hit boundary
    if self.head.x < 0 or self.head.y < 0 or self.head.x > self.w - BLOCK_SIZE or self.head.y > self.h - BLOCK_SIZE:
      return True
    # hit itself
    if self.head in self.snake[1:]:
      return True

    return False

  def play_step(self):
    # 1. collect user input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
          self.direction = Direction.DOWN        
        elif event.key == pygame.K_LEFT:
          self.direction = Direction.LEFT
        elif event.key == pygame.K_RIGHT:
          self.direction = Direction.RIGHT
        elif event.key == pygame.K_UP:
          self.direction = Direction.UP        

    # 2. move
    self._move(self.direction)  # updates the head
    self.snake.insert(0, self.head)

    # 3. check if game over
    game_over=False
    if self._is_collided():
      game_over=True
      return game_over, self.score

    # 4. place new food or move
    if self.head == self.food:
      self.score+=1
      self._place_food()
    else:
      self.snake.pop()

    # 5. update ui and clock
    self._update_ui()
    self.clock.tick(SPEED)
    # 6. return game over and score
    return game_over, self.score

if __name__ == '__main__':
  # initiate SnakeGame
  game = SnakeGame()

  # game loop
  while True:
    game_over, score = game.play_step()
    # break if game over
    if game_over == True:
      break 

  pygame.quit()
