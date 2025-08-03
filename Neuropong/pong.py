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
dv/dt = (v_rest - v + I)/tau : volt
dI/dt = -I/(5*ms) : volt
'''

#define 2 neurons
neurons = NeuronGroup(2, eqs, threshold='v>v_threshold', reset='v = v_reset', method='exact')
neurons.v = v_rest
neurons.I = 0 * mV

#spike monitor
spike_mon = SpikeMonitor(neurons)
net = Network(neurons, spike_mon)
last_spike_count = 0

#setup
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neuromorphic pong", icontitle="Neuromorphic pong") 
clock = pygame.time.Clock()

#objects
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [4, 4]
paddle = pygame.Rect(30, HEIGHT // 2 - 40, 10, 80)
paddle_speed = 18

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
    if ball_speed[0] < 0:
        prediction = ball.centery + ball_speed[1] * 10

        if prediction < paddle.centery - 5:
            neurons.I[0] = 50 * mV
            neurons.I[1] = 0 * mV
        elif prediction > paddle.centery + 5:
            neurons.I[0] = 0 * mV
            neurons.I[1] = 50 * mV
        else:
            neurons.I[:] = 0 * mV
    else:
        neurons.I[:] = 0 * mV  #the paddle doesn't move if the ball is moving away from it
    
    net.run(10*ms, report=None)
    new_spikes = spike_mon.i[last_spike_count:]

    if len(new_spikes) > 0:
        print(f"new spikes: {new_spikes}")
        if 0 in new_spikes:
            paddle.y -= paddle_speed  
        if 1 in new_spikes:
            paddle.y += paddle_speed  

    last_spike_count = len(spike_mon.i)

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


