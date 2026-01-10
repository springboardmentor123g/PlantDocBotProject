import requests
import time

BASE_URL = "http://localhost:8001"

def test_root():
    try:
        response = requests.get(BASE_URL + "/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def check_server_ready(retries=15, delay=2):
    print("Checking if server is ready...")
    for i in range(retries):
        if test_root():
            print("Server is ready!")
            return True
        print(f"Server not ready yet, retrying in {delay}s...")
        time.sleep(delay)
    return False

if __name__ == "__main__":
    if check_server_ready():
        print("\n--- Starting Tests ---")
        # Add more specific tests here if needed, e.g., mocking file upload
        print("Basic connectivity verified.")
    else:
        print("Server failed to start or is not reachable.")
