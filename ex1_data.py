import random

items_list = {}  # (value, weight) tuples
tau = 100  # iteration

n = 100  # số item
capacity = n
r = 5

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
