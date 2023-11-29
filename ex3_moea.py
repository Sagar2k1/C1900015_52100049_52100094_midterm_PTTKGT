#Ex3

import random
import time
from check import *

start_time = time.time()
# bench mark
tau = 100  # iteration

n = 100  # số item
capacity = n
r = 5
items_list = {}

weight = [random.uniform(1, 1000) for _ in range(n)]
value = None
if check_weights(weight):
    value = [random.uniform(-r, r) for _ in range(n)]
else:
    value = [random.uniform(1, 1000) for _ in range(n)]
    value2 = [w + 100 for w in weight]
items_list['uncorr'] = [(int(i), int(j)) for (i, j) in zip(value, weight)]
items_list['bou-s-c'] = [(int(i), int(j)) for (i, j) in zip(value2, weight)]

weight = [random.uniform(1000, 1010) for _ in range(n)]
value = [random.uniform(1, 1000) for _ in range(n)]
items_list['unc-s-w'] = [(int(i), int(j)) for (i, j) in zip(value, weight)]

# Knapsack problem parameters
n = 10
#items = [(5, 5), (8, 3), (15, 7), (6, 2)] #(value, weight) tuples
items = items_list["bou-s-c"]
total_weight = sum([i[1] for i in items])
knapsack_capacity = total_weight+1
population_size = n
max_generations = tau
mutation_rate = 0.4

for i in range(n):
    items.append((int(random.uniform(-5,5)),1))
print(items)


def generate_individual():
    # Generate a random individual (candidate solution)
    individual = [random.choice([0, 1]) for _ in range(len(items))]
    return individual

def evaluate(individual):
    # Calculate the fitness of an individual
    total_value = sum(item[0] * x for item, x in zip(items, individual))
    total_weight = sum(item[1] * x for item, x in zip(items, individual))
    if total_weight > knapsack_capacity:
        total_value = 0  # Penalize solutions that violate the weight constraint
    return total_value

def crossover(parent1, parent2):
    # Perform crossover between two parents to create offspring
    point = random.randint(1, len(parent1) - 1)
    offspring = parent1[:point] + parent2[point:]
    return offspring

def mutate(individual, mutation_rate):
    # Perform mutation on an individual with a given mutation rate
    mutated_individual = []
    for gene in individual:
        if random.random() < mutation_rate:
            mutated_individual.append(int(not gene))  # Flip the bit
        else:
            mutated_individual.append(gene)
    return mutated_individual

def run(max_generations, population_size):
    # Initialization
    population = [generate_individual() for _ in range(population_size)]

    # Evolutionary loop
    for generation in range(max_generations):
        # Evaluation
        fitness_values = [evaluate(individual) for individual in population]

        # Selection
        offspring = []
        while len(offspring) < population_size:
            parent1 = random.choices(population, weights=fitness_values)[0]
            parent2 = random.choices(population, weights=fitness_values)[0]
            child = crossover(parent1, parent2)
            offspring.append(child)

        # Mutation
            offspring = [mutate(child, mutation_rate) for child in offspring]

        # Replacement: Replace the population with the offspring
        population = offspring

    # Final evaluation and output
    fitness_values = [evaluate(individual) for individual in population]
    best_individual = population[fitness_values.index(max(fitness_values))]
    best_fitness = max(fitness_values)
    return fitness_values, best_individual, best_fitness
fitness_values = None
best_individual = None
best_fitness = None
times_list = []
for i in range(tau):
    start_time = time.time()
    fitness_values, best_individual, best_fitness = run(i, population_size)
    end_time = time.time()
    execution_time = end_time - start_time
    times_list.append(execution_time)
    print(i+1,": ",execution_time)
print(times_list)




output_file = "benchmarkMOEA.out"

# Mở file để ghi
file = open(output_file, "w")

# In thông tin về knapsack problem parameters
file.write("Items: {}\n".format(items))
file.write("Knapsack Capacity: {}\n".format(knapsack_capacity))
file.write("Population Size: {}\n".format(population_size))
file.write("Max Generations: {}\n".format(max_generations))
file.write("Mutation Rate: {}\n".format(mutation_rate))

# In thông tin về best_individual và best_fitness
file.write("Best Individual: {}\n".format(best_individual))
file.write("Best Fitness: {}\n".format(best_fitness))


# In thông tin về execution_time
for i in range(tau):
    file.write("Execution Time {}: {} seconds\n".format(i+1,times_list[i]))

# Đóng file sau khi ghi
file.close()