# AI-plays-breakout
An AI that uses NEAT algorithm and python to beat the famous atari game breakout released in 1976.
NeuroEvolution of Augmenting Topologies (NEAT) is a genetic algorithm for the generation of evolving artificial neural networks developed by Ken Stanley. Best performimg agents are passed onto then next generation and repeated process of this creates an efficient agent that can produce optimal set of action for the given task.

# Neural network
The program have a simple two layer feed forward neural network that uses tanh as an activation function to decide actions to be performed.
* Input layer- Consist of 5 nodes(Coordinates of ball and paddle and distance between ball and paddle)
* Hidden layer- Consist of 4 neurons
* Output layer- Consist of 3 nodes(Do nothing, go left, go right)

# Efficiency 
The program efficiency to develop a desirable agent is directly dependent on population size on each generation, where a pop size of 200 can take up to 10-12 generations a population of 500 require only 2-3 gens and population of 1000 can sometimes do the trick on the first shot. You can tweak the neural net hyperparameters and network size to see the effect of it in the learning process.

# Reward function 
The reward or fitness is incremented positively when a particular agent collides with the ball and decremented when it misses or if the ball hits the ground.

<p>&nbsp;</p>


### Example
![](https://i.imgur.com/3a8n6BC.gif)

<p>&nbsp;</p>

***Be my guest to build over my code and use it wisely***
