import random

def stalin_sort(l: list) -> list:
    comrade_list = []
    for i in range(len(l)-1):
        if l[i+1] >= l[i]:
            comrade_list.append(i+1)
    return comrade_list

ex = []
for i in range(100):
    ex.append(random.randint(0, 100))

print(f"Original list: {ex}")

sorted_list = stalin_sort(ex)

print(f"Sorted list: {sorted_list}")
    