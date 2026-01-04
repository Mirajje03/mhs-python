import math
import time
import threading

from concurrent.futures import Executor, ThreadPoolExecutor, ProcessPoolExecutor

def helper(f, l, iters, step):
    result = 0
    for i in range(iters):
        result += f(l + i * step) * step

    return result

def integrate(f, a, b, executor, *, n_jobs=1, n_iter=10000000):
    step = (b - a) / n_iter

    futures = []
    for i in range(n_jobs):
        iters = (i + 1) * n_iter // n_jobs - i * n_iter // n_jobs
        future = executor.submit(helper, f, a + step * (i * n_iter // n_jobs), iters, step)
        futures.append(future)

    acc = 0
    for future in futures:
        acc += future.result()

    return acc

if __name__ == '__main__':
    filename = "artifacts/integrate.txt"
    cpu_num = 6

    with open(filename, "w") as f: 
        for n_jobs in range(1, cpu_num * 2 + 1):
            with ProcessPoolExecutor(max_workers=n_jobs) as executor:
                start_time = time.time()
                integrate(math.cos, 0, math.pi / 2, executor, n_jobs=n_jobs)
                message = f"Process pool executor, n_jobs = {n_jobs}, elapsed: {(time.time() - start_time):.5f} seconds\n"
                f.write(message)

        f.write("\n")

        for n_jobs in range(1, cpu_num * 2 + 1):
            with ThreadPoolExecutor(max_workers=n_jobs) as executor:
                start_time = time.time()
                integrate(math.cos, 0, math.pi / 2, executor, n_jobs=n_jobs)
                message = f"Thread pool executor, n_jobs = {n_jobs}, elapsed: {(time.time() - start_time):.5f} seconds\n"
                f.write(message)
