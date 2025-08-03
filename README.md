# Neuromorphic-Pong

Neuromorphic pong is a small project where the paddle is controlled by a small spiking neural network (SNN). The SNN is implemented using the Brian2 simulator for demonstration of how neural dynamics can be implemented for game controls. 

## How it works
The SNN consists of two Leaky integrate-and-fire (LIF) neurons, where each neuron corresponds to a paddle moement direction. One moves the paddle up and the other one moves it down. 

- When a neuron spikes, the paddle moves
- Input current is based on the balls position and prediction in ball movement 

## Possible improvements

- Adding randomness to the paddle to simulate a more "human"-like behavior in the gameplay (right now the computer doesn't lose)
- Adding a learning curve for the computer paddle, improving paddle control over time
- Adding more neurons for more advanced behavior and game mechanics 
- Adding a second player


