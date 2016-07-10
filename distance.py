def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n] / m



def dis(list1, list2):
    list3 = []
    for i in range(len(list1)):
        list3.append([])
        for j in range(len(list1)):
            list3[i].append(distance(list1[i], list2[j]))
    return list3


def levenshtein_distance_computing(not_founded_names):
    raise NotImplementedError

