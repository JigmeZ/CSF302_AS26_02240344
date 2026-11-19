import time

from closest import closest_pair, closest_pair_brute


def make_points(n):
    return [(i, (i * 37) % 100003) for i in range(n)]


print(f"{'n':>8} {'brute (s)':>12} {'divide (s)':>12}")
brute_total = 0
for n in (1000, 2000, 4000, 8000, 16000, 32000, 64000):
    points = make_points(n)
    start = time.perf_counter()
    closest_pair(points)
    divide_time = time.perf_counter() - start

    start = time.perf_counter()
    closest_pair_brute(points)
    brute_time = time.perf_counter() - start
    brute_total += brute_time
    print(f"{n:8} {brute_time:12.4f} {divide_time:12.4f}")
    if brute_total > 60:
        print("Brute-force timing stopped after 60 seconds.")
        break
