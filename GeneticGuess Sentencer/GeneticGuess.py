##########################################
# CSE 231 Project 04 - GeneticGuess Sentencer
#
# Sentence guesser game attempts to generate a user's sentence randomly
# as quickly as possible using a genetic algorithm model
#
##########################################
import random
random.seed(10)

NUM_GENERATIONS = 200
NUM_POPULATION = 100
PROBABILITY_MUTATION = 0.2
PROBABILITY_CROSSOVER = 0.8
ALPHABET = 'abcdefghijklmnopqrstuvwxyz '

BANNER = """
**************************************************************
Welcome to GeneticGuess Sentencer! 
This program will attempt to guess a sentence that you input. 
Simply input a sentence and the program will attempt to guess it!
**************************************************************
"""

INPUT = "\nWould you like to continue? (y/n) "


def fitness(target, individual):
    '''
    compares two strings to determine similarity
    target: target string
    individual: single individual in population (string) to be compared against target
    returns: ratio of letters that match in the target and individual (float)
    '''
    fitness_value = 0
    for i, ch in enumerate(individual):
        if ch == target[i]:
            fitness_value += 1
    fitness_total = fitness_value / len(target)
    return fitness_total


def five_tournament_selection(population, target):
    '''
    generates five individuals out of a population randomly, then finds the one with the highest fitness
    population: population (string where individuals are chosen from)
    target: target string (to check for fitness)
    returns: individual with the highest fitness out of the five (str)
    '''
    individual_one, individual_two, individual_three, individual_four, individual_five = '', '', '', '', ''
    for i in range(0, 5):
        beginning_index = random.randint(0, NUM_POPULATION - 1) * len(target)
        end_index = beginning_index + len(target)
        if i == 0:
            individual_one = population[beginning_index:end_index]
            ind_one_fitness = fitness(target, individual_one)
            continue
        if i == 1:
            individual_two = population[beginning_index:end_index]
            ind_two_fitness = fitness(target, individual_two)
            continue
        if i == 2:
            individual_three = population[beginning_index:end_index]
            ind_three_fitness = fitness(target, individual_three)
            continue
        if i == 3:
            individual_four = population[beginning_index:end_index]
            ind_four_fitness = fitness(target, individual_four)
            continue
        if i == 4:
            individual_five = population[beginning_index:end_index]
            ind_five_fitness = fitness(target, individual_five)
            break

    # find individual with the greatest fitness out of the five
    max_fitness = -1
    highest_fitness = ''
    if ind_one_fitness > max_fitness:
        max_fitness = ind_one_fitness
        highest_fitness = individual_one
    if ind_two_fitness > max_fitness:
        max_fitness = ind_two_fitness
        highest_fitness = individual_two
    if ind_three_fitness > max_fitness:
        max_fitness = ind_three_fitness
        highest_fitness = individual_three
    if ind_four_fitness > max_fitness:
        max_fitness = ind_four_fitness
        highest_fitness = individual_four
    if ind_five_fitness > max_fitness:
        max_fitness = ind_five_fitness
        highest_fitness = individual_five
    return highest_fitness


def make_population(target):
    '''
    creates NUM_POPULATION (100) individuals, each letter is randomly chosen.
    adds individuals together to create a population
    target: target string
    returns: the full population (str)
    '''
    population = ''
    individual = ''
    for i in range(NUM_POPULATION):
        for x in range(len(target)):
            individual += random.choice(ALPHABET)
    population += individual
    return population


def mutation(individual):
    '''
    randomly generates number between 0-1 for each character in individual
    based on the number, either replace the character with a random one or not
    individual: the given individual to be mutated (str)
    returns: the mutated individual (str)
    '''
    mutated_individual = ''
    for i, ch in enumerate(individual):
        number = random.random()
        if number <= PROBABILITY_MUTATION:
            ch = ch.replace(ch, random.choice(ALPHABET))
            mutated_individual += ch
        if number > PROBABILITY_MUTATION:
            mutated_individual += ch
    return mutated_individual


def single_point_crossover(individual1, individual2):
    '''
    randomly generate number between 0-1
    based on the number, either switch the halves of each individual at a crossover point, or not
    individual1: the first individual of the crossover (str)
    individual2: the second individual of the crossover (str)
    returns: either a new, crossover version of each individual (str) or not (str)
    '''
    number = random.random()
    if number <= PROBABILITY_CROSSOVER:
        crossover_point = random.randint(1, len(individual1))
        new_individual1 = individual1[:crossover_point] + individual2[crossover_point:]
        new_individual2 = individual2[:crossover_point] + individual1[crossover_point:]
        return new_individual1, new_individual2
    else:
        return individual1, individual2


def find_best_individual(population, target):
    '''
    finds the best individual out of an entire population by comparing each individuals fitness
    population: the full population where the individuals are taken from (str)
    target: the target phrase (str) used for length and fitness to find each individual and their fitness
    returns: individual with highest fitness (str)
    '''
    max_fitness = -1
    best_individual = ''
    n = len(target)
    # for each individual in a population, find one with highest fitness
    for i in range(0, len(population), len(target)):

        individual = population[i:i + n]
        individual_fitness = fitness(target, individual)

        if individual_fitness > max_fitness:
            max_fitness = individual_fitness
            best_individual = individual

    return best_individual


def main():
    '''
    where all user input and printing is performed
    takes no arguments, returns nothing
    '''
    print(BANNER)
    input_answer = input(INPUT)

    while input_answer == "y" or input_answer == "Y":

        target = input("\nPlease input the sentence you would like the program to guess: ").lower()
        # check if all characters in target are in the alphabet constant
        for i, ch in enumerate(target):
            if ch in ALPHABET:
                continue
            else:
                print("\nIncorrect input. Please try again.\n")
                target = input("\nPlease input the sentence you would like the program to guess: ").lower()
                break

        # initialize beginning population
        population = make_population(target)
        print("\n\nGeneticGuess results:")
        # iterate over number of generations

        for i in range(NUM_GENERATIONS):
            print("Generation: ", i, sep=" ")
            # values reset for each generation iteration
            best_individual = ''
            new_population = ''
            # iterate over number of individuals in a population
            for index in range(NUM_POPULATION):

                # select two individuals from the tournament, mutate, then crossover
                individual_one = five_tournament_selection(population, target)
                individual_two = five_tournament_selection(population, target)
                individual_one, individual_two = mutation(individual_one), mutation(individual_two)
                individual_one, individual_two = single_point_crossover(individual_one, individual_two)
                # find fitness of each individual
                individual_one_fitness = fitness(target, individual_one)
                individual_two_fitness = fitness(target, individual_two)

                # determine which one is best, add to new population
                if individual_two_fitness >= individual_one_fitness:
                    best_individual = individual_two
                else:
                    best_individual = individual_one

                new_population += best_individual

            # find best of most recent population
            population = new_population
            best_individual = find_best_individual(population, target)

            if best_individual == target:
                print("I found the sentence early!")
                break

        print("\nBest Individual: ", best_individual)
        input_answer = input(INPUT)
    print("\n\nThank you for using GeneticGuess Sentencer!")

if __name__ == '__main__':
    main()
