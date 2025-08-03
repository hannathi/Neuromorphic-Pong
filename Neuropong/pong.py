#pong.py
import pygame
import sys

py_min = min
py_max = max

from brian2 import *
import random

start_scope()  

#neuron parameters
tau = 10*ms
v_rest = -70*mV
v_threshold = -50*mV
v_reset = -70*mV

#LIF definition
eqs = '''
dv/dt = (v_rest - v)/tau : volt
'''

#define 2 neurons
neurons = NeuronGroup(2, eqs, threshold='v>v_threshold', reset='v = v_reset', method='exact')
neurons.v = v_rest

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
        ball_speed[1] = py_max(-5, py_min(ball_speed[1], 5))

    #Paddle logic
    if ball.centery < paddle.centery:
        paddle.y -= paddle_speed
    elif ball.centery > paddle.centery:
        paddle.y += paddle_speed
    
    if paddle.y < 0:
        paddle.y = 0
    elif paddle.y > HEIGHT - paddle.height:
        paddle.y = HEIGHT - paddle.height


    #render game
    screen.fill((40, 30, 60))
    pygame.draw.rect(screen, (200, 200, 200), paddle)
    pygame.draw.ellipse(screen, (200, 200, 0), ball)
    pygame.display.flip()
    clock.tick(60)


