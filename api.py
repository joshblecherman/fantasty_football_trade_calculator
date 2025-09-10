import requests

LEAGUE_ID = "1180258975719632896"

def fetch_drafts():
    url = f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/drafts"
    response = requests.get(url)
    print(1)

fetch_drafts()
