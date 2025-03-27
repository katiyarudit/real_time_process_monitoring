import requests

API_URL = "http://127.0.0.1:5000"

def get_data(endpoint):
    return requests.get(f"{API_URL}/{endpoint}").json()
