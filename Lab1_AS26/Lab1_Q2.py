import random
import time

# 1 - Implement Bubble Sort
def bubble_sort_344(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# 2 - Implement Merge Sort
def merge_sort_344(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_344(arr[:mid])
    right = merge_sort_344(arr[mid:])

    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


sizes = [100, 500, 1000, 2000, 4000, 8000]

for size in sizes:
    # 3 - Generate random array of this size
    data = [random.randint(1, size) for i in range(size)]

    # copy so both sorts start from the same unsorted data
    data_copy1 = data.copy()
    data_copy2 = data.copy()

    # 4 - Measure execution time for Bubble Sort
    start = time.time()
    bubble_sort_344(data_copy1)
    end = time.time()
    bubble_time = end - start

    # 4 - Measure execution time for Merge Sort
    start = time.time()
    merge_sort_344(data_copy2)
    end = time.time()
    merge_time = end - start

    print("Size:", size, "Bubble:", bubble_time, "Merge:", merge_time)