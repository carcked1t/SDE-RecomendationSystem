import requests

BASE = "http://127.0.0.1:8000"

def test_root():
    r = requests.get(BASE + "/")
    assert r.status_code == 200

def test_search():
    r = requests.get(BASE + "/products/search", params={"q": "Mouse"})
    assert r.status_code == 200

if __name__ == "__main__":
    print("Run these tests after starting the server")
    test_root()
    test_search()
    print("OK")
