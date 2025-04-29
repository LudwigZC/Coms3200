import threading
import random
import time

print_lock = threading.Lock()
def worker(id):
    print(f"Worker {id} is running")
    sleep_time = random.randint(1,5)
    time.sleep(sleep_time)
    with print_lock:
        print(f"worker {id} finished after {sleep_time} seconds")


def main():
    threads = []
    for i in range(4):
        t = threading.Thread(target = worker, args = (i,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
        
    
    