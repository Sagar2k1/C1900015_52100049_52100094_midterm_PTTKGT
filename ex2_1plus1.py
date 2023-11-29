from check import *
import random
import time

items = {}  # (value, weight) tuples
tau = 100  # iteration

n = 100  # số item
r = 5

weight = [random.uniform(1, 1000) for _ in range(n)]
value = None
if check_weights(weight):
    value = [random.uniform(-r, r) for _ in range(n)]
else:
    value = [random.uniform(1, 1000) for _ in range(n)]
    value2 = [w + 100 for w in weight]
items['uncorr'] = [(int(i), int(j)) for (i, j) in zip(value, weight)]
items['bou-s-c'] = [(int(i), int(j)) for (i, j) in zip(value2, weight)]

weight = [random.uniform(1000, 1010) for _ in range(n)]
value = [random.uniform(1, 1000) for _ in range(n)]
items['unc-s-w'] = [(int(i), int(j)) for (i, j) in zip(value, weight)]

#=========================================================================
def sqrt(number):
    if number < 0:
        return None
    x = number
    y = (x + 1) / 2
    while y < x:
        x = y
        y = (number / x + x) / 2
    return x

def fitness(solution, items):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += items[i][0]
            total_weight += items[i][1]
    if total_weight <= capacity:
        return total_value
    else:
        return 0

def mutate(solution):
    new_solution = solution[:]
    index = random.randint(0, len(solution) - 1)
    new_solution[index] = 1 - new_solution[index]
    return new_solution

# Start EA
# 1+1 EA
def one_plus_one_ea(tau, items):
    best = [0] * len(items)
    best_fitness = fitness(best, items)
    vau = []

    for i in range(tau):
        child = mutate(best)
        child_fitness = fitness(child, items)  # y

        if child_fitness > best_fitness:
            best = child
            best_fitness = child_fitness
        vau.append(child_fitness)
    return best, best_fitness, vau


type = 'bou-s-c'
capacity = sum([i[1] for i in items[type]])+1
best = None
best_fitness = None
vau = None
times_list = []
for i in range(tau):
    start = time.time()
    best, best_fitness, vau = one_plus_one_ea(tau, items[type])
    end = time.time()
    execution_time = end-start
    times_list.append(execution_time)
    print(i,": ", execution_time)
path = 'benchmark1plus1EA.out'
file = open(path, "w+")
solutions = [i[0] for i in items[type]]
error = [solution - expect for (solution, expect) in zip(solutions, best)]
offical_error = [solution + vau_i for (solution, vau_i) in zip(solutions, vau)]
mean = sum(offical_error) / n
std = sqrt(sum([(i - mean) * (i - mean) for i in error]) / (n - 1))
# print(items)
print("mean: ", round(mean, 2))
print("std: ", round(std, 2))
print("Fitness: ", best_fitness)
file.write('mean: {}\n'.format(mean))
file.write('standard variance: {}\n'.format(std))
file.write('Best fitness: {}\n'.format(best_fitness))
file.write("times list: {}\n".format(times_list))
for i in range(tau):
    file.write("Execution Time with iter = {}: {}\n".format(i+1,times_list[i]))
file.close()
