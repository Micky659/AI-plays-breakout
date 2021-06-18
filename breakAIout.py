import pickle

import pygame
import random
import os
import neat
from pygame.locals import *

# Initialize pygame and pygame font
pygame.init()
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 500

ball_color = (255, 255, 255)

# Load font from folder font
Font = pygame.font.Font(os.path.join("font", 'font.ttf'), 24)

# Create game window
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Breakout")

# Load graphics from folder res
bg = pygame.transform.scale(pygame.image.load(os.path.join("res", "background.png")).convert_alpha(), (610, 510))
paddle = pygame.transform.scale(pygame.image.load(os.path.join("res", "paddle.png")).convert_alpha(), (100, 15))
block = pygame.transform.scale2x(pygame.image.load(os.path.join("res", "brick.png")).convert_alpha())

# Parameter for brick formation
rows = random.randrange(4, 6)
num = int((WIN_WIDTH - 30) / block.get_width())

gen = 0


class Paddle(pygame.sprite.Sprite):
    velocity = 10
    alive = True

    def __init__(self, image):
        self.img = image
        self.rect = self.img.get_rect()
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top

        self.x = WIN_WIDTH / 2 - 50
        self.rect = pygame.Rect(200, self.x, self.width, self.height)

        self.rect.x = self.x
        self.rect.y = WIN_HEIGHT - 30
        self.edge = WIN_WIDTH - self.width - 5

    def move_paddle_left(self):

        self.rect.x -= self.velocity
        if self.rect.x < 5:
            self.rect.x = 5

    def move_paddle_right(self):

        self.rect.x += self.velocity
        if self.rect.x > self.edge:
            self.rect.x = self.edge

    def isAlive(self):  # Function used to eliminate failed population

        return self.alive


class Bricks(pygame.sprite.Sprite):

    def __init__(self, image):
        self.img = image
        self.rect = self.img.get_rect()

        self.width = self.rect.right - self.rect.left
        self.height = self.rect.bottom - self.rect.top

    def set_bricks(self):
        self.lists = []
        y = 35
        for i in range(rows):
            x = 30
            for k in range(num):
                self.lists.append(pygame.Rect(x, y, self.width, self.height))
                x += self.width
            y += self.height


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        self.diameter = 20
        self.radius = int(self.diameter / 2)
        self.edge = WIN_WIDTH - self.diameter

        self.x = WIN_WIDTH / 2 - 10
        self.rect = pygame.Rect(200, self.x - self.diameter, self.diameter, self.radius)

        self.rect.y = 300
        self.rect.x = self.x

        self.velocity = [3, -3]

    def reverse_x(self):
        self.velocity[0] = -self.velocity[0]

    def reverse_y(self):
        self.velocity[1] = -self.velocity[1]

    def ball_collisions(self, mul):  # Detect window edge collision and move the ball
        self.rect.x = self.rect.x - (self.velocity[0] * mul)
        self.rect.y += self.velocity[1]

        if self.rect.x <= 0:
            self.rect.x = 0
            self.reverse_x()

        elif self.rect.x >= self.edge:
            self.rect.x = self.edge
            self.reverse_x()

        if self.rect.y < 0:
            self.rect.y = 0
            self.reverse_y()

    def draw(self):
        pygame.draw.circle(window, ball_color,
                           [(self.rect.x + self.radius), (self.rect.y + self.radius)],
                           self.radius)


def display(score, win, player, level):
    # Current score
    score_label = Font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (440, 10))

    # Current generation
    score_label = Font.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(score_label, (20, 10))

    # Number of population alive
    score_label = Font.render("Alive: " + str(player), 1, (255, 255, 255))
    win.blit(score_label, (170, 10))

    # Current level
    score_label = Font.render("Level: " + str(level), 1, (255, 255, 255))
    win.blit(score_label, (320, 10))


def eval_genomes(genomes, config):
    global window, gen
    win = window
    gen += 1

    nets = []
    player = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        # If we are using pickle then we can directly append it to nets
        if type(genome) is not neat.nn.feed_forward.FeedForwardNetwork:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
        else:
            nets.append(genome)
        player.append(Paddle(paddle))
        ge.append(genome)

    bricks = Bricks(block)
    ball = Ball()
    bricks.set_bricks()

    score = 0
    level = 1
    mul = random.randrange(-1, 2, 2)  # Randomize ball direction on each generation
    clock = pygame.time.Clock()

    run = True
    while run and len(player) > 0:

        win.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                quit()
                break

        ball.ball_collisions(mul)
        winner = 0
        for x, play in enumerate(player):
            ge[x].fitness += 0.1  # Reward agents at each frame for staying alive
            ball.draw()

            if play.isAlive():  # Only display alive population
                win.blit(play.img, play)
                winner += 1

            output = nets[player.index(play)].activate(
                (play.rect.y, ball.rect.x, ball.rect.y, abs(play.rect.x - ball.rect.x), abs(play.rect.y - ball.rect.y)))
            action = output.index(max(output))
            if action == 0:  # Do nothing
                pass
            if action == 1:  # Go left
                play.move_paddle_left()
            if action == 2:  # Go right
                play.move_paddle_right()

        for play in player:
            if ball.rect.colliderect(play):  # Reward agents if they collide with ball
                ge[player.index(play)].fitness += 10
                for pla in player:  # Agents that miss the ball are failed and punished
                    if not ball.rect.colliderect(pla):
                        ge[player.index(pla)].fitness -= 5
                        pla.alive = False
                ball.reverse_y()
                ball.rect.top = play.rect.y - ball.diameter

        if ball.rect.y > WIN_HEIGHT:  # If ball get past all agents then punish all and end game
            score = 0
            for play in player:
                ge[player.index(play)].fitness -= 5
                nets.pop(player.index(play))
                ge.pop(player.index(play))
                player.pop(player.index(play))

        rand = random.randrange(2, 5)  # Randomize ball speed after it hit a brick
        for brick in bricks.lists:
            if ball.rect.colliderect(brick):
                score += 10
                if brick.left > ball.rect.right or ball.rect.left < brick.right:
                    ball.reverse_y()
                    ball.velocity[1] = rand
                elif brick.bottom > ball.rect.top or ball.rect.bottom < brick.top:
                    ball.reverse_x()
                    ball.velocity[0] = rand
                bricks.lists.remove(brick)  # Remove the brick from the list after collision

        if len(bricks.lists) == 0:  # If all the bricks are cleared increment level by 1 and reset brick formation
            bricks.set_bricks()
            score += 1000
            level += 1

        for brick in bricks.lists:  # Update bricks on the screen using the list
            window.blit(bricks.img, brick)

        if winner == 0:  # If all the agents fail then end generation
            break

        display(score, win, winner, level)

        if score > 400:
            # Save best player using pickle
            with open('winner.pkl', "wb") as f:
                pickle.dump(nets[player.index([ply for ply in player if ply.alive][0])], f)
                f.close()
            break

        clock.tick(60)  # Set max fps
        pygame.display.flip()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

# Created by Akshat Kothari (May, 2020)
