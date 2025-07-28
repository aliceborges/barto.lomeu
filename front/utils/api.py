import os
import requests
import json
import pandas as pd

BASE_URL = os.getenv("BASE_URL", "http://localhost/")

def get_all_stats():
    response = requests.get(f"{BASE_URL}/all/stats")
    content = json.loads(response.content)
    return pd.DataFrame(content)

def get_history():
    response = requests.get(f"{BASE_URL}/all/history")
    content = json.loads(response.content)
    df = pd.DataFrame(content)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
