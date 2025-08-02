#pong.py
import pygame
import sys
import random

#setup
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#objects
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [4, 4]
paddle = pygame.Rect(30, HEIGHT // 2 - 40, 10, 80)
paddle_speed = 4

def reset():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] *= -1  #direction change

#loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #ball logic
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1
    
    if ball.right >= WIDTH:
        ball_speed[0] *= -1

    if ball.left <= 0:
        reset()
    
    if ball.colliderect(paddle):
        ball_speed[0] *= -1
        ball_speed[1] += random.choice([-1, 0, 1])
        ball_speed[1] = max(-5, min(ball_speed[1], 5))

    #Paddle logic
    if ball.centery < paddle.centery:
        paddle.y -= paddle_speed
    elif ball.centery > paddle.centery:
        paddle.y += paddle_speed
    
    paddle.y = max(0, min(paddle.y, HEIGHT - paddle.height))

    #render game
    screen.fill((40, 30, 60))
    pygame.draw.rect(screen, (200, 200, 200), paddle)
    pygame.draw.ellipse(screen, (200, 200, 0), ball)
    pygame.display.flip()
    clock.tick(60)


