import time
import threading
import multiprocessing

def fib(n):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)

def run_sync(n, iterations):
    start_time = time.time()
    for _ in range(iterations):
        fib(n)

    return time.time() - start_time

def run_threading(n, iterations):
    start_time = time.time()
    threads = []
    for _ in range(iterations):
        thread = threading.Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    return time.time() - start_time

def run_multiprocessing(n, iterations):
    start_time = time.time()
    processes = []
    for _ in range(iterations):
        process = multiprocessing.Process(target=fib, args=(n,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    return time.time() - start_time

if __name__ == '__main__':
    number = 32
    times = 10
    filename = "artifacts/fib.txt"

    time_sync = run_sync(number, times)
    time_threads = run_threading(number, times)
    time_procs = run_multiprocessing(number, times)

    output_text = (
        f"Synchronous execution: {time_sync:.5f} seconds\n"
        f"Threading execution:   {time_threads:.5f} seconds\n"
        f"Multiprocessing execution: {time_procs:.5f} seconds\n"
    )

    with open(filename, "w") as f:
        f.write(output_text)
