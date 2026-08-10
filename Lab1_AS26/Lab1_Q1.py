import random
import time

# 1 - Implement Linear Search
def linear_search_344(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# 2 - Implement Binary Search (needs sorted array)
def binary_search_344(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

for size in sizes:
    # 3 - Generate random dataset of this size
    data = [random.randint(1, size) for i in range(size)]
    target = data[0]  # search for the first element

    # 4 - Sort the dataset before applying Binary Search
    sorted_data = sorted(data)

    # 5 - Measure execution time for Binary Search
    start = time.time()
    binary_search_344(sorted_data, target)
    end = time.time()
    binary_time = end - start

    # 5 - Measure execution time for Linear Search
    start = time.time()
    linear_search_344(data, target)
    end = time.time()
    linear_time = end - start

    print("Size:", size, "Linear:", linear_time, "Binary:", binary_time)