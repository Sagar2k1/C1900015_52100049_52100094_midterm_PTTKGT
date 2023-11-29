import random

n = 1000
r = 5
items = []
for i in range(n):
    value = int(random.uniform(-r,r))
    weight = int(random.uniform(-r,r))
    item = (value, weight)
    items.append(item)

total_weights = sum([item[1] for item in items])
capacity = total_weights+1
print(items[:10])
print(capacity)

def evaluate_fitness(items):
    total_values = sum([items[0] for item in items])
    total_weights = sum([item[1] for item in items])
    if total_weights>capacity:
        return 0
    return total_values

def 
    