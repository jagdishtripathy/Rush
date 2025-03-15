import os
import time
import threading
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
    new_file_path = f'{file_path}.replicated.{counter}'
    with open(new_file_path, 'wb') as new_file:
        new_file.write(doubled_data)

    return new_file_path

def replication_worker(initial_file_path):
    global stop_replication
    counter = 0
    while not stop_replication:
        initial_file_path = replicate_file(initial_file_path, counter)
        counter += 1
        time.sleep(0.001)  # Adjust the sleep time to control the replication rate

def signal_handler(sig, frame):
    global stop_replication
    print("Stopping replication...")
    stop_replication = True

def main():
    initial_file_path = 'initial_file.txt'
    with open(initial_file_path, 'wb') as file:
        file.write(b'0' * 4 * 1024 * 1024)  # Create a 4 MB file

    # Set up signal handler to stop the replication
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create multiple threads for replication
    threads = []
    for _ in range(1000):  # Adjust the number of threads as needed
        thread = threading.Thread(target=replication_worker, args=(initial_file_path,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()