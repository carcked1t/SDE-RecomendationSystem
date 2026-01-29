"""Simple load test script that simulates searches and product views using requests.
This is not a full load test tool (like locust), but a simple script you can run to simulate activity.
"""
import requests
import random
import time

BASE = "http://127.0.0.1:8000"

def random_search():
    params = {
        "q": random.choice(["", "Mouse", "Headphones", "Notebook", "Bottle"]),
        "category": random.choice([None, "Electronics", "Home", "Stationery"]),
        "min_price": random.choice([None, 10, 20, 50]),
        "max_price": random.choice([None, 50, 150, 300]),
        "page": 1,
        "size": 5
    }
    # strip None
    params = {k: v for k, v in params.items() if v}
    r = requests.get(f"{BASE}/products/search", params=params)
    print("search", r.status_code)
    return r.json() if r.status_code == 200 else []


def view_random_product():
    # fetch some results then view a random product
    res = random_search()
    if not res:
        return
    pid = random.choice(res)["id"]
    r = requests.get(f"{BASE}/products/{pid}/view")
    print("view", pid, r.status_code)


def main(iterations=50):
    for i in range(iterations):
        if random.random() < 0.6:
            random_search()
        else:
            view_random_product()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
