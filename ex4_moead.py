#Ex4
import random
from check import *
import time

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

type = "bou-s-c"
# Knapsack problem parameters
items = items_list[type]  # List of items with values and weights
knapsack_capacity = sum([i[1] for i in items])+1  # Maximum capacity of the knapsack

# MOEA/D parameters
population_size = n
max_generations = tau
subproblem_count = int(tau/10)
neighbourhood_size = 5
mutation_rate = 0.4


def generate_individual():
    # Generate a random individual (candidate solution)
    individual = [random.choice([0, 1]) for _ in range(len(items))]
    return individual


# Rest of the code remains the same
# ...
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

# Initialization
def run(max_generations, population_size, subproblem_count):
    population = [generate_individual() for _ in range(population_size)]
    weight_vectors = [[random.random() for _ in range(len(items))] for _ in range(subproblem_count)]  # Random weight vectors

    # Evolutionary loop
    for generation in range(max_generations):
        for subproblem_index in range(subproblem_count):
            subproblem = population[subproblem_index]

            # Neighbourhood selection
            neighbourhood = random.sample(range(subproblem_count), neighbourhood_size)

            # Reproduction
            parent1 = subproblem
            parent2 = population[random.choice(neighbourhood)]
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring, mutation_rate)

            # Update subproblem with better offspring
            if evaluate(offspring) >= evaluate(subproblem):
                population[subproblem_index] = offspring

    # Final evaluation and output
    fitness_values = [evaluate(individual) for individual in population]
    best_individual = population[fitness_values.index(max(fitness_values))]
    best_fitness = max(fitness_values)
    return best_fitness, best_individual

best_fitness = None
best_individual = None
times_list = []
for i in range(max_generations):
    start = time.time()
    best_fitness, best_individual = run(i, population_size, subproblem_count)
    end_time = time.time()
    execution_time = end_time - start
    times_list.append(execution_time)
    print(i+1, ": ", execution_time)

output_file = "benchmarkMOEAD.out"

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
file.write("Times list: {}\n".format(times_list))
# In thông tin về execution_time
for i in range(max_generations):
    file.write("Execution Time {}: {} seconds\n".format(i+1, times_list[i]))

# Đóng file sau khi ghi
file.close()