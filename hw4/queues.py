import multiprocessing
import time
import codecs
import sys
import threading

def worker_a(input_queue, output_queue, start_time):
    while True:
        message = input_queue.get()
        if message is None:
            output_queue.put(None)
            break
        
        processed_message = message.lower()
        time.sleep(5)
        output_queue.put(processed_message)

def worker_b(input_queue, output_queue, start_time):
    while True:
        message = input_queue.get()
        if message is None:
            output_queue.put(None)
            break
        
        encoded_message = codecs.encode(message, 'rot_13')
        sys.stdout.write(f"Process B Output: {encoded_message}, time: {time.time() - start_time}\n")
        sys.stdout.flush()
        output_queue.put(encoded_message)

def result_listener(output_queue):
    while True:
        result = output_queue.get()
        if result is None:
            break

if __name__ == "__main__":
    start_time = time.time()

    queue_main_to_a = multiprocessing.Queue()
    queue_a_to_b = multiprocessing.Queue()
    queue_b_to_main = multiprocessing.Queue()

    process_a = multiprocessing.Process(target=worker_a, args=(queue_main_to_a, queue_a_to_b, start_time))
    process_b = multiprocessing.Process(target=worker_b, args=(queue_a_to_b, queue_b_to_main, start_time))

    process_a.start()
    process_b.start()

    listener_thread = threading.Thread(target=result_listener, args=(queue_b_to_main,))
    listener_thread.start()

    try:
        while True:
            user_input = input()
            print(f"User input: {user_input}, time: {time.time() - start_time}")
            if user_input.strip().lower() == 'exit':
                break
            queue_main_to_a.put(user_input)
    finally:
        queue_main_to_a.put(None)

        process_a.join()
        process_b.join()
        listener_thread.join()
