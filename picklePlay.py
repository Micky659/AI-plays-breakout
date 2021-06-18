import os
from breakAIout import eval_genomes
import pickle
import neat


def play_best_pickle(config_path, pickle_path):
    # Load neat config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Unpickle saved genome
    with open(pickle_path, "rb") as f:
        genome = pickle.load(f)

    # Convert to required data structure
    genomes = [(1, genome)]

    # Run breakout using only our winner genome
    eval_genomes(genomes, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward.txt')
    pickle_file = os.path.join(local_dir, "winner.pkl")
    play_best_pickle(config_file, pickle_file)
