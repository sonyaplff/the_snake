from random import randint
import pygame

# Настройки экрана
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (93, 216, 228)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
FPS = 10

class Apple:
    def __init__(self):
        self.position = self.random_position()
        self.color = RED
        
    def random_position(self):
        # Создаем яблоко в случайной позиции, кратной размеру сетки
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return (x, y)
        
    def draw(self):
        # Рисуем яблоко
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLUE, rect, 1)

class Snake:
    def __init__(self):
        # Начальная позиция змейки
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.color = GREEN
        self.length = 1
        
    def change_direction(self, new_direction):
        # Не позволяем змейке развернуться на 180 градусов
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
            
    def move(self):
        # Меняем направление
        self.direction = self.next_direction
        
        # Получаем текущую позицию головы
        head_x, head_y = self.positions[0]
        
        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверяем столкновение с собой
        if new_head in self.positions:
            self.reset()
            return
            
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()
            
    def reset(self):
        # Сбрасываем змейку к начальному состоянию
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1
        
    def grow(self):
        # Увеличиваем длину змейки
        self.length += 1
        
    def get_head_position(self):
        # Возвращаем позицию головы
        return self.positions[0]
        
    def draw(self):
        # Рисуем змейку
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BLUE, rect, 1)

def main():
    snake = Snake()
    apple = Apple()
    
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
        
        # Движение змейки
        snake.move()
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.random_position()
            # Убеждаемся, что яблоко не появилось в змейке
            while apple.position in snake.positions:
                apple.position = apple.random_position()
        
        # Отрисовка
        screen.fill(BLACK)  # Очищаем экран
        snake.draw()
        apple.draw()
        pygame.display.update()
        
        # Контроль FPS
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
