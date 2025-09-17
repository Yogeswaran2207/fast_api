import time

def fetch_data(api_id):
    print(f"Fetching data from API {api_id}...")
    time.sleep(2)  # simulate network delay
    print(f"Data from API {api_id} received.")
    return f"Data {api_id}"

def main_sync():
    start = time.time()
    results = []
    for i in range(1, 4):
        results.append(fetch_data(i))  # blocks until done
    print("All data fetched:", results)
    print("Time taken:", time.time() - start)

if __name__ == "__main__":
    main_sync()
