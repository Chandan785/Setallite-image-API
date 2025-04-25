# get_token.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    url = "https://services.sentinel-hub.com/oauth/token"
    payload = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, data=payload)
    response.raise_for_status()
    token = response.json().get("access_token")
    return token

if __name__ == "__main__":
    token = get_access_token()
    print("Access Token:", token)
